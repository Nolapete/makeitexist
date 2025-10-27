from django.urls import path
from . import views

app_name = "pantry"

urlpatterns = [
    path("", views.location_list, name="location_list"),
    path("location/<int:pk>/", views.location_detail, name="location_detail"),
    path("location/create/", views.location_create, name="location_create"),
    path("location/<int:pk>/edit/", views.location_update, name="location_update"),
    path("location/<int:pk>/delete/", views.location_delete, name="location_delete"),
    path("unit/<int:pk>/", views.storage_unit_detail, name="storage_unit_detail"),
    path("unit/<int:pk>/edit/", views.storage_unit_update, name="storage_unit_update"),
    path(
        "unit/<int:pk>/delete/", views.storage_unit_delete, name="storage_unit_delete"
    ),
    path("item/<int:pk>", views.pantry_item_detail, name="pantry_item_detail"),
    path("item/<int:pk>/edit/", views.pantry_item_update, name="pantry_item_update"),
    path("item/add/", views.pantry_item_create, name="pantry_item_create"),
    path("stock/add/", views.stock_add, name="stock_add"),
    path("stock/<int:pk>/edit/", views.stock_edit, name="stock_edit"),
    path("stock/<int:pk>/delete/", views.stock_delete, name="stock_delete"),
    path("scan/", views.barcode_scan, name="barcode_scan"),
    path("alerts/", views.alerts_dashboard, name="alerts_dashboard"),
    path("api/scan/", views.api_barcode_scan, name="api_barcode_scan"),
]
