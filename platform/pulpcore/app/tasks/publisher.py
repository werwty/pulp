from gettext import gettext as _

from celery import shared_task

from pulpcore.app import models
from pulpcore.app import serializers
from pulpcore.tasking.services import storage
from pulpcore.tasking.tasks import UserFacingTask


@shared_task(base=UserFacingTask)
def update(publisher_id, data, *args, **kwargs):
    instance = models.Publisher.objects.get(id=publisher_id)
    serializer = serializers.PublisherSerializer(instance, data=data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()


@shared_task(base=UserFacingTask)
def delete(repo_name, publisher_name):
    """
    Delete a :class:`~pulpcore.app.models.Publisher`

    :param repo_name:       the name of a repository
    :type  repo_name:       str
    :param publisher_name:  the name of a publisher
    :type  publisher_name:  str
    """
    models.Publisher.objects.filter(name=publisher_name, repository__name=repo_name).delete()

@shared_task(base=UserFacingTask)
def publish(repo_name, publisher_name):
    """
    Call publish on the publisher defined by a plugin.

    A working directory is prepared, the plugin's publish is called, and then working directory is
    removed.

    Args:
        repo_name (str): unique name to specify the repository.
        publisher_name (str): name to specify the Publisher.
    """
    publisher = models.Publisher.objects.get(name=publisher_name,
                                             repository__name=repo_name).cast()

    with storage.working_dir_context() as working_dir:
        publisher.working_dir = working_dir
        publisher.publish()
