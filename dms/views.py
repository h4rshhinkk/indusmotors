from core import mixins
from crm.models import BookingRequest

from . import tables
from django.urls import reverse_lazy


class BookingRequestListView(mixins.HybridListView):
    model = BookingRequest
    table_class = tables.BookingRequestTable
    filterset_fields = ("order_no",)
    template_name = "dms/order_request_list.html"

    def get_queryset(self):
        excluded_stages = [
            "booking_request_approved",
            "back_order_requested",
            "back_order_created",
            "invoice_requested",
            "chassis_alloted",
            "chassis_reject",
            "invoice_accepted",
            "chassis_blocked",
        ]
        return super().get_queryset().filter(opportunity__stage="booking_requested").exclude(stage__in=excluded_stages)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Order Request"
        context["is_opportunity"] = True
        context["can_add"] = True
        context["new_link"] = reverse_lazy("dms:booking_request_list")
        context["is_dms_order_request"] = True
        return context


class BookingRequestDetailView(mixins.HybridDetailView):
    model = BookingRequest
    template_name = "dms/order_request_detail.html"
