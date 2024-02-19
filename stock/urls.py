from . import views
from django.urls import path


app_name = "stock"

urlpatterns = [
    path("billing-request/", views.BillingRequestListView.as_view(), name="billing_request_list"),
    path("billing-request/<str:pk>/update/", views.BillingRequestUpdateView.as_view(), name="billing_request_update"),
    path("back-order-request/", views.BackOrderRequestListView.as_view(), name="back_order_request_list"),
    path(
        "back-order-request/<str:pk>/update/",
        views.BackOrderRequestUpdateView.as_view(),
        name="back_order_request_update",
    ),
    path("invoice_reject_invoice_team/<str:pk>/", views.reject_invoice_status, name="invoice_reject_invoice_team"),
]
