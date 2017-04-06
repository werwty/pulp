from rest_framework import pagination

from pulp.app.models import DownloadCatalog
from pulp.app.serializers import DownloadCatalogSerializer
from pulp.app.viewsets import NamedModelViewSet


class DownloadCatalogPagination(pagination.CursorPagination):
    """
    Download catalog paginator, orders download catalog by importer when paginating.
    """
    ordering = 'importer'


class DownloadCatalogViewSet(NamedModelViewSet):
    endpoint_name = 'downloadcatalog'
    queryset = DownloadCatalog.objects.all()
    serializer_class = DownloadCatalogSerializer
    pagination_class = DownloadCatalogPagination
    http_method_names = ['get', 'options']
