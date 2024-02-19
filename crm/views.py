from django.shortcuts import redirect
from datetime import date
from django.forms.models import BaseModelForm
from accounts.models import User
from django.forms import formset_factory
from core import mixins
from masters.models import Document,LostSubReason, District
from masters.models import Variant
from masters.models import Stock
from stock.forms import BookingInvoiceUpdateFormTeamLead
from . import tables
from .forms import (
    BOOKINGINVOICEDOCUMENTFORMSET,
    INVOICETOPUPFORMSET,
    AccountsTeamInvoiceUpdateForm,
    BookingFollowUpFormFinanceExecutive,
    BookingInvoiceForm,
    DailyReportForm,
    DigitalLeadLostForm,
    InvoiceDocumentForm,
    InvoiceDocumentFormset,
    InvoiceAccessoryForm,
    DocumentUploadForm,
    TestDrivePendingUpdateForm,
    AfterDeliveryFollowUpForm,
    DigitalLeadEnquiryForm,
    EventReportForm
)
from .forms import BookingRequestForm, InvoiceDiscountForm
from .forms import BookingRequestUpdateForm
from .forms import ChassisBlockForm
from .forms import OpportunityFollowUpFormFinanceExecutive
from .forms import OpportunityForm
from .forms import OpportunityLostForm, BookingLostForm, BookingLostUpdateForm
from .forms import TestDriveRequestForm, BackOrderForm
from .models import (
    AfterDeliveryFollowup,
    BackOrder,
    BookingInvoiceDocument,
    DailyReport,
    DigitalLeadEnquiry,
    DigitalLeadEnquiryLost,
    DigitalLeadFollowUp,
    EventCustomerDetails,
    EventPhoto,
    EventReport,
    InvoiceAccessory,
    InvoiceDiscount,
    InvoiceDocument,
    InvoiceTopUp,
    RegistrationRemark,
)
from .models import BookingFollowUp
from .models import BookingInvoice
from .models import BookingRequest
from .models import ChassisBlock
from .models import Opportunity
from .models import OpportunityFollowUp
from .models import OpportunityLost, BookingLost
from .models import TestDriveRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Q
from .create_pdf import PDFView


class VariantListView(View):
    def get(self, request, *args, **kwargs):
        car_model = request.GET.get("car_model")
        trim = request.GET.get("trim")
        color = request.GET.get("color")

        queryset = Variant.objects.all()
        if car_model:
            queryset = queryset.filter(car_model=car_model)
        if trim:
            queryset = queryset.filter(trim=trim)
        if color:
            queryset = queryset.filter(color=color)

        variants = list(queryset.values("id", "vehicle_code").distinct())
        colors = list(queryset.values("color__id", "color__name").distinct())
        trims = list(queryset.values("trim__id", "trim__name").distinct())
        return JsonResponse({"variants": variants, "colors": colors, "trims": trims})


class GetChassisListView(View):
    def get(self, request, *args, **kwargs):
        variant_id = request.GET.get("variant_id")
        variant = get_object_or_404(Variant, pk=variant_id)
        queryset = Stock.objects.filter(variant=variant, is_chassis_blocked=False)
        stocks = [{"id": x.id, "chassis_number": x.__str__()} for x in queryset]
        return JsonResponse({"stocks": stocks})


class ReasonListView(View):
    def get(self, request, *args, **kwargs):
        reason = request.GET.get("reason")
        queryset = LostSubReason.objects.all()
        if reason:
            queryset = queryset.filter(reason=reason)
        lost_sub_reasons = list(queryset.values("id", "name"))
        return JsonResponse({"lost_sub_reasons": lost_sub_reasons})


class StateListView(View):
    def get(self, request, *args, **kwargs):
        state = request.GET.get("state")
        queryset = District.objects.all()
        if state:
            queryset = queryset.filter(state=state)
        district = list(queryset.values("id", "name"))
        return JsonResponse({"district": district})


class OpportunityListView(mixins.HybridListView):
    model = Opportunity
    table_class = tables.OpportunityTable
    filterset_fields = {"opt_id": ["icontains"], "opt_status": ["exact"], "opt_date": ["lte"]}
    template_name = "crm/opportunity_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Opportunity"
        context["is_opportunity"] = True
        context["can_add"] = True
        context["new_link"] = reverse_lazy("crm:opportunity_create")
        return context
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.usertype in ("team_lead", "asm", "sm", "finance_executive"):
            dse_qs = User.objects.filter(branch__in=self.request.user.branch.all())
            qs = qs.filter(dse__in=dse_qs)
        elif self.request.user.usertype == "customer_advisor":
            qs = qs.filter(dse=self.request.user)
        else:
            qs = qs
        qs = qs.exclude(stage="booking_requested")

        return qs


class OpportunityDetailView(mixins.HybridDetailView):
    model = Opportunity
    template_name = "crm/opportunity_detail.html"


class OpportunityCreateView(mixins.HybridCreateView):
    model = Opportunity
    template_name = "crm/opportunity_form.html"
    form_class = OpportunityForm

    def get_form(self, *args, **kwargs):
        # TODO: Filter qs by usertype
        form = super().get_form(*args, **kwargs)
        if self.request.user.usertype == "team_lead":
            form.fields["dse"].queryset = User.objects.filter(
                branch__in=self.request.user.branch.all(), usertype="customer_advisor"
            )
        elif self.request.user.usertype == "customer_advisor":
            form.fields["dse"].initial = self.request.user
            form.fields["dse"].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Opportunity Entry"
        context["is_opportunity_entry"] = True
        return context


class OpportunityUpdateView(mixins.HybridUpdateView):
    model = Opportunity
    template_name = "crm/opportunity_form.html"
    form_class = OpportunityForm

    def get_form(self, *args, **kwargs):
        # TODO: Filter qs by usertype
        form = super().get_form(*args, **kwargs)
        if self.request.user.usertype == "branch":
            form.fields["dse"].queryset = User.objects.filter(branch__user=self.request.user, usertype="dse")
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Opportunity Update"
        return context


class OpportunityDeleteView(mixins.HybridDeleteView):
    model = Opportunity


class OpportunityFollowUpCreateView(mixins.HybridCreateView):
    model = OpportunityFollowUp
    exclude = ("is_active", "opportunity", "finance_executive_status", "finance_executive_remark")
    template_name = "crm/followup_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:opportunity_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opportunity = get_object_or_404(Opportunity, pk=self.kwargs["pk"])
        followups = OpportunityFollowUp.objects.filter(opportunity=opportunity)
        context["opportunity"] = opportunity
        context["title"] = "Opportunity Follow Up"
        context["followups"] = tables.OpportunityFollowUpTable(followups)
        return context

    def form_valid(self, form):
        opportunity = get_object_or_404(Opportunity, pk=self.kwargs["pk"])
        form.instance.opportunity = opportunity  # Set the foreign key
        return super().form_valid(form)


class OpportunityFollowUpDetailView(mixins.HybridDetailView):
    model = OpportunityFollowUp

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Opportunity Follow Up"
        return context


