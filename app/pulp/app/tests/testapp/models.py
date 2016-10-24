from django.db import models

from pulp.app.models import Content, Importer, Publisher


class TestContent(Content):
    TYPE = 'test'

    name = models.TextField()

    class Meta:
        pass


class TestImporter(Importer):
    TYPE = 'test'

    test_field = models.TextField()

    class Meta:
        pass


class TestPublisher(Publisher):
    TYPE = 'test'

    test_field = models.TextField()

    class Meta:
        pass
