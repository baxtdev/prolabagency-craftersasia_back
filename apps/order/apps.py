from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.order'
    verbose_name = "Заказы и Детали заказа"

    def ready(self) -> None:
        import apps.order.signals