class OpportunityFollowUpUpdateView(mixins.HybridUpdateView):
    model = OpportunityFollowUp
    template_name = "crm/followup_form.html"
    exclude = ("is_active", "opportunity", "finance_executive_status", "finance_executive_remark")

    def get_form_class(self):
        usertype = self.request.user.usertype
        if usertype == "finance_executive":
            return OpportunityFollowUpFormFinanceExecutive
        return super().get_form_class()

    def get_success_url(self):
        return reverse_lazy("crm:followup_create", kwargs={"pk": self.object.opportunity.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Opportunity FollowUp Update"
        return context


class TestDriveRequestCreateView(mixins.HybridCreateView):
    model = TestDriveRequest
    template_name = "crm/testdrive_form.html"
    form_class = TestDriveRequestForm

    def get_success_url(self):
        return reverse_lazy("crm:testdrive_create", kwargs={"pk": self.kwargs["pk"]})

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        opportunity = get_object_or_404(Opportunity, pk=self.kwargs["pk"])

        # Set initial values for the fields from the Opportunity model
        form.initial["car_model"] = opportunity.variant.car_model
        form.initial["trim"] = opportunity.variant.trim
        form.initial["color"] = opportunity.variant.color
        form.initial["variant"] = opportunity.variant  # Assuming 'variant' is a ForeignKey field in TestDriveRequest

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opportunity = get_object_or_404(Opportunity, pk=self.kwargs["pk"])
        drive_requests = TestDriveRequest.objects.filter(opportunity=opportunity, is_active=True)
        context["opportunity"] = opportunity
        context["title"] = "Test Drive Request"
        context["drive_requests"] = tables.TestDriveRequestTable(drive_requests)
        return context

    def form_valid(self, form):
        opportunity = get_object_or_404(Opportunity, pk=self.kwargs["pk"])
        form.instance.opportunity = opportunity
        if BookingRequest.objects.filter(
            opportunity=opportunity, stage__in=["booking_request_approved", "chassis_blocked"]
        ).exists():
            form.instance.testdrive_stage = "after_booking"
        else:
            form.instance.testdrive_stage = "from_opportunity"

        return super().form_valid(form)


class TestDriveRequestUpdateView(mixins.HybridUpdateView):
    model = TestDriveRequest
    template_name = "crm/testdrive_form.html"
    form_class = TestDriveRequestForm

    def get_success_url(self):
        return reverse_lazy("crm:testdrive_create", kwargs={"pk": self.object.opportunity.pk})

    def get_delete_url(self):
        return reverse_lazy("crm:testdrive_create", kwargs={"pk": self.object.opportunity.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "TestDrive Request Update"
        return context


class TestDriveRequestDeleteView(mixins.HybridDeleteView):
    model = TestDriveRequest


class OpportunityLostCreateView(mixins.HybridCreateView):
    form_class = OpportunityLostForm
    template_name = "crm/opt_lost_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:opt_lost_create", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opportunity = get_object_or_404(Opportunity, pk=self.kwargs["pk"])
        opt_lost = OpportunityLost.objects.filter(opportunity=opportunity, is_active=True)
        context["opportunity"] = opportunity
        context["opt_lost"] = tables.OpportunityLostTable(opt_lost)

        return context

    def form_valid(self, form):
        opportunity = get_object_or_404(Opportunity, pk=self.kwargs["pk"])
        form.instance.opportunity = opportunity  # Set the foreign key

        # Update the stage of the Opportunity model to 'opportunity_lost'
        opportunity.stage = "opportunity_lost"
        opportunity.save()

        return super().form_valid(form)


class OpportunityLostUpdateView(mixins.HybridUpdateView):
    model = OpportunityLost
    template_name = "crm/opt_lost_form.html"
    form_class = OpportunityLostForm

    def get_success_url(self):
        return reverse_lazy("crm:opt_lost_create", kwargs={"pk": self.object.opportunity.pk})

    def get_delete_url(self):
        return reverse_lazy("crm:opt_lost_delete", kwargs={"pk": self.object.opportunity.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Opportunity Lost Update"
        return context


class OpportunityLostDeleteView(mixins.HybridDeleteView):
    model = OpportunityLost


class BookingRequestCreateView(mixins.HybridCreateView):
    model = BookingRequest
    form_class = BookingRequestForm
    template_name = "crm/booking_request_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:opportunity_list")

    def get_delete_url(self):
        return reverse_lazy("crm:booking_request_delete", kwargs={"pk": self.object.opportunity.pk})

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        opportunity = get_object_or_404(Opportunity, pk=self.kwargs["pk"])
        if BookingRequest.objects.filter(opportunity=opportunity).exists():
            instance = BookingRequest.objects.get(opportunity__pk=self.kwargs["pk"])
            form = BookingRequestForm(instance=instance, data=self.request.POST or None)
        
        if self.request.user.usertype == "team_lead":
            form.fields["dse"].queryset = User.objects.filter(
                branch__in=self.request.user.branch.all(), usertype="customer_advisor"
            )
        elif self.request.user.usertype == "customer_advisor":
            form.fields["dse"].initial = self.request.user
            form.fields["dse"].disabled = True

        

        # Set initial values for the form based on the Opportunity
        form.fields["opt_id"].initial = opportunity.opt_id
        form.fields["dse"].initial = opportunity.dse
        form.fields["customer_salutation"].initial = opportunity.customer_salutation
        form.fields["customer_name"].initial = opportunity.customer_name
        form.fields["mobile"].initial = opportunity.mobile
        form.fields["phone"].initial = opportunity.phone
        form.fields["address"].initial = opportunity.address
        form.fields["place"].initial = opportunity.place
        form.fields["district"].initial = opportunity.district
        # form.fields['state'].initial = opportunity.district.state
        form.fields["email"].initial = opportunity.email
        form.fields["profession"].initial = opportunity.profession
        form.fields["profession_detail"].initial = opportunity.profession_detail
        form.fields["guardian_salutation"].initial = opportunity.guardian_salutation
        form.fields["guardian_name"].initial = opportunity.guardian_name
        form.fields["opt_type"].initial = opportunity.opt_type
        form.fields["exchange_vehicle_make"].initial = opportunity.exchange_vehicle_make
        form.fields["exchange_vehicle_model"].initial = opportunity.exchange_vehicle_model
        form.fields["exchange_reg_no"].initial = opportunity.exchange_reg_no
        form.fields["exchange_mfg_year"].initial = opportunity.exchange_mfg_year
        form.fields["owner_name"].initial = opportunity.owner_name
        form.fields["relation"].initial = opportunity.relation
        form.fields["variant"].initial = opportunity.variant
        form.fields["car_model"].initial = opportunity.variant.car_model
        form.fields["trim"].initial = opportunity.variant.trim
        form.fields["color"].initial = opportunity.variant.color
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opportunity = get_object_or_404(Opportunity, pk=self.kwargs["pk"])
        booking_request_list = BookingRequest.objects.filter(opportunity=opportunity, is_active=True)
        context["opportunity"] = opportunity
        context["booking_request_list"] = tables.BookingRequestedTable(booking_request_list)
        context["title"] = "Create Booking Request"
        return context

    def form_valid(self, form):
        opportunity = get_object_or_404(Opportunity, pk=self.kwargs["pk"])
        if BookingRequest.objects.filter(opportunity=opportunity, is_active=True).exists():
            # instance = BookingRequest.objects.get(opportunity__pk=self.kwargs['pk'])
            form = BookingRequestForm(self.request.POST)
            form.save(commit=False)
            form.instance.opportunity = opportunity
        else:
            form.instance.opportunity = opportunity
            form.instance.stage = "booking_requested"
            form.save()

        # Update the Opportunity fields
        opportunity.opt_id = form.cleaned_data["opt_id"]
        opportunity.dse = form.cleaned_data["dse"]
        opportunity.customer_salutation = form.cleaned_data["customer_salutation"]
        opportunity.customer_name = form.cleaned_data["customer_name"]
        opportunity.mobile = form.cleaned_data["mobile"]
        opportunity.phone = form.cleaned_data["phone"]
        opportunity.address = form.cleaned_data["address"]
        opportunity.place = form.cleaned_data["place"]
        opportunity.district = form.cleaned_data["district"]
        # opportunity.state = form.cleaned_data['state']
        opportunity.email = form.cleaned_data["email"]
        opportunity.profession = form.cleaned_data["profession"]
        opportunity.profession_detail = form.cleaned_data["profession_detail"]
        opportunity.guardian_salutation = form.cleaned_data["guardian_salutation"]
        opportunity.guardian_name = form.cleaned_data["guardian_name"]
        opportunity.opt_type = form.cleaned_data["opt_type"]
        opportunity.variant = form.cleaned_data["variant"]
        opportunity.car_model = form.cleaned_data["car_model"]
        opportunity.trim = form.cleaned_data["trim"]
        opportunity.color = form.cleaned_data["color"]
        opportunity.stage = "booking_requested"
        opportunity.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class BookingRequestUpdateView(mixins.HybridUpdateView):
    model = BookingRequest
    form_class = BookingRequestUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Booking Request Update"
        return context

    def form_valid(self, form):
        data = form.save(commit=False)
        data.stage = "booking_request_approved"
        data.save()
        return super().form_valid(form)


class BookingRequestDeleteView(mixins.HybridDeleteView):
    model = BookingRequest

    def get_success_url(self):
        return reverse_lazy("crm:booking_request_create", kwargs={"pk": self.object.opportunity.pk})


# Booking Tracker List /
class BookingTrackerListView(mixins.HybridListView):
    model = BookingRequest
    table_class = tables.BookingRequestTable
    filterset_fields = {"order_no": ["icontains"], "order_date": ["lte"]}
    template_name = "crm/booking_tracker_list.html"

    def get_queryset(self):
        if self.request.user.usertype in ("team_lead", "asm", "sm", "finance_executive"):
            dse_qs = User.objects.filter(branch__in=self.request.user.branch.all())
            qs = (
                super()
                .get_queryset()
                .filter(
                    opportunity__dse__in=dse_qs,
                    stage__in=[
                        "booking_request_approved",
                        "chassis_blocked",
                        "back_order_requested",
                        "back_order_created",
                        "booking_request_lost_with_refund",
                        "booking_request_lost_without_refund",
                    ],
                )
            )
        elif self.request.user.usertype == "customer_advisor":
            qs = (
                super()
                .get_queryset()
                .filter(
                    opportunity__dse=self.request.user,
                    stage__in=[
                        "booking_request_approved",
                        "chassis_blocked",
                        "back_order_requested",
                        "back_order_created",
                        "booking_request_lost_with_refund",
                        "booking_request_lost_without_refund",
                    ],
                )
            )
        else:
            qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Booking Tracker"
        context["is_booking_tracker_list"] = True
        return context


class BookingFollowUpCreateView(mixins.HybridCreateView):
    model = BookingFollowUp
    exclude = ("is_active", "booking_request", "finance_executive_status", "finance_executive_remark")
    template_name = "crm/booking_followup_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:booking_tracker_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])
        booking_followups = BookingFollowUp.objects.filter(booking_request=booking_request)
        context["booking_request"] = booking_request
        context["booking_followups"] = tables.BookingFollowUpTable(booking_followups)
        context["title"] = "Booking FollowUp"
        return context

    def form_valid(self, form):
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])
        form.instance.booking_request = booking_request  # Set the foreign key
        return super().form_valid(form)


class BookingFollowUpDetailView(mixins.HybridDetailView):
    model = BookingFollowUp

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Booking Follow Up"
        return context


class BookingFollowUpUpdateView(mixins.HybridUpdateView):
    model = BookingFollowUp
    exclude = ("booking_request", "is_active", "finance_executive_status", "finance_executive_remark")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Booking Follow Up"
        return context

    def get_success_url(self):
        return reverse_lazy("crm:booking_followup_create", kwargs={"pk": self.object.booking_request.pk})

    def get_form_class(self):
        usertype = self.request.user.usertype
        if usertype == "finance_executive":
            return BookingFollowUpFormFinanceExecutive
        return super().get_form_class()


class BookingLostCreateView(mixins.HybridCreateView):
    form_class = BookingLostForm
    template_name = "crm/booking_lost_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:booking_lost_create", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])
        booking_lost = BookingLost.objects.filter(booking_request=booking_request, is_active=True)
        context["booking_request"] = booking_request
        context["booking_lost"] = tables.BookingLostTable(booking_lost)
        context["title"] = "Booking Lost Create"
        return context

    def form_valid(self, form):
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])
        form.instance.booking_request = booking_request  # Set the foreign key
        return super().form_valid(form)


