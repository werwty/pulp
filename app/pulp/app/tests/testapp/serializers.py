from pulp.app.serializers import ContentSerializer

from pulp.app.tests.testapp.models import TestContent


class TestContentSerializer(ContentSerializer):
    class Meta:
        fields = ContentSerializer.Meta.fields + ('name',)
        model = TestContent
