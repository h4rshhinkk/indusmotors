from core.choices import ENQUIRY_TYPE, SELECTION_CHOICES, SELECTION_CHOICES_FINANCE
from crm.models import BackOrder
from crm.models import BookingInvoice
from crm.models import BookingRequest
from crm.models import ChassisBlock
from crm.models import OpportunityFollowUp
from crm.models import OpportunityLost, BookingLost
from masters.models import CarModel, Variant
from masters.models import Color
from masters.models import LostReason
from masters.models import Trim, Profession
from masters.models import State, District
from accounts.models import User
from .models import (
    AfterDeliveryFollowup,
    BookingFollowUp,
    BookingInvoiceDocument,
    DailyReport,
    DigitalLeadEnquiry,
    DigitalLeadEnquiryLost,
    EventReport,
    InvoiceAccessory,
    InvoiceDiscount,InvoiceDocument,
    InvoiceTopUp,
    Opportunity,
)
from .models import TestDriveRequest
from django import forms
from django.forms import inlineformset_factory


class OpportunityForm(forms.ModelForm):
    car_model = forms.ModelChoiceField(
        queryset=CarModel.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Car Model",
    )
    trim = forms.ModelChoiceField(
        queryset=Trim.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False, label="Trim"
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Color",
    )
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="State",
    )

    class Meta:
        model = Opportunity
        fields = (
            "opt_date",
            "opt_id",
            "opportunity_source",
            "dse",
            "customer_salutation",
            "customer_name",
            "guardian_salutation",
            "guardian_name",
            "address",
            "place",
            "state",
            "district",
            "mobile",
            "phone",
            "email",
            "dob",
            "profession",
            "profession_detail",
            "opt_type",
            "exchange_vehicle_make",
            "exchange_vehicle_model",
            "exchange_reg_no",
            "exchange_mfg_year",
            "owner_name",
            "relation",
            "opt_status",
            "next_followup_date",
            "car_model",
            "trim",
            "color",
            "variant",
        )
        exclude = ("stage",)


class OpportunityFollowUpFormFinanceExecutive(forms.ModelForm):
    class Meta:
        model = OpportunityFollowUp
        fields = ("finance_executive_status", "finance_executive_remark")


class BookingFollowUpFormFinanceExecutive(forms.ModelForm):
    class Meta:
        model = BookingFollowUp
        fields = ("finance_executive_status", "finance_executive_remark")


class TestDriveRequestForm(forms.ModelForm):
    car_model = forms.ModelChoiceField(
        queryset=CarModel.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Car Model",
    )
    trim = forms.ModelChoiceField(
        queryset=Trim.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False, label="Trim"
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Color",
    )

    class Meta:
        model = TestDriveRequest
        fields = ("car_model", "trim", "color", "variant", "preferred_date", "preferred_time")


class TestDrivePendingUpdateForm(forms.ModelForm):
    class Meta:
        model = TestDriveRequest
        fields = (
            "preferred_date",
            "preferred_time",
            "starting_km",
            "end_km",
            "testdrive_given_by",
            "remarks",
            "status",
        )


class OpportunityLostForm(forms.ModelForm):
    class Meta:
        model = OpportunityLost
        fields = ("reason", "sub_reason", "remarks")


class BookingRequestForm(forms.ModelForm):
    car_model = forms.ModelChoiceField(
        queryset=CarModel.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Car Model",
    )
    trim = forms.ModelChoiceField(
        queryset=Trim.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False, label="Trim"
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Color",
    )
    opt_id = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    dse = forms.ModelChoiceField(
        queryset=User.objects.filter(usertype="customer_advisor"),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="DSE",
    )
    customer_salutation = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    customer_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    mobile = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    place = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="District",
    )
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    profession = forms.ModelChoiceField(
        queryset=Profession.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Profession",
    )
    profession_detail = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    guardian_salutation = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    guardian_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    opt_type = forms.ChoiceField(choices=ENQUIRY_TYPE, required=False)
    exchange_vehicle_make = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    exchange_vehicle_model = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    exchange_reg_no = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    exchange_mfg_year = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    owner_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    relation = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=False)

    class Meta:
        model = BookingRequest
        fields = (
            "obf",
            "obf_no",
            "aadhar_card",
            "aadhar_card_no",
            "opt_id",
            "dse",
            "customer_salutation",
            "customer_name",
            "guardian_salutation",
            "guardian_name",
            "mobile",
            "phone",
            "address",
            "place",
            "district",
            "email",
            "profession",
            "profession_detail",
            "opt_type",
            "exchange_vehicle_make",
            "exchange_vehicle_model",
            "exchange_reg_no",
            "exchange_mfg_year",
            "owner_name",
            "relation",
            "car_model",
            "trim",
            "color",
            "variant",
            "scheme",
            "scheme_name",
            "institution_name",
            "amount",
            "yono_scheme_amount",
        )


class BookingRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ["order_date", "order_time", "order_no", "order_amount"]


