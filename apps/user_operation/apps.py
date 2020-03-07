from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    name = 'user_operation'
    verbose_name = "Operations Management"

    def ready(self):
        import user_operation.signals
