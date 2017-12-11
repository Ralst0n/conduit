from django.apps import AppConfig

class AuthenticationAppConfig(AppConfig):
    name = 'conduit.apps.authentication'
    label = 'authentication'
    verbose_name = 'Authentication'

    def ready(self):
        import conduit.apps.authentication.signals

# DJANGO CHECKS FOR default_app_config property
# for each registered app
default_app_config = 'conduit.apps.authentication.AuthenticationAppConfig'
