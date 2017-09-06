import warnings

from django.shortcuts import get_object_or_404
from pulpcore.app.models import MasterModel
from rest_framework import viewsets, mixins

from rest_framework.reverse import reverse
from pulpcore.app import tasks
from pulpcore.app.response import OperationPostponedResponse

from pulpcore.common import tags
from rest_framework.response import Response
from rest_framework import status


class GenericNamedModelViewSet(viewsets.GenericViewSet):
    """
    A customized named ModelViewSet that knows how to register itself with the Pulp API router.

    This viewset is discoverable by its name.
    "Normal" Django Models and Master/Detail models are supported by the ``register_with`` method.

    Attributes:
        lookup_field (str): The name of the field by which an object should be looked up, in
            addition to any parent lookups if this ViewSet is nested. Defaults to 'pk'
        endpoint_name (str): The name of the final path segment that should identify the ViewSet's
            collection endpoint.
        nest_prefix (str): Optional prefix under which this ViewSet should be nested. This must
            correspond to the "parent_prefix" of a router with rest_framework_nested.NestedMixin.
            None indicates this ViewSet should not be nested.
        parent_lookup_kwargs (dict): Optional mapping of key names that would appear in self.kwargs
            to django model filter expressions that can be used with the corresponding value from
            self.kwargs, used only by a nested ViewSet to filter based on the parent object's
            identity.
    """
    endpoint_name = None
    nest_prefix = None
    parent_lookup_kwargs = {}

    @classmethod
    def is_master_viewset(cls):
        # ViewSet isn't related to a model, so it can't represent a master model
        if getattr(cls, 'queryset', None) is None:
            return False

        # ViewSet is related to a MasterModel subclass that doesn't have its own related
        # master model, which makes this viewset a master viewset.
        if (issubclass(cls.queryset.model, MasterModel) and
                cls.queryset.model._meta.master_model is None):
            return True

        return False

    @classmethod
    def register_with(cls, router):
        """
        Register this viewset with the API router using derived names and URL paths.

        When called, "normal" models will be registered with the API router using
        the defined endpoint_name as that view's URL pattern, and also as the base
        name for all views defined by this ViewSet (e.g. <endpoint_name>-list,
        <endpoint_name>-detail, etc...)

        Master/Detail models are also handled by this method. Detail ViewSets must
        subclass Master ViewSets, and both endpoints must have endpoint_name set.
        The URL pattern created for detail ViewSets will be a combination of the two
        endpoint_names::

            <master_viewset.endpoint_name>/<detail_viewset.endpoint_name>

        The base name for views generated will be similarly constructed::

            <master_viewset.endpoint_name>-<detail_viewset.endpoint_name>

        """
        # if we have a master model, include its endpoint name in endpoint pieces
        # by looking at its ancestry and finding the "master" endpoint name
        if cls.queryset is None:
            # If this viewset has no queryset, we can't begin to introspect its
            # endpoint. It is most likely a superclass to be used by Detail
            # Model ViewSet subclasses.
            return

        if cls.is_master_viewset():
            # If this is a master viewset, it doesn't need to be registered with the API
            # router (its detail subclasses will be registered instead).
            return

        if cls.queryset.model._meta.master_model is not None:
            # Model is a Detail model. Go through its ancestry (via MRO) to find its
            # eldest superclass with a declared name, representing the Master ViewSet

            master_endpoint_name = None
            # first item in method resolution is the viewset we're starting with,
            # so start finding parents at the second item, index 1.
            for eldest in reversed(cls.mro()):
                try:
                    if eldest.endpoint_name is not None:
                        master_endpoint_name = eldest.endpoint_name
                        break
                except AttributeError:
                    # no endpoint_name defined, need to get more specific in the MRO
                    continue

            pieces = (master_endpoint_name, cls.endpoint_name)

            # ensure that neither piece is None/empty and that they are not equal.
            if not all(pieces) or pieces[0] == pieces[1]:
                # unable to register; warn and return
                msg = ('Unable to determine viewset inheritance path for master/detail '
                       'relationship represented by viewset {}. Does the Detail ViewSet '
                       'correctly subclass the Master ViewSet, and do both have endpoint_name '
                       'set to different values?').format(cls.__name__)
                warnings.warn(msg, RuntimeWarning)
                return
        else:
            # "Normal" model, can just use endpoint_name directly.
            pieces = (cls.endpoint_name,)

        urlpattern = '/'.join(pieces)
        view_name = '-'.join(pieces)
        router.register(urlpattern, cls, view_name)

    def get_queryset(self):
        """
        Gets a QuerySet based on the current request.

        For nested ViewSets, this adds parent filters to the result returned by the superclass. For
        non-nested ViewSets, this returns the original QuerySet unchanged.

        Returns:
            django.db.models.query.QuerySet: the queryset returned by the superclass with additional
                filters applied that match self.parent_lookup_kwargs, to scope the results to only
                those associated with the parent object.
        """
        qs = super().get_queryset()
        if self.parent_lookup_kwargs:
            filters = {}
            for key, lookup in self.parent_lookup_kwargs.items():
                filters[lookup] = self.kwargs[key]
            qs = qs.filter(**filters)
        return qs

    def get_parent(self, parent_queryset):
        parent_key = ''
        if self.parent_lookup_kwargs:
            filters = {}
            for key, lookup in self.parent_lookup_kwargs.items():
                split_lookup = lookup.split('__')
                parent_key = split_lookup[0]
                parent_lookup = '__'.join(split_lookup[1:])
                filters[parent_lookup] = self.kwargs[key]
        return parent_key, get_object_or_404(parent_queryset, **filters)


class NestedAsyncUpdateModelMixin(object):
    """
    Update a model instance.
    """
    def update(self, request, *args, partial=False, **kwargs):

        parent_name, parent_queryset = self.get_parent(self.parent_viewset.queryset)
        lookup_name = kwargs.get(parent_name+'_'+self.lookup_field)
        url=reverse(self.nest_prefix+'-detail', args=[lookup_name], request=request)
        if request.data.get(parent_name) != url:
            return Response({"detail": "Cannot update parent"}, status=status.HTTP_400_BAD_REQUEST)

        data=request.data.copy()
        data.update({parent_name : url})

        object = self.get_object()
        serializer = self.get_serializer(object, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        app_label = object._meta.app_label
        async_result = self.task_type.update.apply_async_with_reservation(
            self.task_tag, lookup_name,
            args=(object.id, app_label, serializer.__class__.__name__),
            kwargs={'data': data, 'partial': partial}
        )
        return OperationPostponedResponse([async_result], request)

class NestedListModelMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        # make sure parent exists
        parent_name, parent_queryset = self.get_parent(self.parent_viewset.queryset)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class NestedNamedModelViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        NestedAsyncUpdateModelMixin,
                        NestedListModelMixin,
                        GenericNamedModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`, `partial_update()`,
    `destroy()` and `list()` actions.
    """
    pass

class NamedModelViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        GenericNamedModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`, `partial_update()`,
    `destroy()` and `list()` actions.
    """
    pass


class CreateDestroyReadNamedModelViewSet(mixins.CreateModelMixin,
                                         mixins.RetrieveModelMixin,
                                         mixins.DestroyModelMixin,
                                         mixins.ListModelMixin,
                                         GenericNamedModelViewSet):
    """
    A customized NamedModelViewSet for models that don't support updates.

    A viewset that provides default `create()`, `retrieve()`, `destroy()` and `list()` actions.

    """
    pass
