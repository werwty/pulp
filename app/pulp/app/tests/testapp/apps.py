from pulp.app.apps import PulpPluginAppConfig


class TestAppConfig(PulpPluginAppConfig):
    name = 'pulp.app.tests.testapp'
