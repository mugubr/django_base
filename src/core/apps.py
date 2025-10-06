from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        """
        This method is called when the application is ready.
        We import signals here to ensure they are registered.
        Este método é chamado quando a aplicação está pronta.
        Nós importamos os sinais aqui para garantir que eles sejam registrados.
        """
        import core.signals  # noqa: F401
