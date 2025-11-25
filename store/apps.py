from django.apps import apps
from django.urls import path
from oscar.core.application import OscarConfig


class StoreConfig(OscarConfig):
    name = "store"

    def ready(self):
        super().ready()
        self.catalogue_app = apps.get_app_config("catalogue")
        self.basket_app = apps.get_app_config("basket")
        # Add other Oscar apps as needed

    def get_urls(self):
        urls = [
            path("catalogue/", self.catalogue_app.urls),
            path("basket/", self.basket_app.urls),
            # ... include other apps' URLs here
        ]
        return urls