class BookingLostForm(forms.ModelForm):
    lost_reason = forms.ModelChoiceField(
        queryset=LostReason.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Lost Reason",
    )  # Use the actual queryset here

    class Meta:
        model = BookingLost
        fields = (
            "lost_reason",
            "reason",
            "remarks",
            "cancellation_type",
            "obf_copy",
            "bank_name",
            "account_no",
            "branch_name",
            "ifsc_code",
            "passbook_copy",
        )


class BookingLostUpdateForm(forms.ModelForm):
    class Meta:
        model = BookingLost
        fields = ("stage",)


class BackOrderForm(forms.ModelForm):
    class Meta:
        model = BackOrder
        fields = ["back_order_need", "remarks"]
        exclude = ["back_order_no", "back_order_date"]


class BackOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = BackOrder
        fields = ["back_order_no", "back_order_date"]
        exclude = ["back_order_need", "remarks"]


class ChassisBlockForm(forms.ModelForm):
    car_model = forms.ModelChoiceField(
        queryset=CarModel.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Car Model",
    )
    trim = forms.ModelChoiceField(
        queryset=Trim.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False, label="Trim"
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Color",
    )
    # stock = forms.ModelChoiceField(queryset=Stock.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False, label="Stock")

    class Meta:
        model = ChassisBlock
        fields = ("car_model", "trim", "color", "variant", "stock")


class BookingInvoiceForm(forms.ModelForm):

    is_temp_address = forms.ChoiceField(choices=SELECTION_CHOICES,widget=forms.Select(attrs={"class": "form-control w-20"}),)
    is_exchange = forms.ChoiceField(choices=SELECTION_CHOICES,widget=forms.Select(attrs={"class": "form-control w-20"}),)
    is_scheme = forms.ChoiceField(choices=SELECTION_CHOICES,widget=forms.Select(attrs={"class": "form-control w-20"}),)
    is_yono_scheme = forms.ChoiceField(choices=SELECTION_CHOICES,widget=forms.Select(attrs={"class": "form-control w-20"}),)
    is_finance = forms.ChoiceField(choices=SELECTION_CHOICES_FINANCE,widget=forms.Select(attrs={"class": "form-control w-40"}),)

    opt_id = forms.CharField(max_length=128,widget=forms.TextInput(attrs={"readonly": "readonly"}),)
    booking_no = forms.CharField(max_length=128,widget=forms.TextInput(attrs={"readonly": "readonly"}),)
    booking_date= forms.CharField(max_length=128,widget=forms.TextInput(attrs={"readonly": "readonly"}),)
    
    state = forms.ModelChoiceField(queryset=State.objects.all(), label="State")
    district = forms.ModelChoiceField(queryset=District.objects.all(), label="District")
    # temp address
    temp_state = forms.ModelChoiceField(queryset=State.objects.all(), label="State", required=False)
    temp_district = forms.ModelChoiceField(queryset=District.objects.all(), label="District", required=False)

    car_model = forms.ModelChoiceField(queryset=CarModel.objects.all())
    trim = forms.ModelChoiceField(queryset=Trim.objects.all())
    color = forms.ModelChoiceField(queryset=Color.objects.all())
    variant = forms.ModelChoiceField(queryset=Variant.objects.all())

    class Meta:
        model = BookingInvoice
        fields = (
            "dse",
            "customer_salutation",
            "customer_name",
            "mobile",
            "email",
            "guardian_salutation",
            "guardian_name",
            "dob",
            "house_name",
            "place",
            "panchayath",
            "village",
            "post",
            "pin",
            "state",
            "district",
            "temp_house_name",
            "temp_place",
            "temp_panchayath",
            "temp_village",
            "temp_post",
            "temp_pin",
            "temp_state",
            "temp_district",
            "car_model",
            "trim",
            "color",
            "variant",
            "chassis",
            "exchange_vehicle_make",
            "exchange_vehicle_model",
            "exchange_reg_no",
            "exchange_mfg_year",
            "owner_name",
            "relation",
            "exchange_vehicle_status",
            "scheme",
            "scheme_name",
            "institution_name",
            "amount",
            "yono_scheme_amount",
            "finance",
            "branch",
            "loan_amount",
            "is_temp_address",
            "is_exchange",
            "is_scheme",
            "is_yono_scheme",
            "is_finance",

            "opt_id",
            "booking_no",
            "booking_date",
        )


class InvoiceDiscountForm(forms.ModelForm):
    class Meta:
        model = InvoiceDiscount
        fields = ("discount", "amount","discount_remark")
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "discount": forms.Select(attrs={"class": "form-select"}),
            "discount_remark": forms.TextInput(attrs={"class": "form-control"}),
        }


class InvoiceAccessoryForm(forms.ModelForm):
    class Meta:
        model = InvoiceAccessory
        fields = ("accessory_type", "accessory_name", "payment_type", "amount")
        widgets = {
            "accessory_type": forms.Select(attrs={"class": "form-select"}),
            "accessory_name": forms.TextInput(attrs={"class": "form-control"}),
            "payment_type": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }


