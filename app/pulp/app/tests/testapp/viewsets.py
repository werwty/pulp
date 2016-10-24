from pulp.app import viewsets

from pulp.app.tests.testapp.models import TestContent
from pulp.app.tests.testapp.serializers import TestContentSerializer


class TestContentViewSet(viewsets.ContentViewSet):
    endpoint_name = 'test'
    queryset = TestContent.objects.all()
    serializer_class = TestContentSerializer
