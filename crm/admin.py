from .models import AfterDeliveryFollowup, BackOrder, BookingInvoiceDocument, DailyReport, DigitalLeadEnquiryLost, DigitalLeadFollowUp, EventCustomerDetails, EventPhoto, EventReport, InvoiceTopUp
from .models import BookingFollowUp
from .models import BookingInvoice
from .models import BookingRequest
from .models import Opportunity,DigitalLeadEnquiry
from .models import OpportunityFollowUp, ChassisBlock
from .models import OpportunityLost, BookingLost
from .models import TestDriveRequest
from .models import InvoiceAccessory
from .models import InvoiceDiscount
from .models import InvoiceDocument
from .models import RegistrationRemark
from django.contrib import admin
from core.base import BaseAdmin


@admin.register(BookingInvoiceDocument)
class BookingInvoiceDocumentAdmin(BaseAdmin):
    list_display = ("invoice", "user", "document_name", "document")


@admin.register(RegistrationRemark)
class RegistrationRemarkAdmin(BaseAdmin):
    list_display = ("invoice", "remark", "is_active")


@admin.register(InvoiceDocument)
class InvoiceDocumentAdmin(BaseAdmin):
    list_display = ("invoice", "document", "is_active")
    list_filter = ("document",)
    search_fields = ("invoice__customer_name",)


@admin.register(InvoiceDiscount)
class InvoiceDiscountAdmin(BaseAdmin):
    list_display = ("invoice", "discount", "amount", "is_active")
    list_filter = ("discount",)
    search_fields = ("discount__discount_name",)


@admin.register(InvoiceTopUp)
class InvoiceTopUpAdmin(BaseAdmin):
    list_display = ("invoice",)
    list_filter = ("invoice",)
    search_fields = ("invoice",)


@admin.register(InvoiceAccessory)
class InvoiceAccessoryAdmin(BaseAdmin):
    list_display = ("invoice", "accessory_name", "payment_type", "amount", "is_active")
    list_filter = ("payment_type",)
    search_fields = ("accessory_name",)


@admin.register(Opportunity)
class OpportunityAdmin(BaseAdmin):
    list_display = ("customer_name", "profession", "phone", "is_active")
    list_filter = ("is_active",)
    search_fields = ("customer_name",)
    ordering = ("customer_name",)


@admin.register(OpportunityFollowUp)
class OpportunityFollowUpAdmin(BaseAdmin):
    list_display = ["opportunity", "followup_date", "followup_via", "opt_status"]
    search_fields = ["opportunity__customer_name"]
    list_filter = ["followup_date", "opt_status"]


@admin.register(TestDriveRequest)
class TestDriveRequestAdmin(BaseAdmin):
    list_display = ["opportunity", "preferred_date"]
    search_fields = ["opportunity__customer_name"]
    list_filter = ["preferred_date"]


@admin.register(OpportunityLost)
class OpportunityLostAdmin(BaseAdmin):
    list_display = ["opportunity", "reason", "remarks"]
    search_fields = ["opportunity__customer_name"]
    list_filter = ["reason"]


@admin.register(BookingRequest)
class BookingRequestAdmin(BaseAdmin):
    list_display = ["opportunity", "order_no", "order_date", "order_time", "order_amount"]
    search_fields = ["opportunity__customer_name"]


@admin.register(BookingFollowUp)
class BookingFollowUpAdmin(BaseAdmin):
    list_display = ["booking_request", "booking_followup_date", "booking_status", "exp_delivery_date"]
    search_fields = ["booking_request__opportunity__customer_name"]


@admin.register(BackOrder)
class BackOrderAdmin(BaseAdmin):
    list_display = ["booking_request", "back_order_need", "remarks"]
    search_fields = ["booking_request__opportunity__customer_name"]


@admin.register(ChassisBlock)
class ChassisBlockAdmin(BaseAdmin):
    list_display = ["booking_request", "variant", "stock"]
    search_fields = ["booking_request__opportunity__customer_name"]


@admin.register(BookingInvoice)
class BookingInvoiceAdmin(BaseAdmin):
    list_display = ["booking_request", "invoice_no", "status"]
    search_fields = ["booking_request__opportunity__customer_name"]


@admin.register(BookingLost)
class BookingLostAdmin(BaseAdmin):
    list_display = ["booking_request", "reason", "remarks"]
    search_fields = ["booking_request__opportunity__customer_name"]
    list_filter = ["reason"]


@admin.register(AfterDeliveryFollowup)
class AfterDeliveryFollowupAdmin(BaseAdmin):
    list_display = [ "invoice"]
   
@admin.register(DailyReport)
class DailyReportAdmin(BaseAdmin):
    list_display = ["customer_name", "phone"]


@admin.register(DigitalLeadEnquiry)
class DigitalLeadEnquiryAdmin(BaseAdmin):
    list_display = ["customer_name", "phone_1"]


@admin.register(DigitalLeadFollowUp)
class DigitalLeadFollowUpAdmin(BaseAdmin):
    list_display = ["digital_lead", "followup_date","opt_status"]

@admin.register(DigitalLeadEnquiryLost)
class DigitalLeadEnquiryLostAdmin(BaseAdmin):
    list_display = ["digital_lead", "reason","sub_reason","remarks"]

@admin.register(EventReport)
class EventReportAdmin(BaseAdmin):
    list_display = ["event_id", "event_date","event_location"]

@admin.register(EventPhoto)
class EventPhotoAdmin(BaseAdmin):
    list_display = ["event",]

@admin.register(EventCustomerDetails)
class EventCustomerDetailsAdmin(BaseAdmin):
    list_display = ["customer_name","phone",]