class BookingLostUpdateView(mixins.HybridUpdateView):
    model = BookingLost
    template_name = "crm/booking_lost_form.html"
    form_class = BookingLostForm

    def get_success_url(self):
        return reverse_lazy("crm:booking_lost_create", kwargs={"pk": self.object.booking_request.pk})

    def get_delete_url(self):
        return reverse_lazy("crm:booking_lost_delete", kwargs={"pk": self.object.booking_request.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Booking Lost Edit"
        return context


class BookingLostDeleteView(mixins.HybridDeleteView):
    model = BookingLost


# booking_cancelation_verfy_asm_gm_accounts
class BookingLostListView(mixins.HybridListView):
    model = BookingLost
    table_class = tables.BookingLostTable
    filterset_fields = ("booking_request__order_no", "booking_request__order_date")

    def get_queryset(self):
        usertype = self.request.user.usertype
        if usertype == "gm":
            return super().get_queryset().filter(stage="forward")
        elif usertype == "accounts":
            return super().get_queryset().filter(stage="approve")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Booking Cancelation List"
        context["is_booking_lost_list"] = True
        return context


# dpt asm gm accounts verification update
class BookingLostDptUpdateView(mixins.HybridUpdateView):
    model = BookingLost
    template_name = "crm/booking_lost_dpt_update_form.html"
    form_class = BookingLostUpdateForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        usertype = self.request.user.usertype
        if usertype in ("asm", "gm", "sm"):
            form.fields["stage"].choices = [("approve", "Approve"), ("forward", "Forward")]
        elif usertype in ("accounts",):
            form.fields["stage"].choices = [("refund", "Refund")]
        return form

    def get_success_url(self):
        return reverse_lazy("crm:booking_lost_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_canceled = get_object_or_404(BookingLost, pk=self.kwargs["pk"])
        context["booking_canceled"] = booking_canceled
        context["title"] = "Booking Cancelation Update"
        return context

    def form_valid(self, form):
        booking_lost = form.save(commit=False)
        booking_request = booking_lost.booking_request
        if booking_lost.stage == "refund":
            booking_request.stage = "booking_request_lost_with_refund"
        else:
            pass
        booking_request.save()
        return super().form_valid(form)


class BackOrderCreateView(mixins.HybridCreateView):
    model = BackOrder
    template_name = "crm/back_order_form.html"
    form_class = BackOrderForm

    def get_success_url(self):
        return reverse_lazy("crm:back_order_create", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])
        back_order = BackOrder.objects.filter(booking_request=booking_request)
        context["booking_request"] = booking_request
        context["back_order"] = tables.BackOrderTable(back_order)
        return context

    def form_valid(self, form):
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])
        form.instance.booking_request = booking_request
        booking_request.stage = "back_order_requested"
        booking_request.save()
        return super().form_valid(form)


class ChassisBlockCreateView(mixins.HybridCreateView):
    model = ChassisBlock
    template_name = "crm/chassis_block_form.html"
    form_class = ChassisBlockForm

    def get_success_url(self):
        return reverse_lazy("crm:chassis_block_create", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])
        chassis_block = ChassisBlock.objects.filter(booking_request=booking_request)
        context["booking_request"] = booking_request
        context["chassis_block"] = tables.ChassisBlockTable(chassis_block)
        context["title"] = "Chassis Block"
        return context

    def form_valid(self, form):
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])
        booking_request.stage = "chassis_blocked"
        booking_request.save()
        form.instance.booking_request = booking_request
        form.instance.is_chassis_blocked = True
        form.instance.stock.save()
        return super().form_valid(form)


