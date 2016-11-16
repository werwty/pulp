from rest_framework import serializers

from pulp.app import models
from pulp.app.serializers import (MasterModelSerializer, ModelSerializer,
                                  NotesKeyValueRelatedField, RepositoryRelatedField,
                                  ScratchpadKeyValueRelatedField, ContentRelatedField, ContentSerializer, base)


class RepositorySerializer(ModelSerializer):
    # _href is normally provided by the base class, but Repository's
    # "name" lookup field means _href must be explicitly declared.
    _href = serializers.HyperlinkedIdentityField(
        view_name='repositories-detail',
        lookup_field='name',
    )
    name = serializers.CharField(
        help_text='A unique name for this repository.',
        write_only=True
    )

    description = serializers.CharField(
        help_text='An optional description.',
        required=False
    )

    last_content_added = serializers.DateTimeField(
        help_text='Timestamp of the most recent addition of content to this repository.',
        read_only=True
    )

    last_content_removed = serializers.DateTimeField(
        help_text='Timestamp of the most recent removal of content to this repository.',
        read_only=True
    )
    notes = NotesKeyValueRelatedField()
    scratchpad = ScratchpadKeyValueRelatedField()

    class Meta:
        model = models.Repository
        fields = ModelSerializer.Meta.fields + ('name', 'description', 'notes', 'scratchpad',
                                                'last_content_added', 'last_content_removed')


class RepositoryGroupSerializer(ModelSerializer):
    name = serializers.CharField(
        help_text='A unique name for this repository group.'
    )
    description = serializers.CharField(
        help_text='An optional description of the repository group.',
        required=False
    )
    members = RepositoryRelatedField(many=True)
    scratchpad = ScratchpadKeyValueRelatedField()
    notes = NotesKeyValueRelatedField()

    class Meta:
        model = models.RepositoryGroup
        fields = ModelSerializer.Meta.fields + ('name', 'description', 'members', 'scratchpad',
                                                'notes')


class ImporterSerializer(MasterModelSerializer):
    """
    Every importer defined by a plugin should have an Importer serializer that inherits from this
    class. Please import from `pulp.app.serializers` rather than from this module directly.
    """
    # _href is normally provided by the base class, but Importer's
    # "name" lookup field means _href must be explicitly declared.
    _href = serializers.HyperlinkedIdentityField(
        view_name='importers-detail',
        lookup_field='name',
    )
    name = serializers.CharField(
        help_text='A name for this importer, unique within the associated repository.'
    )

    repository = RepositoryRelatedField()

    class Meta:
        abstract = True
        model = models.Publisher
        fields = MasterModelSerializer.Meta.fields + (
            'name', 'last_updated', 'repository', 'auto_publish', 'relative_path', 'last_published'
        )


class ContentURLSerializer(MasterModelSerializer):
    _href = ContentRelatedField()

    class Meta:
        fields = MasterModelSerializer.Meta.fields
        model = models.RepositoryContent

class RepositoryContentSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(RepositoryContentSerializer, self).__init__(*args, **kwargs)
        self.fields['content'] = ContentURLSerializer(context=self.context)

    #content = ContentRelatedField(context=self.context)

    repository = RepositoryRelatedField()

    class Meta:
        model = models.RepositoryContent
        fields = (
         'repository', 'content'
        )

