from django.shortcuts import get_object_or_404
from core import mixins
from crm.models import BookingInvoice, BackOrder
from accounts.models import User
from crm.forms import BackOrderUpdateForm
from masters.models import Stock, Variant
from .forms import BookingInvoiceUpdateFormInvoice, BookingInvoiceUpdateFormStock, BookingInvoiceUpdateFormTeamLead
from . import tables
from django.urls import reverse_lazy
from django.http import JsonResponse


class BillingRequestListView(mixins.HybridListView):
    model = BookingInvoice
    filterset_fields = {
        "booking_request__opportunity__customer_name": ["icontains"],
        "invoice_no": ["icontains"],
        "invoice_date": ["lte"],
    }
    template_name = "stock/billing_request_list.html"
    table_class = tables.BookingInvoiceTable

    def get_table_class(self):
        user = self.request.user
        if user.is_authenticated and user.usertype in ["team_lead", "asm"]:
            return tables.InvoicedTable

        return tables.BookingInvoiceTable

    def get_queryset(self):
        qs = super().get_queryset()
        usertype = self.request.user.usertype
        if usertype == "stock":
            qs = qs.filter(status="requested")
        elif usertype == "invoice_team":
            qs = qs.filter(status="alloted")
        elif usertype == "team_lead":
            # Filter opportunities based on DSEs associated with the team_lead
            dse_qs = User.objects.filter(branch__in=self.request.user.branch.all())
            qs = qs.filter(booking_request__opportunity__dse__in=dse_qs, status="invoiced")
        elif usertype == "asm":
            dse_qs = User.objects.filter(branch__in=self.request.user.branch.all())
            qs = qs.filter(booking_request__opportunity__dse__in=dse_qs,status="invoiced")
        elif usertype == "gm":
            qs = qs.filter(status="invoiced")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.usertype == "team_lead":
            context["title"] = "Invoiced"
        else:
            context["title"] = "Billing Request"
        context["is_billing_request_list"] = True
        return context


class BillingRequestUpdateView(mixins.HybridUpdateView):
    model = BookingInvoice
    template_name = "crm/delivery_request_form.html"

    def get_form_class(self):
        usertype = self.request.user.usertype
        if usertype == "stock":
            return BookingInvoiceUpdateFormStock
        elif usertype == "invoice_team":
            return BookingInvoiceUpdateFormInvoice
        elif usertype == "team_lead":
            return BookingInvoiceUpdateFormTeamLead
        else:
            return super().get_form_class()

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        usertype = self.request.user.usertype
        if usertype == "stock":
            form.fields["status"].choices = [("alloted", "Alloted"), ("rejected_stock_team", "Rejected")]
            form.fields["car_model"].initial = self.object.chassis.variant.car_model
            form.fields["variant"].initial = self.object.chassis.variant
            form.fields["chassis"].initial = self.object.chassis
        elif usertype == "team_lead":
            form.fields["state"].initial = self.object.district.state
            if self.object.temp_district and hasattr(self.object.temp_district, "state"):
                form.fields["temp_state"].initial = self.object.temp_district.state
            else:
                form.fields["temp_state"].initial = None
        return form

    def get_success_url(self):
        return reverse_lazy("stock:billing_request_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_request_details = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])

        selected_trim_id = self.object.chassis.variant.trim.id
        selected_color_id = self.object.chassis.variant.color.id
        selected_chassis_id = self.object.chassis.id
        selected_chassis_display = str(self.object.chassis)
        chassis_data = {
            "id": self.object.chassis.id,
            "chassis_number": f"{self.object.chassis.chassis_number} - {self.object.chassis.age()} days",
            # Add other fields as needed
        }
        print(
            "car_chassis",
            list(Stock.objects.filter(variant=self.object.chassis.variant).values("id", "chassis_number")),
        )
        context["selected_trim_id"] = selected_trim_id
        context["selected_color_id"] = selected_color_id
        context["selected_chassis_id"] = selected_chassis_id
        context["selected_chassis_display"] = selected_chassis_display
        qs = Stock.objects.filter(variant=self.object.chassis.variant, is_chassis_blocked=False)
        context["car_chassis"] = [{"id": x.id, "chassis_number": x.__str__()} for x in qs]
        context["car_color"] = list(
            Variant.objects.filter(trim=self.object.chassis.variant.trim).values("color__id", "color__name")
        )
        context["car_trim"] = list(
            Variant.objects.filter(car_model=self.object.chassis.variant.car_model).values("trim__id", "trim__name")
        )
        context["car_chassis"].append(chassis_data)

        context["title"] = "Billing Request Update"
        context["invoice_request_details"] = invoice_request_details
        context["is_stock_billing_req_update"] = True
        if self.object.status == "invoiced":
            context["title"] = "Delivery Plan"
            context["is_delivar_plan"] = True
        context["object"] = self.object
        return context

    def form_valid(self, form):
        booking_invoice = form.save(commit=False)
        usertype = self.request.user.usertype
        if usertype == "invoice_team":
            booking_invoice.status = "invoiced"
        if usertype == "team_lead":
            booking_invoice.status = "plan_pending"

        elif usertype == "stock" and booking_invoice.status == "rejected_stock_team":
            # Update the is_chassis_blocked field to False in the related Stock model j5
            booking_invoice.chassis.is_chassis_blocked = False
            booking_invoice.chassis.save()

        booking_invoice.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class BackOrderRequestListView(mixins.HybridListView):
    model = BackOrder
    table_class = tables.BackOrderRequestTable
    filterset_fields = ("back_order_need",)
    template_name = "stock/back_order_request_list.html"

    def get_queryset(self):
        return BackOrder.objects.filter(booking_request__stage="back_order_requested")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Back Order Request"
        context["is_back_order_request_list"] = True
        return context


class BackOrderRequestUpdateView(mixins.HybridUpdateView):
    model = BackOrder
    form_class = BackOrderUpdateForm

    def get_success_url(self):
        return reverse_lazy("stock:back_order_request_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Back Order Request Update"
        return context

    def form_valid(self, form):
        back_order = form.save(commit=False)
        booking_request = back_order.booking_request
        booking_request.stage = "back_order_created"
        booking_request.save()

        return super().form_valid(form)


def reject_invoice_status(request, pk):
    booking_invoice = get_object_or_404(BookingInvoice, pk=pk)
    booking_invoice.status = "rejected_invoice_team"
    booking_invoice.save()
    return JsonResponse({"status": "success"})