class BookingInvoiceCreateView(mixins.HybridCreateView):
    model = BookingInvoice
    form_class = BookingInvoiceForm
    template_name = "crm/invoice_request_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])

        selected_trim_id = booking_request.variant.trim.id
        selected_color_id = booking_request.variant.color.id

        context["booking_request"] = booking_request

        context["selected_trim_id"] = selected_trim_id
        context["selected_color_id"] = selected_color_id
        context["title"] = "Invoice Request"
        context["is_create"] = "Invoice Request"
        chassis_qs = Stock.objects.filter(variant=booking_request.variant, is_chassis_blocked=False)
        context["car_chassis"] = [{"id": x.id, "chassis_number": x.__str__()} for x in chassis_qs]
        context["car_color"] = list(
            Variant.objects.filter(trim=booking_request.variant.trim).values("color__id", "color__name")
        )
        context["car_trim"] = list(
            Variant.objects.filter(car_model=booking_request.variant.car_model).values("trim__id", "trim__name")
        )

        context["is_invoice_create"] = True

        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])

        form.fields["dse"].initial = booking_request.opportunity.dse
        form.fields["customer_salutation"].initial = booking_request.opportunity.customer_salutation
        form.fields["customer_name"].initial = booking_request.opportunity.customer_name
        form.fields["mobile"].initial = booking_request.opportunity.mobile
        form.fields["email"].initial = booking_request.opportunity.email
        form.fields["guardian_salutation"].initial = booking_request.opportunity.guardian_salutation
        form.fields["guardian_name"].initial = booking_request.opportunity.guardian_name
        form.fields["dob"].initial = booking_request.opportunity.dob
        form.fields["house_name"].initial = booking_request.opportunity.address
        form.fields["place"].initial = booking_request.opportunity.place
        form.fields["state"].initial = (
            booking_request.opportunity.district.state if booking_request.opportunity.district else None
        )
        form.fields["district"].initial = booking_request.opportunity.district
        form.fields["exchange_vehicle_make"].initial = booking_request.opportunity.exchange_vehicle_make
        form.fields["exchange_vehicle_model"].initial = booking_request.opportunity.exchange_vehicle_model
        form.fields["exchange_reg_no"].initial = booking_request.opportunity.exchange_reg_no
        form.fields["exchange_mfg_year"].initial = booking_request.opportunity.exchange_mfg_year
        form.fields["owner_name"].initial = booking_request.opportunity.owner_name
        form.fields["relation"].initial = booking_request.opportunity.relation
        form.fields["scheme"].initial = booking_request.scheme
        form.fields["scheme_name"].initial = booking_request.scheme_name
        form.fields["institution_name"].initial = booking_request.institution_name
        form.fields["amount"].initial = booking_request.amount
        form.fields["yono_scheme_amount"].initial = booking_request.yono_scheme_amount

        form.fields["car_model"].initial = booking_request.variant.car_model
        # form.fields['trim'].initial = booking_request.variant.trim
        # form.fields['color'].initial = booking_request.variant.color
        form.fields["variant"].initial = booking_request.variant
        # form.fields['chassis'].queryset = Stock.objects.filter(variant=booking_request.variant, is_chassis_blocked=False)
        form.fields["opt_id"].initial = booking_request.opportunity.opt_id
        form.fields["booking_no"].initial = booking_request.order_no
        form.fields["booking_date"].initial = booking_request.order_date
        
        
        return form

    def form_valid(self, form):
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])
        BookingRequest.objects.filter(pk=self.kwargs["pk"]).update(stage="invoice_requested")
        form.instance.booking_request = booking_request
        variant = form.cleaned_data.get("variant")
        form.instance.showroom_price = variant.showroom_price
        form.instance.insurance = variant.insurance
        form.instance.road_tax = variant.road_tax
        form.instance.registration_charge = variant.registration_charge
        form.instance.tcs = variant.tcs
        form.instance.rsa = variant.rsa
        form.instance.p2p = variant.p2p
        form.instance.extended_warranty = variant.extended_warranty
        chassis = form.instance.chassis
        chassis.is_chassis_blocked = True
        chassis.save()
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print(form.errors)
        return super().form_invalid(form)


class BookingInvoiceUpdateView(mixins.HybridUpdateView):
    model = BookingInvoice
    form_class = BookingInvoiceUpdateFormTeamLead
    template_name = "crm/invoice_request_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:plan_pending_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Plan"
        context["is_delivar_plan"] = True
        return context


class InvoicePlanDetailView(mixins.HybridDetailView):
    model = BookingInvoice
    template_name = "crm/invoice_plan_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_details = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        invoice_discounts = InvoiceDiscount.objects.filter(invoice=invoice_details)
        context["invoice_details"] = invoice_details
        context["invoice_discounts"] = invoice_discounts
        context["invoice_request_view"] = True
        context["title"] = "Plan Details"
        return context


# testdriverequets_approve_by_testdrive_operator
class PendingTestDriveListView(mixins.HybridListView):
    model = TestDriveRequest
    table_class = tables.TestDriveRequestTable
    template_name = "crm/pending_testdrive_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(status__in=["pending", "scheduled", "rescheduled"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Pending Test Drive Requests"
        context["is_pending_testdrive_list"] = True
        return context


def testdrive_status_update(request, pk):
    crt_status = request.POST.get("status")
    testdrive_status = get_object_or_404(TestDriveRequest, pk=pk)
    testdrive_status.status = crt_status
    testdrive_status.save()
    return JsonResponse({"status": "success"})


class PendingTestDriveUpdateView(mixins.HybridUpdateView):
    model = TestDriveRequest
    form_class = TestDrivePendingUpdateForm
    template_name = "crm/testdrive_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:pending_testdrive_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Test Drive"
        return context


class InvoicediscountDetailView(mixins.HybridDetailView):
    model = InvoiceDiscount