class InvoiceDocumentForm(forms.ModelForm):
    class Meta:
        model = InvoiceDocument
        fields = ("document", "file",)
        widgets = {
            'document': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(),
        }



class AccountsTeamInvoiceUpdateForm(forms.ModelForm):
    booking_amount = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = BookingInvoice
        fields = (
            "booking_amount",
            "loan_amount",
            "total_value_to_new_car",
            "total_eligible_bonus",
            "showroom_price",
            "insurance",
            "road_tax",
            "registration_charge",
            "tcs",
            "rsa",
            "p2p",
            "extended_warranty",
            "accounts_status",
            "accounts_remarks",
            "amount",
            "yono_scheme_amount",
            "ac_consumer_offer_amount",
            "vd_other_amount_one",
            "vd_other_amount_two",
            "rd_other_amount_one",
            "rd_other_amount_two",
        )


class InvoiceTopUpForm(forms.ModelForm):
    class Meta:
        model = InvoiceTopUp
        exclude = ("is_active", "invoice")
        widgets = {
            "receipt_no": forms.TextInput(attrs={"class": "form-control"}),
            "receipt_date": forms.DateInput(
                attrs={"class": "form-control dateinput", "data-provide": "datepicker", "format": "dd/mm/yyyy"}
            ),
            "top_up_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "mode_of_payment": forms.Select(attrs={"class": "form-control"}),
        }


class BookingInvoiceDocumentForm(forms.ModelForm):
    class Meta:
        model = BookingInvoiceDocument
        exclude = ("is_active", "invoice", "user")
        widgets = {"document_name": forms.TextInput(attrs={"class": "form-control"})}


INVOICETOPUPFORMSET = inlineformset_factory(
    BookingInvoice, InvoiceTopUp, form=InvoiceTopUpForm, extra=1, can_delete=True
)

BOOKINGINVOICEDOCUMENTFORMSET = inlineformset_factory(
    BookingInvoice, BookingInvoiceDocument, form=BookingInvoiceDocumentForm, extra=1
)




InvoiceDocumentFormset = inlineformset_factory(BookingInvoice, InvoiceDocument, form=InvoiceDocumentForm, extra=1, can_delete=True)

# delivary pending
class DocumentUploadForm(forms.Form):
    document = forms.FileField()  
    

class DailyReportForm(forms.ModelForm):
    
    class Meta:
        model = DailyReport
        fields = (
            "customer_advisor",
            "customer_name",
            "phone",
            "place",
            "profession",
            "segment",
            "existing_vehicle_details",
            "interested_in_new_car",
        )
        

class AfterDeliveryFollowUpForm(forms.ModelForm):

    dse = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","readonly": "readonly"}),
        required=False,
        label="DSE", 
    )

    customer_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","readonly": "readonly"}), required=False)
    mobile = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","readonly": "readonly"}), required=False)
    vehicle_delivered_date = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","readonly": "readonly"}), required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","readonly": "readonly"}), required=False)
    
    
    class Meta:
        model = AfterDeliveryFollowup
        fields = (
            "dse",
            "customer_name",
            "mobile",
            "vehicle_delivered_date",
            "email",
            "dcall_date",
            "answer_1",
            "answer_remark_1",
            "answer_2",
            "answer_remark_2",
            "answer_3",
            "answer_remark_3",
            "answer_4",
            "answer_remark_4",
            "answer_5",
            "answer_remark_5",
            "answer_6",
            "answer_remark_6",
            "answer_7",
            "answer_remark_7",
            "answer_8",
            "answer_remark_8",
            "answer_9",
            "answer_remark_9",
            "answer_10",
            "answer_remark_10",
            "answer_11",
            "answer_remark_11",
            "answer_12",
            "answer_remark_12",
            "answer_13",
            "answer_remark_13",
            "answer_14",
            "answer_remark_14",
            "answer_15",
            "answer_remark_15",

            "customer_voice",
            "d15_calling_remark",

                
        )



class DigitalLeadEnquiryForm(forms.ModelForm):
    
    class Meta:
        model = DigitalLeadEnquiry
        fields = (
            "customer_name",
            "phone_1",
            "phone_2",
            "vehicle_interested",
            "opportunity_source",
            "initial_remark",
            "attended_by",
            "remark_by_tellecaller",
            "expected_buying_date",
            "remark",
            "assigned_to",
        )
        exclude = ("stage",)

class DigitalLeadLostForm(forms.ModelForm):
    class Meta:
        model = DigitalLeadEnquiryLost
        fields = ("reason", "sub_reason", "remarks")

class EventReportForm(forms.ModelForm):
    class Meta:
        model = EventReport
        fields = (
            "event_id",
            "event_date",
            "event_location",
            "model_displayed",
            "total_footfall",
            "prospects",
            "total_booking",
            "total_retail",
            "responsible_ca",
            "event_expense",
            "cost_per_enquiry",
        )