from . import views
from django.urls import path


app_name = "dms"

urlpatterns = [
    path("booking-request/", views.BookingRequestListView.as_view(), name="booking_request_list"),
    path("booking-request/detail/<str:pk>/", views.BookingRequestDetailView.as_view(), name="booking_request_detail"),
]