class InvoiceDiscountCreateView(mixins.HybridFormView):
    template_name = "crm/invoice_accessory_and_discount_form.html"
    form_class = formset_factory(InvoiceDiscountForm, can_delete=True)

    def get_success_url(self):
        return reverse_lazy("crm:invoice_discount_create", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        discounts = InvoiceDiscount.objects.filter(invoice=invoice)
        context["invoice"] = invoice
        context["title"] = "Invoice Discount"
        context["table"] = tables.InvoiceDiscountTable(discounts)
        return context

    def get_form(self, form_class=None):
        formset = super().get_form(form_class)
        formset.extra = 1
        form_name = InvoiceDiscountForm.__name__.lower()
        formset.prefix = form_name
        return formset

    def form_valid(self, form):
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        formset = form
        for subform in formset:
            discount = subform.save(commit=False)
            discount.invoice = invoice
            discount.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        formset = form
        print("Formset errors:", formset.errors)
        print("Formset non-form errors:", formset.non_form_errors())
        return self.render_to_response(self.get_context_data(form=form))


class InvoiceDiscountUpdateView(mixins.HybridUpdateView):
    model = InvoiceDiscount
    exclude = ("is_active", "invoice", "stage")

    def get_success_url(self):
        invoice_discount = get_object_or_404(InvoiceDiscount, pk=self.kwargs["pk"])
        return reverse_lazy("crm:invoice_discount_create", kwargs={"pk": invoice_discount.invoice.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Invoice Discount"
        return context


class InvoiceAccessoryDetailView(mixins.HybridDetailView):
    model = InvoiceAccessory


class InvoiceAccessoryCreateVIew(mixins.HybridFormView):
    template_name = "crm/invoice_accessory_form.html"
    form_class = formset_factory(InvoiceAccessoryForm, can_delete=True)

    def get_success_url(self):
        return reverse_lazy("crm:invoice_accessory_create", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        accessorys = InvoiceAccessory.objects.filter(invoice=invoice)
        context["invoice"] = invoice
        context["title"] = "Invoice Accessory"
        context["table"] = tables.InvoiceAccessoryTable(accessorys)
        return context

    def get_form(self, form_class=None):
        formset = super().get_form(form_class)
        formset.extra = 1
        form_name = InvoiceAccessoryForm.__name__.lower()
        formset.prefix = form_name
        return formset

    def form_valid(self, form):
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        formset = form
        for subform in formset:
            discount = subform.save(commit=False)
            discount.invoice = invoice
            discount.save()
        return super().form_valid(form)


class InvoiceAccessoryUpdateView(mixins.HybridUpdateView):
    model = InvoiceAccessory
    exclude = ("is_active", "invoice", "stage")

    def get_success_url(self):
        invoice_accessory = get_object_or_404(InvoiceAccessory, pk=self.kwargs["pk"])
        return reverse_lazy("crm:invoice_accessory_create", kwargs={"pk": invoice_accessory.invoice.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Invoice accessory"
        return context


class PlanPendingListView(mixins.HybridListView):
    model = BookingInvoice
    filterset_fields = {
        "booking_request__opportunity__customer_name": ["icontains"],
        "invoice_no": ["icontains"],
        "invoice_date": ["lte"],
    }
    table_class = tables.PlanPendingTable

    def get_table_class(self):
        usertype = self.request.user.usertype
        if usertype not in ("team_lead", "asm", "sm", "gm"):
            return tables.InvoiceVeificationTable
        return self.table_class

    def get_queryset(self):
        dse_qs = User.objects.filter(branch__in=self.request.user.branch.all())
        print("===",dse_qs)
        qs = (
            super()
            .get_queryset()
            .filter(
                Q(exchange_status__in=("not_ok", "pending"))
                | Q(finance_status__in=("not_ok", "pending"))
                | Q(accessory_status__in=("not_ok", "pending"))
                | Q(scheme_status__in=("not_ok", "pending"))
                | Q(reg_status__in=("not_ok", "pending"))
                | Q(insurance_status__in=("not_ok", "pending"))
                | Q(discount_status__in=("not_ok", "pending"))
                | Q(accounts_status__in=("not_ok", "pending"))
                | Q(pdi_status__in=("not_ok", "pending")),
                status="plan_pending",
            )
        )
        print("qs===",qs)
        usertype = self.request.user.usertype
        if usertype == "finance_bo":
            qs = qs.filter(finance_status__in=("pending", "not_ok"))
        elif usertype == "exchange_bo":
            qs = qs.filter(exchange_status__in=("pending", "not_ok"))
        elif usertype == "registration_bo":
            qs = qs.filter(reg_status__in=("pending", "not_ok"))
        elif usertype == "scheme":
            qs = qs.filter(scheme_status__in=("pending", "not_ok"))
        elif usertype == "insurance":
            qs = qs.filter(insurance_status__in=("pending", "not_ok"))
        elif usertype == "pdi":
            qs = qs.filter(pdi_status__in=("pending", "not_ok"))
        elif usertype == "tmga":
            qs = qs.filter(accessory_status__in=("pending", "not_ok"))
        elif usertype == "gm":
            qs = qs.filter(status="plan_pending")
        else:
            qs = qs.filter(booking_request__opportunity__dse__in=dse_qs, status="plan_pending")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Plan Pending"
        context["is_plan_pending_list"] = True
        return context


class SaleSupportListView(mixins.HybridListView):
    model = BookingInvoice
    filterset_fields = {"booking_request__opportunity__customer_name": ["icontains"]}
    table_class = tables.SaleSupportTable

    def get_queryset(self):
        usertype = self.request.user.usertype
        qs = super().get_queryset()
        if usertype in ("asm", "sm"):
            dse_qs = User.objects.filter(branch__in=self.request.user.branch.all())
            qs = qs.filter(booking_request__opportunity__dse__in=dse_qs,status="plan_pending", discount_status="pending")
        elif usertype == "gm":
            qs = qs.filter(status="plan_pending", discount_status="forward")
        return qs


class PlanAccountsListView(mixins.HybridListView):
    model = BookingInvoice
    filterset_fields = {"booking_request__opportunity__customer_name": ["icontains"]}
    table_class = tables.PlanAccountsTable

    def get_queryset(self):
        return super().get_queryset().filter(accounts_status="pending", status="plan_pending")


class InvoiceDocumentUpdateView(mixins.HybridUpdateView):
    model = BookingInvoice
    fields = ('booking_request',)
    template_name = 'crm/invoice_document_form.html'
    

    def get_success_url(self):
        return reverse_lazy('crm:plan_pending_list')


    def get_invoice_document_formset(self, department, documents):
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs['pk'])
        # Get the documents related to the specific department
        department_documents = Document.objects.filter(department=department)
        
        # Dynamically set the choices for the document field
        choices = [(doc.id, doc.name) for doc in department_documents]
        
        # Set the choices for the document field in the formset
        formset = InvoiceDocumentFormset(
            self.request.POST or None,
            self.request.FILES or None,
            queryset=documents.filter(document__department=department),
            prefix=f'invoice_documents_{department}',
            instance=invoice
        )
        formset.forms[0].fields['document'].queryset = department_documents
        
        return formset
            

    # Updated get_context_data method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs['pk'])
        documents = InvoiceDocument.objects.filter(invoice=invoice, is_active=True)
        context['invoice'] = invoice
        context["title"] = "Invoice Documents Upload"
        context['table'] = tables.InvoiceDocumentTable(documents)
        departments = ['registration', 'scheme', 'exchange']
        for department in departments:
            formset_name = f'invoice_documents_formset_{department}'
            context[formset_name] = self.get_invoice_document_formset(department, documents)

        return context

    # Revised form_valid method
    def form_valid(self, form):
        context = self.get_context_data()
        
        for department in ['registration', 'scheme', 'exchange']:
            formset_name = f'invoice_documents_formset_{department}'
            invoice_documents_formset = context[formset_name]

            if not invoice_documents_formset.is_valid():
                return self.form_invalid(form)

        for department in ['registration', 'scheme', 'exchange']:
            formset_name = f'invoice_documents_formset_{department}'
            invoice_documents_formset = context[formset_name]
            invoice_documents_formset.instance = self.get_object()            
            invoice_documents_formset.save()

        return super().form_valid(form)


class BaseInvoiceStatusUpdateView(mixins.HybridUpdateView):
    model = BookingInvoice
    template_name = "crm/invoice_status_update_form.html"
    success_url_name = None
    title = None
    document_table = None
    accessory_table = None
    discount_table = None
    fields = ()

    def get_success_url(self):
        if self.success_url_name:
            return reverse_lazy(self.success_url_name)
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        documents = InvoiceDocument.objects.filter(invoice=invoice, is_active=True)
        if self.request.user.usertype == "registration_bo":
            documents = documents.filter(document__department="registration")
        elif self.request.user.usertype == "scheme":
            documents = documents.filter(document__department="scheme")
        elif self.request.user.usertype == "exchange_bo":
            documents = documents.filter(document__department="exchange")
        context["invoice"] = invoice
        context["table"] = tables.InvoiceDocumentTable(documents)

        usertype = self.request.user.usertype

        if self.document_table:
            document_objects = self.document_table.objects.filter(invoice=invoice)
            context["document_table"] = self.document_table(document_objects)

        if self.accessory_table:
            accessory_objects = InvoiceAccessory.objects.filter(invoice=invoice)
            context["accessory"] = self.accessory_table(accessory_objects)

        if self.discount_table:
            discount_objects = InvoiceDiscount.objects.filter(invoice=invoice)
            if usertype == "gm":
                allowed_statuses = ["escalate", "approve", "reject"]
                discount_objects = discount_objects.filter(discount_status__in=allowed_statuses)
            elif usertype == "accounts":
                allowed_statuses = ["approve"]
                discount_objects = discount_objects.filter(discount_status__in=allowed_statuses)
            context["discounts"] = self.discount_table(discount_objects)

        return context

    def form_valid(self, form):
        self.object.plan_ok_date = date.today()
        return super().form_valid(form)


class FinanceStatusUpdateView(BaseInvoiceStatusUpdateView):
    fields = (
        "finance",
        "branch",
        "loan_amount",
        "loan_amount_receipt_no",
        "loan_amount_receipt_date",
        "executive",
        "payout",
        "upload_finance_letter",
        "finance_status",
        "finance_remarks",
    )
    success_url_name = "crm:plan_pending_list"
    title = "Finance Status Update"


class ExchangeStatusUpdateView(BaseInvoiceStatusUpdateView):
    fields = (
        "exchange_vehicle_make",
        "exchange_vehicle_model",
        "exchange_reg_no",
        "exchange_mfg_year",
        "owner_name",
        "relation",
        "exchange_vehicle_status",
        "old_car_purchase_value",
        "exchange_bonus",
        "deduction_remarks",
        "total_value_to_new_car",
        "exchange_campaign_code",
        "tml_share",
        "dealer_share",
        "total_eligible_bonus",
        "exchange_status",
        "exchange_remarks",
    )
    success_url_name = "crm:plan_pending_list"
    title = "Exchange Status Update"
    template_name = "crm/exchange_status_update_form.html"

class RegistrationStatusUpdateView(BaseInvoiceStatusUpdateView):
    fields = ("reg_type", "any_tax_exemption", "tax_remarks", "rto", "reg_status", "reg_remarks")
    success_url_name = "crm:plan_pending_list"
    title = "RTO Status Update"


class SchemeStatusUpdateView(BaseInvoiceStatusUpdateView):
    fields = (
        "scheme",
        "scheme_name",
        "scheme_campaign_code",
        "institution_name",
        "amount",
        "yono_scheme_amount",
        "yono_scheme_status",
        "yono_scheme_remark",
        "scheme_status",
        "scheme_remark",
    )
    success_url_name = "crm:plan_pending_list"
    title = "Scheme Status Update"
    template_name = "crm/scheme_status_update_form.html"


class InsuranceStatusUpdateView(BaseInvoiceStatusUpdateView):
    fields = (
        "insurance_type",
        "ncb_eligibility",
        "ncb_percentage",
        "any_other_discount",
        "insurance_amount",
        "nominee_name",
        "nominee_relation",
        "insurance_status",
        "insurance_remarks",
    )
    success_url_name = "crm:plan_pending_list"
    title = "Insurance Status Update"


class PdiStatusUpdateView(BaseInvoiceStatusUpdateView):
    fields = ("front_image","rear_image","rh_image","lh_image","engine_room","suggested_delivery_date","pdi_status", "pdi_remarks")
    success_url_name = "crm:plan_pending_list"
    title = "PDI Status Update"


class AccessoryStatusUpdateView(BaseInvoiceStatusUpdateView):
    fields = ("accessory_status", "accessory_remarks")
    success_url_name = "crm:plan_pending_list"
    title = "Accessory Status Update"
    accessory_table = tables.InvoiceAccessoryTable
    discount_table = tables.InvoiceDiscountTable


class DiscountStatusUpdateView(BaseInvoiceStatusUpdateView):
    fields = ("discount_status", "discount_remarks")
    success_url_name = "crm:sale_support_list"
    title = "Discount Status Update"
    discount_table = tables.InvoiceDiscountTable


class AccountsStatusUpdateView(BaseInvoiceStatusUpdateView):
    form_class = AccountsTeamInvoiceUpdateForm
    success_url_name = "crm:plan_accounts"
    title = "Accounts Status Update"
    template_name = "crm/invoice_accounts_verification_form.html"
    fields = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        context["accessories"] = InvoiceAccessory.objects.filter(invoice=invoice, is_active=True)
        context["topups"] = InvoiceTopUp.objects.filter(invoice=invoice, is_active=True)
        context["invoice_topup_formset"] = INVOICETOPUPFORMSET(
            self.request.POST or None, prefix="topup", instance=self.object
        )
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["booking_amount"].initial = self.object.booking_request.order_amount
        return form

    def form_valid(self, form):
        context = self.get_context_data()
        invoice_topup_formset = context["invoice_topup_formset"]
        booking_amount = form.cleaned_data["booking_amount"]
        booking_req = self.object.booking_request
        booking_req.order_amount = booking_amount
        booking_req.save()
        if invoice_topup_formset.is_valid():
            self.object = form.save()

            invoice_topup_formset.instance = self.object

            invoice_topup_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class DeliveryPendingListView(mixins.HybridListView):
    model = BookingInvoice
    table_class = tables.DeliveryPendingTable
    filterset_fields = {"customer_name": ["icontains"]}
    template_name = "crm/delivary_pending_list.html"
    
    
    def get_queryset(self):
        usertype = self.request.user.usertype
        queryset = super().get_queryset().filter(
            status="plan_pending",
            exchange_status="ok",
            finance_status="ok",
            accessory_status="ok",
            scheme_status="ok",
            reg_status="ok",
            insurance_status="ok",
            discount_status="ok",
            accounts_status="ok",
            pdi_status="ok",
        )
        
        if usertype in ["asm", "sm", "customer_advisor", "team_lead"]:
            dse_qs = User.objects.filter(branch__in=self.request.user.branch.all())
            queryset = queryset.filter(booking_request__opportunity__dse__in=dse_qs)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delivery Pending"
        context["is_delivary_pending_list"] = True
        context['document_upload_form'] = DocumentUploadForm(self.request.POST or None , self.request.FILES or None)
        return context

class DocumentUploadAccountsTeamView(mixins.HybridView):
    def post(self, request, *args, **kwargs):
        # Handle the POST request here
        form_type = request.POST.get('form_type')  # Assuming a form_type field in your HTML form
        form = DocumentUploadForm(request.POST, request.FILES)
        print('form_type=',form_type)
        if form.is_valid():
            print('valid==========')
            invoice_id = request.POST.get('invoice_id')
            print('vavalidlid==========',invoice_id)
            invoice = get_object_or_404(BookingInvoice, pk=invoice_id)
            doc = form.cleaned_data.get('document')
            redirect_link = 'crm:delivary_pending_list'
            if form_type in ('signed_invoice_upload','signed_settlement_upload','delivary_photo_upload','signed_gate_pass_upload'):
                redirect_link = 'crm:delivered_list'
            if form_type == 'invoice_upload':
                invoice.invoice = doc
            elif form_type == 'settlement_upload':
                invoice.settlement = doc
            elif form_type == 'receipts_upload':
                invoice.receipts = doc
            elif form_type == 'form20_upload':
                invoice.form20 = doc
            elif form_type == 'disclimer_upload':
                invoice.disclimer = doc
            elif form_type == 'undertaking_upload':
                invoice.under_taking_letter = doc
            elif form_type == 'accessory_bill_upload':
                invoice.accessory_bill = doc
            
            elif form_type == 'signed_form20_upload':
                invoice.signed_form20 = doc
            elif form_type == 'signed_disclimer_upload':
                invoice.signed_disclimer = doc
            elif form_type == 'signed_undertaking_upload':
                invoice.signed_under_taking_letter = doc
                
            elif form_type == 'signed_invoice_upload':
                invoice.signed_invoice = doc
            elif form_type == 'signed_settlement_upload':
                invoice.signed_settlement = doc
            elif form_type == 'delivary_photo_upload':
                invoice.delivary_photo = doc
            elif form_type == 'signed_gate_pass_upload':
                invoice.signed_gate_pass = doc
            invoice.save()
        return redirect(redirect_link)

class DeliveredListView(mixins.HybridListView):
    model = BookingInvoice
    table_class = tables.DeliveredTable
    filterset_fields = {"booking_request__opportunity__customer_name": ["icontains"]}
    template_name = "crm/delivered_list.html"
    
    def get_queryset(self):
        usertype = self.request.user.usertype
        queryset = super().get_queryset().filter(status="delivered")

        if usertype in ["asm", "sm", "customer_advisor", "team_lead"]:
            dse_qs = User.objects.filter(branch__in=self.request.user.branch.all())
            queryset = queryset.filter(booking_request__opportunity__dse__in=dse_qs)

        return queryset


    def get_table_class(self):
        usertype = self.request.user.usertype
        if usertype  in ["cre",]:
            return tables.DeliveredFollowupTable
        return self.table_class


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delivered"
        context["is_delivered_list"] = True
        context['document_upload_form'] = DocumentUploadForm(self.request.POST or None , self.request.FILES or None)
        return context


class RegistrationRemarkCreateView(mixins.HybridCreateView):
    model = RegistrationRemark
    exclude = ("is_active", "invoice")

    def form_valid(self, form):
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        form.instance.invoice = invoice
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("crm:delivary_pending_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Remarks"
        return context


class InvoiceAccessoryListView(mixins.HybridListView):
    model = InvoiceAccessory
    table_class = tables.InvoiceAccessoryTable
    filterset_fields = {"invoice": ["exact"]}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Accessories"
        return context


class GatepassView(PDFView):
    template_name = "crm/gatepass2.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        invoice = get_object_or_404(BookingInvoice, pk=pk)
        context = super().get_context_data(**kwargs)
        context["object"] = invoice
        return context


# class JobcardView(PDFView):
#     template_name = 'crm/job_card.html'

#     def get_context_data(self, **kwargs):
#         pk = self.kwargs.get('pk')
#         accessory_job_cards = InvoiceAccessory.objects.filter(invoice__pk=pk)
#         job_details = get_object_or_404(InvoiceAccessory, pk=pk)
#         print(accessory_job_cards)
#         context = super().get_context_data(**kwargs)
#         context["object_list"] = accessory_job_cards
#         context["object_details"] = job_details
#         return context


class JobcardView(PDFView):
    template_name = "crm/job_card.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        invoice = get_object_or_404(BookingInvoice, pk=pk)
        accessory_job_cards = InvoiceAccessory.objects.filter(invoice=invoice)
        context = super().get_context_data(**kwargs)
        context["object_list"] = accessory_job_cards
        context["object_details"] = invoice
        return context


class UpdatetoDeliverd(BaseInvoiceStatusUpdateView):
    fields = ("status",)
    success_url_name = "crm:delivary_pending_list"
    title = "Update Status"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["status"].choices = [("delivered", "Delivered")]
        return form
    
    def form_valid(self, form):
        # Set the vehicle_delivered_date field in the BookingInvoice model
        self.object.vehicle_delivered_date = form.cleaned_data.get("vehicle_delivered_date", date.today())
        return super().form_valid(form)




class InvoiceRejectedListView(mixins.HybridListView):
    model = BookingInvoice
    table_class = tables.InvoiceRejectUpdateTable
    filterset_fields = {"booking_request__opportunity__customer_name": ["icontains"]}

    def get_queryset(self):
        user = self.request.user
        if user.usertype in ("team_lead", "asm", "sm", "finance_executive"):
            dse_qs = User.objects.filter(branch__in=user.branch.all())
            qs = (
                super()
                .get_queryset()
                .filter(
                    booking_request__opportunity__dse__in=dse_qs,
                    status__in=["rejected_stock_team", "rejected_invoice_team", "requested"],
                )
            )
        else:
            qs = super().get_queryset()

        return qs

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Invoices Requests"
        context["is_rejected_invoices"] = True
        return context


class InvoiceRejectedUpdateView(mixins.HybridUpdateView):
    model = BookingInvoice
    form_class = BookingInvoiceForm
    template_name = "crm/invoice_request_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_request = get_object_or_404(BookingRequest, pk=self.kwargs["pk"])
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
        context["title"] = "Invoice Request Update"
        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.fields["state"].initial = self.object.district.state if self.object.district else None
        form.fields["car_model"].initial = self.object.chassis.variant.car_model
        form.fields["trim"].initial = self.object.chassis.variant.trim
        form.fields["color"].initial = self.object.chassis.variant.color
        form.fields["variant"].initial = self.object.chassis.variant
        form.fields["opt_id"].initial = self.object.booking_request.opportunity.opt_id
        form.fields["booking_no"].initial = self.object.booking_request.order_no
        form.fields["booking_date"].initial = self.object.booking_request.order_date
        return form

    def get_success_url(self):
        return reverse_lazy("crm:invoice_rejected_list")

    def form_valid(self, form):
        print(form.errors)
        current_status = self.object.status

        # Check the current status and set the new status accordingly
        if current_status == "rejected_stock_team":
            form.instance.status = "requested"
        elif current_status == "rejected_invoice_team":
            form.instance.status = "alloted"

        chassis = form.instance.chassis
        chassis.is_chassis_blocked = True
        chassis.save()

        return super().form_valid(form)


# seprate-discount-approval


def each_discount_status_update(request, pk):
    crt_status = request.POST.get("status")
    each_discount_status = get_object_or_404(InvoiceDiscount, pk=pk)
    each_discount_status.discount_status = crt_status
    each_discount_status.save()
    return JsonResponse({"status": "success"})


class BookingInvoiceDocumentCreateVIew(mixins.HybridUpdateView):
    model = BookingInvoice
    template_name = "crm/booking_invoice_document_form.html"
    fields = ("booking_request",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        documents = BookingInvoiceDocument.objects.filter(is_active=True, invoice=invoice)
        if self.request.user.usertype == "accounts":
            documents.filter(user__usertype="accounts")
        elif self.request.user.usertype == "registration_bo":
            documents.filter(user__usertype="registration_bo")
        context["invoice"] = invoice
        context["booking_invoice_document_table"] = tables.BookingInvoiceDocumentTable(documents)
        context["title"] = "Add Documents"
        context["booking_invoice_document_formset"] = BOOKINGINVOICEDOCUMENTFORMSET(
            self.request.POST or None,
            self.request.FILES or None,
            instance=invoice,
            queryset=documents,
            prefix="booking_invoice_document_formset",
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        booking_invoice_document_formset = context["booking_invoice_document_formset"]
        if booking_invoice_document_formset.is_valid():
            booking_invoice_document_formset.instance = self.get_object()
            for form in booking_invoice_document_formset:
                form.instance.user = self.request.user
            booking_invoice_document_formset.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class BookingInvoiceDocumentUpdateView(mixins.HybridUpdateView):
    model = BookingInvoiceDocument
    exclude = ("is_active", "invoice", "user")

    def get_success_url(self):
        return reverse_lazy("crm:booking_invoice_document_create", kwargs={"pk": self.object.invoice.pk})


class BookingInvoiceDocumentDeleteView(mixins.HybridDeleteView):
    model = BookingInvoiceDocument

    def get_success_url(self):
        return reverse_lazy("crm:booking_invoice_document_create", kwargs={"pk": self.object.invoice.pk})



class DailyReportCreateView(mixins.HybridCreateView):
    model = DailyReport
    
    form_class = DailyReportForm

    def get_form(self, *args, **kwargs):
        # TODO: Filter qs by usertype
        form = super().get_form(*args, **kwargs)
        if self.request.user.usertype == "team_lead":
            form.fields["customer_advisor"].queryset = User.objects.filter(
                branch__in=self.request.user.branch.all(), usertype="customer_advisor"
            )
        elif self.request.user.usertype == "customer_advisor":
            form.fields["customer_advisor"].initial = self.request.user
            form.fields["customer_advisor"].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Daily Report Entry"
        context["is_opportunity_entry"] = True
        return context

class DailyReportListView(mixins.HybridListView):
    model = DailyReport
    table_class = tables.DailyReportTable
    filterset_fields = {"created": ["lte"],}
    template_name = "crm/opportunity_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Daily Report"
        context["is_daily_report"] = True
        context["can_add"] = True
        context["new_link"] = reverse_lazy("crm:daily_report_create")
        return context
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.usertype == "team_lead":
            dse_qs = User.objects.filter(branch__in=self.request.user.branch.all())
            qs = qs.filter(customer_advisor__in=dse_qs)
        elif self.request.user.usertype == "customer_advisor":
            qs = qs.filter(customer_advisor=self.request.user)

        return qs
    

class AfterDeliveryFollowupCreateView(mixins.HybridCreateView):
    model = AfterDeliveryFollowup
    template_name = "crm/after_delivery_followup.html"
    form_class = AfterDeliveryFollowUpForm
    

    def get_success_url(self):
        return reverse_lazy("crm:delivered_followup_create", kwargs={"pk": self.kwargs["pk"]})


    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        bkng_invoice = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        
        form.fields["dse"].initial = bkng_invoice.dse
        form.fields["customer_name"].initial = bkng_invoice.customer_name
        form.fields["mobile"].initial = bkng_invoice.mobile
        form.fields["vehicle_delivered_date"].initial = bkng_invoice.vehicle_delivered_date
        form.fields["email"].initial = bkng_invoice.email
        
        return form



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        followups = AfterDeliveryFollowup.objects.filter(invoice=invoice, is_active=True)
        context["invoice"] = invoice
        context["followups"] = tables.AfterDeliveryFollowupTable(followups)
        context["title"] = "After Delivery Followup Create"
        return context

    def form_valid(self, form):
        invoice = get_object_or_404(BookingInvoice, pk=self.kwargs["pk"])
        form.instance.invoice = invoice
        return super().form_valid(form)



class AfterDeliveryFollowupPrintView(PDFView):
    template_name = "crm/aftr_dl_followup_pdf.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        after_delivery = get_object_or_404(AfterDeliveryFollowup, pk=pk)
        context = super().get_context_data(**kwargs)
        context["object"] = after_delivery
        return context
    

class DigitalLeadEnquiryCreateView(mixins.HybridCreateView):
    model = DigitalLeadEnquiry
    form_class = DigitalLeadEnquiryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Digital Lead Entry"
        context["is_digital_lead_entry"] = True
        return context



class DigitalLeadEnquiryListView(mixins.HybridListView):
    model = DigitalLeadEnquiry
    table_class = tables.DigitalLeadEnquiryTable
    filterset_fields = {"created": ["lte"],}
    template_name = "crm/opportunity_list.html"

    def get_queryset(self):
        usertype = self.request.user.usertype
        queryset = super().get_queryset()
        if usertype == "team_lead":
            queryset = queryset.filter(assigned_to=self.request.user)
        return queryset

    def get_table_class(self):
        usertype = self.request.user.usertype
        if usertype  in ["team_lead",]:
            return tables.DigitalLeadEnquiryTeamLeadTable
        return self.table_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Digital Lead"
        context["is_digital_lead"] = True
        context["can_add"] = True
        context["new_link"] = reverse_lazy("crm:digital_leads_create")
        return context
    

class DigitalLeadFollowUpCreateView(mixins.HybridCreateView):
    model = DigitalLeadFollowUp
    exclude = ("is_active", "digital_lead")
    template_name = "crm/digitallead_followup_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:digital_leads_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        digital_lead = get_object_or_404(DigitalLeadEnquiry, pk=self.kwargs["pk"])
        followups = DigitalLeadFollowUp.objects.filter(digital_lead=digital_lead)
        context["opportunity"] = digital_lead
        context["title"] = "Digital Lead Follow Up"
        context["followups"] = tables.DigitalLeadFollowUpTable(followups)
        return context

    def form_valid(self, form):
        digital_lead = get_object_or_404(DigitalLeadEnquiry, pk=self.kwargs["pk"])
        form.instance.digital_lead = digital_lead  # Set the foreign key
        return super().form_valid(form)
    

class DigitalLeadLostCreateView(mixins.HybridCreateView):
    form_class = DigitalLeadLostForm
    template_name = "crm/digital_lead_lost_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:digital_leads_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        digital_lead = get_object_or_404(DigitalLeadEnquiry, pk=self.kwargs["pk"])
        opt_lost = DigitalLeadEnquiryLost.objects.filter(digital_lead=digital_lead, is_active=True)
        context["opportunity"] = digital_lead
        context["opt_lost"] = tables.DigitalLeadEnquiryLostTable(opt_lost)

        return context

    def form_valid(self, form):
        digital_lead = get_object_or_404(DigitalLeadEnquiry, pk=self.kwargs["pk"])
        form.instance.digital_lead = digital_lead  
        digital_lead.stage = "lead_lost"
        digital_lead.save()

        return super().form_valid(form)
    


class EventReportListView(mixins.HybridListView):
    model = EventReport
    table_class = tables.EventReportTable
    filterset_fields = {"created": ["lte"],}
    template_name = "crm/opportunity_list.html"

    def get_queryset(self):
        usertype = self.request.user.usertype
        queryset = super().get_queryset()
        if usertype == "customer_advisor":
            queryset = queryset.filter(responsible_ca=self.request.user)
        elif usertype == "team_lead":
            dse_qs = User.objects.filter(branch__in=self.request.user.branch.all())
            queryset = queryset.filter(responsible_ca__in=dse_qs)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Event Report"
        context["is_event_report"] = True
        context["can_add"] = True
        context["new_link"] = reverse_lazy("crm:event_report_create")
        return context

class EventReportCreateView(mixins.HybridCreateView):
    model = EventReport
    form_class = EventReportForm

    def get_form(self, *args, **kwargs):
        # TODO: Filter qs by usertype
        form = super().get_form(*args, **kwargs)
        if self.request.user.usertype == "team_lead":
            form.fields["responsible_ca"].queryset = User.objects.filter(
                branch__in=self.request.user.branch.all(), usertype="customer_advisor"
            )
        elif self.request.user.usertype == "customer_advisor":
            form.fields["responsible_ca"].initial = self.request.user
            form.fields["responsible_ca"].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Event Report Entry"
        context["is_event_entry"] = True
        return context

class EventReportUpdateView(mixins.HybridUpdateView):
    model = EventReport
    form_class = EventReportForm

    def get_form(self, *args, **kwargs):
        # TODO: Filter qs by usertype
        form = super().get_form(*args, **kwargs)
        if self.request.user.usertype == "team_lead":
            form.fields["responsible_ca"].queryset = User.objects.filter(branch__user=self.request.user, usertype="customer_advisor")
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = " Edit Event"
        return context
    

class EventPhotoUploadCreateView(mixins.HybridCreateView):
    model = EventPhoto
    exclude = ("is_active", "event")
    template_name = "crm/event_photo_form.html"

    def get_success_url(self):
        return reverse_lazy("crm:event_report_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_report = get_object_or_404(EventReport, pk=self.kwargs["pk"])
        followups = EventPhoto.objects.filter(event=event_report)
        context["opportunity"] = event_report
        context["title"] = "Digital Lead Follow Up"
        context["followups"] = tables.EventPhotoTable(followups)
        return context

    def form_valid(self, form):
        event = get_object_or_404(EventReport, pk=self.kwargs["pk"])
        form.instance.event = event  # Set the foreign key
        return super().form_valid(form)
    

class EventCustomerDetailsCreateView(mixins.HybridCreateView):
    model = EventCustomerDetails
    exclude = ("is_active", "event")
    template_name = "crm/event_customer_detail_form.html"
    filterset_fields = {"enquiry_status": ["exact"],}

    def get_success_url(self):
        return reverse_lazy("crm:event_customer_details_create", kwargs={"pk": self.object.event.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Get the related EventReport
        event = get_object_or_404(EventReport, pk=self.kwargs["pk"])
        # Set the initial value for ca_name field
        form.fields['ca_name'].initial = event.responsible_ca
        # Make ca_name field read-only
        form.fields['ca_name'].widget.attrs['readonly'] = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_cust_details = get_object_or_404(EventReport, pk=self.kwargs["pk"])
        followups = EventCustomerDetails.objects.filter(event=event_cust_details)
        context["opportunity"] = event_cust_details
        context["title"] = "Event Customer Details"
        context["followups"] = tables.EventCustomerDetailsTable(followups)
        return context

    def form_valid(self, form):
        event = get_object_or_404(EventReport, pk=self.kwargs["pk"])
        form.instance.event = event  # Set the foreign key
        return super().form_valid(form)