from core.base import BaseTable
from crm.functions import get_stock_in_optlist

from .models import (
    AfterDeliveryFollowup,
    BackOrder,
    BookingInvoice,
    BookingInvoiceDocument,
    DailyReport,
    DigitalLeadEnquiry,
    DigitalLeadEnquiryLost,
    DigitalLeadFollowUp,
    EventPhoto,
    EventReport,
    InvoiceAccessory,
    InvoiceDocument,
    EventCustomerDetails,
)
from .models import BookingFollowUp
from .models import BookingRequest
from .models import ChassisBlock
from .models import Opportunity
from .models import OpportunityFollowUp
from .models import OpportunityLost, BookingLost
from .models import TestDriveRequest
from .models import InvoiceDiscount
from django_tables2 import columns
import django_tables2 as tables


class OpportunityTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            {% if request.user.usertype == 'finance_executive' %}
                <li><a class="dropdown-item" href="{{record.get_absolute_url}}">View Opportunity</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:followup_create' record.pk %}">View Follow Ups</a></li>
            {% else %}
                <li><a class="dropdown-item" href="{{record.get_absolute_url}}">View Opportunity</a></li>
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Edit Opportunity</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:followup_create' record.pk %}">Update Follow Up</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:testdrive_create' record.pk %}">Request for TestDrive</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:opt_lost_create' record.pk %}">Request Lost</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:booking_request_create' record.pk %}">Request for Booking</a></li>
            {% endif %}
            </ul>
        </div>

        """,
        orderable=False,
    )

    followup_details = columns.TemplateColumn(
        """
        Next Followup: {{record.last_followup.followup_date}}<br>
        {{record.last_followup.opt_status}}<br>
        {{record.last_followup.remarks}}<br>
        Exp Bkg:{{record.last_followup.exp_booking_date}}
        """,
        orderable=False,
        verbose_name="Follow Details",
    )

    opt_date_id = columns.TemplateColumn(
        """
        {{record.opt_date}}<br>
        {{record.opt_id}}

        """,
        orderable=False,
        verbose_name="Opt ID/Date",
    )

    branch_dse = columns.TemplateColumn(
        """
        {{record.dse}}<br>
        {{record.dse.branch.all.first}}

        """,
        orderable=False,
        verbose_name="Branch / DSE",
    )

    vehicle_variant = columns.TemplateColumn(
        """
        {{record.variant.car_model}}<br>
        {{record.variant.trim}}<br>
        {{record.variant.transmission}} - {{record.variant.fuel}}

        """,
        orderable=False,
        verbose_name="Vehicle / Variant",
    )

    exchange_details = columns.TemplateColumn(
        """
        {{record.exchange_vehicle_make|default_if_none:""}}<br>
        {{record.exchange_vehicle_model|default_if_none:""}}<br>
        {{record.exchange_reg_no|default_if_none:""}} {{record.exchange_mfg_year|default_if_none:""}}

        """,
        orderable=False,
    )

    stock_status = columns.Column(empty_values=())

    def render_stock_status(self, value, record):
        return get_stock_in_optlist(record.variant)

    class Meta:
        model = Opportunity
        fields = (
            "branch_dse",
            "opt_date_id",
            "customer_name",
            "mobile",
            "vehicle_variant",
            "followup_details",
            "exchange_details",
            "stock_status",
        )
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class OpportunityFollowUpTable(BaseTable):
    action = columns.TemplateColumn(
        """

        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{{record.get_absolute_url}}">View</a></li>
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Update</a></li>
            </ul>
        </div>


        """,
        orderable=False,
    )
    created = None

    class Meta:
        model = OpportunityFollowUp
        fields = (
            "followup_date",
            "opt_status",
            "remarks",
            "next_followup_date",
            "followup_via",
            "finance_executive_status",
        )
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class TestDriveRequestTable(BaseTable):
    action = columns.TemplateColumn(
        """

        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            {% if request.user.usertype == 'test_drive_operator' %}
                <li><a class="dropdown-item" href="{% url 'crm:pending_testdrive_update' record.pk %}">Update</a></li>
            {% else %}
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Update</a></li>
                <li><a class="dropdown-item" href="{{record.get_delete_url}}">Delete</a></li>
            {% endif %}
            </ul>
        </div>


        """,
        orderable=False,
    )
    # status = tables.TemplateColumn(template_name="app/partials/testdrive_status_form.html")
    created = None

    vehicle_variant = columns.TemplateColumn(
        """
        {{record.variant}}<br>
        {{record.variant.trim}}<br>
        {{record.variant.transmission}} - {{record.variant.fuel}}

        """,
        orderable=False,
        verbose_name="Vehicle / Variant",
    )

    calculate_total_kilometers = columns.Column(orderable=False, verbose_name="Distance Covered")

    class Meta:
        model = TestDriveRequest
        fields = (
            "opportunity",
            "vehicle_variant",
            "preferred_date",
            "preferred_time",
            "testdrive_stage",
            "status",
            "calculate_total_kilometers",
            "remarks",
        )
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class OpportunityLostTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Update</a></li>
                <li><a class="dropdown-item" href="{{record.get_delete_url}}">Delete</a></li>

            </ul>
        </div>

        """,
        orderable=False,
    )

    reason = columns.TemplateColumn(
        """
        {{record.reason}}

        """,
        orderable=False,
        verbose_name="Lost Reason",
    )

    class Meta:
        model = OpportunityLost
        fields = ("opportunity", "reason", "sub_reason", "remarks")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class BookingRequestTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            {% if request.user.usertype == 'finance_executive' %}
                <li><a class="dropdown-item" href="{% url 'crm:booking_followup_create' record.pk %}">Booking Follow Up</a></li>
            {% else %}
                <li><a class="dropdown-item" href="{% url 'crm:booking_followup_create' record.pk %}">Booking Follow Up</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:back_order_create' record.pk %}">Request Back Order</a></li>
                {% comment %}<li><a class="dropdown-item" href="{% url 'crm:chassis_block_create' record.pk %}">Chasis Block</a></li>{% endcomment %}
                <li><a class="dropdown-item" href="{% url 'crm:booking_lost_create' record.pk %}">Cancel Booking</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:testdrive_create' record.opportunity.pk %}">Test Drive Request</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:invoice_request_create' record.pk %}">Invoice Request</a></li>
            {% endif %}
            </ul>
        </div>

        """,
        orderable=False,
    )

    branch_dse = columns.TemplateColumn(
        """
        {{record.opportunity.dse}}<br>
        {{record.opportunity.dse.branch.all.first}}

        """,
        orderable=False,
        verbose_name="Branch / DSE",
    )

    enquiry_details = columns.TemplateColumn(
        """
        {{record.opportunity.opt_id}}<br>
        {{record.opportunity.opt_date}}
        """,
        orderable=False,
        verbose_name="Enquiry Details",
    )

    name_place = columns.TemplateColumn(
        """
        {{record.opportunity.customer_name}}<br>
        {{record.opportunity.place}}
        """
    )

    booking_details = columns.TemplateColumn(
        """
        {{record.order_date}}<br>
        {{record.order_no}}
        """,
        orderable=False,
        verbose_name="Booking Details",
    )

    vehicle_variant = columns.TemplateColumn(
        """
        {{record.opportunity.variant.car_model}}<br>
        {{record.opportunity.variant.trim}}<br>
        {{record.opportunity.variant.transmission}} - {{record.opportunity.variant.fuel}}

        """,
        orderable=False,
        verbose_name="Vehicle / Variant",
    )

    finance_details = columns.TemplateColumn(
        """
        {{record.last_followup_finance.finance|default:"-"}}<br>
        {{record.last_followup_finance.branch|default:"-"}}<br>
        {{record.last_followup_finance.loan_amount|default:"-"}}

        """,
        orderable=False,
    )

    class Meta:
        model = BookingRequest
        fields = (
            "branch_dse",
            "enquiry_details",
            "name_place",
            "booking_details",
            "vehicle_variant",
            "stage",
            "finance_details",
        )
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class BookingRequestedTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{% url 'crm:booking_request_delete' record.pk %}">Delete</a></li>

            </ul>
        </div>

        """,
        orderable=False,
    )

    class Meta:
        model = BookingRequest
        fields = (
            "opportunity__dse",
            "opportunity",
            "opportunity__place",
            "order_date",
            "order_no",
            "opportunity__variant",
        )
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class BookingFollowUpTable(BaseTable):
    action = columns.TemplateColumn(
        """

        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{{record.get_absolute_url}}">View</a></li>
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Update</a></li>
            </ul>
        </div>


        """,
        orderable=False,
    )
    created = None

    class Meta:
        model = BookingFollowUp
        fields = (
            "booking_followup_date",
            "booking_status",
            "exp_billing_date",
            "exp_delivery_date",
            "finance_executive_status",
        )
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class BookingLostTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            {% if request.user.usertype == 'asm' or request.user.usertype == 'sm' or request.user.usertype == 'gm' or request.user.usertype == 'accounts' %}
                <li><a class="dropdown-item" href="{% url 'crm:booking_lost_dpt_update' record.pk %}">Update</a></li>
            {% else %}
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Update</a></li>
                <li><a class="dropdown-item" href="{{record.get_delete_url}}">Delete</a></li>
            {% endif %}
            </ul>
        </div>

        """,
        orderable=False,
    )

    created = None

    stage = columns.Column(orderable=False, verbose_name="Status")

    class Meta:
        model = BookingLost
        fields = ("booking_request__opportunity", "reason__reason", "remarks", "stage")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class BackOrderTable(BaseTable):
    class Meta:
        model = BackOrder
        fields = ("booking_request", "back_order_need", "remarks")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class ChassisBlockTable(BaseTable):
    class Meta:
        model = ChassisBlock
        fields = ("booking_request", "variant", "stock")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class InvoiceDiscountTable(BaseTable):
    created = None
    action = None
    status = tables.TemplateColumn(template_name="app/partials/discount_status_form.html")

    class Meta:
        model = InvoiceDiscount
        fields = ("discount", "amount","discount_remark","status",)
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class InvoiceAccessoryTable(BaseTable):
    created = None

    class Meta:
        model = InvoiceAccessory
        fields = ("invoice", "accessory_type", "accessory_name", "payment_type", "amount")
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class PlanPendingBaseTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <ul>
            <li><a class="btn btn-sm btn-primary mb-1" href="{{record.get_document_create_url}}">Add Documents</a></li>
            <li><a class="btn btn-sm btn-primary mb-1" href="{{record.get_discount_create_url}}">Add Discount</a></li>
            <li><a class="btn btn-sm btn-primary mb-1" href="{{record.get_accessory_create_url}}">Add Accessory</a></li>
            <li><a class="btn btn-sm btn-primary mb-1" href="{{record.get_invoice_update_url}}">Update Plan</a></li>
            <li><a class="btn btn-sm btn-primary mb-1" href="{{record.get_absolute_url}}">View Plan</a></li>
        </ul>
        """,
        orderable=False,
    )

    created = None

    branch_dse = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.dse.branch.all.first}} <br>
        {{record.booking_request.opportunity.dse}} <br>
         """,
        orderable=False,
    )

    enquiry_booking = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.opt_id}} <br>
        {{record.booking_request.opportunity.opt_date}} <br>
        OBF No: {{record.booking_request.obf_no}} <br>
        Order No: {{record.booking_request.order_no}} <br>
        Order Date :{{record.booking_request.order_date}} <br>
         """,
        orderable=False,
    )
    customer_details = columns.TemplateColumn(
        """
        Name : {{record.customer_name}} <br>
        Phone : {{record.mobile}} <br>
        Address : {{record.house_name}} <br>
        {{record.place}} - {{record.village}}<br>
        {{record.district}} <br>
        """,
        orderable=False,
    )
    vehicle_details = columns.TemplateColumn(
        """
        <b>Vehicle</b> :{{record.chassis.variant.car_model}} <br>
        <b>Variant</b> :{{record.chassis.variant.vehicle_code}} <br>
        <b>Trim</b> :{{record.chassis.variant.trim}} <br>
        <b>Chassis</b> :{{record.chassis.chassis_number}} <br>
        <b>Type</b> :{{record.chassis.bs_type}} <br>
         """,
        orderable=False,
    )

    billing_details = columns.TemplateColumn(
        """
        Invoice Date :{{record.invoice_date}} <br>
        Order No :{{record.invoice_no}} <br>
         """,
        orderable=False,
    )

    registration = columns.TemplateColumn(
        """
        {{record.get_reg_status_display}} <br>
        {% if record.reg_status == 'pending' %}
        <i class="fe fe-x text-danger h1"></i>
        {% elif record.reg_status == 'ok' %}
        <i class="fe fe-check text-success h1"></i>
        {% else %}
        <i class="fe fe-x text-danger h1"></i>
        {% endif %}
        <br>
        <b>RTO</b>:{{record.rto}} <br>
        <b>Type</b>:{{record.reg_type}} <br>
        <b>Tax Exemption</b>:{{record.any_tax_exemption}} <br>
         """,
        orderable=False,
    )
    scheme = columns.TemplateColumn(
        """
        {{record.get_scheme_status_display}} <br>
        {% if record.scheme_status == 'pending' %}
        <i class="fe fe-x text-danger h1"></i>
        {% elif record.scheme_status == 'ok' %}
        <i class="fe fe-check text-success h1"></i>
        {% else %}
        <i class="fe fe-x text-danger h1"></i>
        {% endif %}
        <br>
        <b>Scheme </b>:{{record.scheme}} <br>
        <b>Amount </b>:{{record.amount}} <br>
        <b>Yono scheme amount </b>:{{record.yono_scheme_amount}} <br>
        <b>Yono Status </b>:{{record.get_yono_scheme_status_display}} <br>
        <b>Yono Remark </b>:{{record.yono_scheme_remark|default:"N/A"}} <br>

         """,
        orderable=False,
    )
    insurance = columns.TemplateColumn(
        """
        {{record.get_insurance_status_display}} <br>
        {% if record.insurance_status == 'pending' %}
        <i class="fe fe-x text-danger h1"></i>
        {% elif record.insurance_status == 'ok' %}
        <i class="fe fe-check text-success h1"></i>
        {% else %}
        <i class="fe fe-x text-danger h1"></i>
        {% endif %}
        <br>
        {{record.get_insurance_type_display}} <br>
        <b>Nominee </b>:{{record.nominee_name}} <br>
        <b>Relation </b>:{{record.nominee_relation}} <br>
        <b>Insurance Amount </b>:{{record.insurance_amount|default:"0"}} <br>
         """,
        orderable=False,
    )

    discount = columns.TemplateColumn(
        """
        {{record.get_discount_status_display}} <br>
        {% if record.discount_status == 'pending' %}
        <i class="fe fe-x text-danger h1"></i>
        {% elif record.discount_status == 'ok' %}
        <i class="fe fe-check text-success h1"></i>
        {% else %}
        <i class="fe fe-x text-danger h1"></i>
        {% endif %}
        {% for discount in record.get_discounts %}
            {{ discount.discount}} : {{ discount.amount }} <br>
        {% endfor %}
         """,
        orderable=False,
    )
    accounts = columns.TemplateColumn(
        """
        {{record.get_accounts_status_display}} <br>
        {% if record.accounts_status == 'pending' %}
        <i class="fe fe-x text-danger h1"></i>
        {% elif record.accounts_status == 'ok' %}
        <i class="fe fe-check text-success h1"></i>
        {% else %}
        <i class="fe fe-x text-danger h1"></i>
        {% endif %}
         """,
        orderable=False,
    )
    finance_status = columns.TemplateColumn(
        """
        {{record.get_finance_status_display}}<br>
        {% if record.finance_status == 'pending' %}
        <i class="fe fe-x text-danger h1"></i>
        {% elif record.finance_status == 'ok' %}
        <i class="fe fe-check text-success h1"></i>
        {% else %}
        <i class="fe fe-x text-danger h1"></i>
        {% endif %}
        {% if finance %}
        {{record.finance}} <br>
        {{record.branch}} <br>
        {{record.loan_amount}}
        {% endif %}
        {% if record.finance_remarks %}
        Remark : {{record.finance_remarks}}
        {% endif %}
         """
    )
    accessory_status = columns.TemplateColumn(
        """
        {{record.get_accessory_status_display}}<br>
        {% if record.accessory_status == 'pending' %}
        <i class="fe fe-x text-danger h1"></i>
        {% elif record.accessory_status == 'ok' %}
        <i class="fe fe-check text-success h1"></i>
        {% else %}
        <i class="fe fe-x text-danger h1"></i>
        {% endif %}
         """
    )
    exchange_status = columns.TemplateColumn(
        """

        {{record.get_exchange_status_display}}<br>
        {% if record.exchange_status == 'pending' %}
        <i class="fe fe-x text-danger h1"></i>
        {% elif record.exchange_status == 'ok' %}
        <i class="fe fe-check text-success h1"></i>
        {% else %}
        <i class="fe fe-x text-danger h1"></i>
        {% endif %}
        Exchange Amount :{{record.total_eligible_bonus|default:"0"}}<br>
         """
    )

    pdi_status = columns.TemplateColumn(
        """
        {{record.get_pdi_status_display}}<br>
        {% if record.pdi_status == 'pending' %}
        <i class="fe fe-x text-danger h1"></i>
        {% elif record.pdi_status == 'ok' %}
        <i class="fe fe-check text-success h1"></i>
        {% else %}
        <i class="fe fe-x text-danger h1"></i>
        {% endif %}
        <b>Suggested Delivery Date </b>:{{record.suggested_delivery_date|default:"N/A"}} <br>
         """
    )


class PlanPendingTable(PlanPendingBaseTable):
    class Meta:
        model = BookingInvoice
        fields = (
            "branch_dse",
            "enquiry_booking",
            "customer_details",
            "vehicle_details",
            "billing_details",
            "finance_status",
            "accessory_status",
            "exchange_status",
            "registration",
            "scheme",
            "insurance",
            "discount",
            "accounts",
            "pdi_status",
        )
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class InvoiceDocumentTable(BaseTable):
    action = None

    file = columns.TemplateColumn(
        """
        <a class="btn btn-sm btn-primary mb-1" href="{{record.file.url}}" target="_blank"><i class="fe fe-eye bs-light align-middle"></i>  View Document</a>
         """
    )

    class Meta:
        model = InvoiceDocument
        fields = ("document", "file")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class InvoiceVeificationTable(BaseTable):
    created = None

    branch_dse = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.dse.branch.all.first.all.first}} <br>
        {{record.booking_request.opportunity.dse}} <br>
         """,
        orderable=False,
    )

    enquiry_booking = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.opt_id}} <br>
        {{record.booking_request.opportunity.opt_date}} <br>
        OBF No: {{record.booking_request.obf_no}} <br>
        Order No: {{record.booking_request.order_no}} <br>
        Order Date :{{record.booking_request.order_date}} <br>
         """,
        orderable=False,
    )
    customer_details = columns.TemplateColumn(
        """
        Name : {{record.booking_request.opportunity.customer_name}} <br>
        Address : {{record.house_name}} <br>
        {{record.place}} <br>
        {{record.panchayath}} <br>
        {{record.district}} <br>
        """,
        orderable=False,
    )
    vehicle_details = columns.TemplateColumn(
        """
        <b>Vehicle</b> :{{record.chassis.variant.car_model}} <br>
        <b>Trim</b> :{{record.chassis.variant.trim}} <br>
        <b>Variant</b> :{{record.chassis.variant.vehicle_code}} <br>
        <b>Chassis</b> :{{record.chassis.chassis_number}} <br>
        <b>Type</b> :{{record.chassis.bs_type}} <br>
         """,
        orderable=False,
    )

    billing_details = columns.TemplateColumn(
        """
        Invoice Date :{{record.invoice_date}} <br>
        Invoice No :{{record.invoice_no}} <br>
         """,
        orderable=False,
    )
    action = columns.TemplateColumn(
        """
        {% if request.user.usertype == 'finance_bo' %}
        <a href="{{ record.get_finance_status_update_url }}" class="btn btn-sm btn-light btn-outline-info">UPDATE</a>
        <a href="{{record.get_absolute_url}}" class="btn btn-sm btn-light btn-outline-success">View Plan</a>
        {% elif request.user.usertype == 'exchange_bo' %}
        <a href="{{ record.get_exchange_status_update_url }}" class="btn btn-sm btn-light btn-outline-info">UPDATE</a>
        <a href="{{record.get_absolute_url}}" class="btn btn-sm btn-light btn-outline-success">View Plan</a>
        {% elif request.user.usertype == 'registration_bo' %}
        <a href="{{ record.get_registration_status_update_url }}" class="btn btn-sm btn-light btn-outline-info">UPDATE</a>
        <a href="{{record.get_absolute_url}}" class="btn btn-sm btn-light btn-outline-success">View Plan</a>
        {% elif request.user.usertype == 'scheme' %}
        <a href="{{ record.get_scheme_status_update_url }}" class="btn btn-sm btn-light btn-outline-info">UPDATE</a>
        <a href="{{record.get_absolute_url}}" class="btn btn-sm btn-light btn-outline-success">View Plan</a>
        {% elif request.user.usertype == 'insurance' %}
        <a href="{{ record.get_insurance_status_update_url }}" class="btn btn-sm btn-light btn-outline-info">UPDATE</a>
        <a href="{{record.get_absolute_url}}" class="btn btn-sm btn-light btn-outline-success">View Plan</a>
        {% elif request.user.usertype == 'pdi' %}
        <a href="{{ record.get_pdi_status_update_url }}" class="btn btn-sm btn-light btn-outline-info">UPDATE</a>
        <a href="{{record.get_absolute_url}}" class="btn btn-sm btn-light btn-outline-success">View Plan</a>
        {% elif request.user.usertype == 'tmga' %}

        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{{ record.get_accessory_status_update_url }}">UPDATE</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:job_card' record.pk %}" target="_blank"">Print Job Card</a></li>
                <li><a class="dropdown-item" href="{{record.get_accessory_create_url}}">Add Accessory</a></li>
                <li><a class="dropdown-item" href="{{record.get_absolute_url}}">View Plan</a></li>
            </ul>
        </div>

        {% endif %}
        """,
        orderable=False,
    )

    class Meta:
        model = BookingInvoice
        fields = ("branch_dse", "enquiry_booking", "customer_details", "vehicle_details", "billing_details")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class SaleSupportTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <a href="{{ record.get_discount_status_update_url }}" class="btn btn-sm btn-light btn-outline-info">UPDATE</a>
        """,
        orderable=False,
    )
    created = None
    branch_dse = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.dse.branch.all.first.all.first}} <br>
        {{record.booking_request.opportunity.dse}} <br>
         """,
        orderable=False,
    )

    enquiry_booking = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.opt_id}} <br>
        {{record.booking_request.opportunity.opt_date}} <br>
        OBF No: {{record.booking_request.obf_no}} <br>
        Order No: {{record.booking_request.order_no}} <br>
        Order Date :{{record.booking_request.order_date}} <br>
         """,
        orderable=False,
    )
    customer_details = columns.TemplateColumn(
        """
        Name : {{record.booking_request.opportunity.customer_name}} <br>
        Address : {{record.house_name}} <br>
        """,
        orderable=False,
    )
    vehicle_details = columns.TemplateColumn(
        """
        <b>Vehicle</b> :{{record.chassis.variant.car_model}} <br>
        <b>Variant</b> :{{record.chassis.variant.vehicle_code}} <br>
        <b>Chassis</b> :{{record.chassis.chassis_number}} <br>
        <b>Type</b> :{{record.chassis.bs_type}} <br>
         """,
        orderable=False,
    )

    billing_details = columns.TemplateColumn(
        """
        Invoice Date :{{record.invoice_date}} <br>
        Order No :{{record.invoice_no}} <br>
         """,
        orderable=False,
    )

    class Meta:
        model = BookingInvoice
        fields = ("branch_dse", "enquiry_booking", "customer_details", "vehicle_details", "billing_details")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class PlanAccountsTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{{record.get_document_create_url}}">View Documents</a></li>

                <li><a class="dropdown-item" href="{{record.get_accounts_status_update_url}}">Update</a></li>
            </ul>
        </div>
        """,
        orderable=False,
    )
    created = None
    branch_dse = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.dse.branch.all.first.all.first}} <br>
        {{record.booking_request.opportunity.dse}} <br>
         """,
        orderable=False,
    )

    enquiry_booking = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.opt_id}} <br>
        {{record.booking_request.opportunity.opt_date}} <br>
        OBF No: {{record.booking_request.obf_no}} <br>
        Order No: {{record.booking_request.order_no}} <br>
        Order Date :{{record.booking_request.order_date}} <br>
         """,
        orderable=False,
    )
    customer_details = columns.TemplateColumn(
        """
        Name : {{record.booking_request.opportunity.customer_name}} <br>
        Address : {{record.address}} <br>
        """,
        orderable=False,
    )
    vehicle_details = columns.TemplateColumn(
        """
        <b>Vehicle</b> :{{record.chassis.variant.car_model}} <br>
        <b>Variant</b> :{{record.chassis.variant.vehicle_code}} <br>
        <b>Chassis</b> :{{record.chassis.chassis_number}} <br>
        <b>Type</b> :{{record.chassis.bs_type}} <br>
         """,
        orderable=False,
    )
    amounts = columns.TemplateColumn(
        """
        Receipts <br>
        Finance : {{record.loan_amount|default:"0"}} <br>
        Schemes : {{record.amount|default:"0"}} <br>
        Yono : {{record.yono_scheme_amount|default:"0"}} <br>
        Discounts:<br>
        {% for discount in record.get_discounts %}
            {{ discount.discount }} : {{ discount.amount }}
        {% endfor %}
        """,
        orderable=False,
    )

    class Meta:
        model = BookingInvoice
        fields = ("branch_dse", "enquiry_booking", "customer_details", "vehicle_details", "amounts")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class DeliveredTable(PlanPendingBaseTable):
    action = columns.TemplateColumn(template_name="app/partials/table_actions_delivered.html", orderable=False)
    view_document = columns.TemplateColumn(template_name="app/partials/view_document_modal.html", verbose_name="Documents",orderable=False)
    download_documents = columns.TemplateColumn(template_name="app/partials/delivered_download_document_button.html", verbose_name="Download Documents",orderable=False)
    class Meta:
        model = BookingInvoice
        fields = (
            "branch_dse",
            "enquiry_booking",
            "customer_details",
            "vehicle_details",
            "billing_details",
            "finance_status",
            "accessory_status",
            "exchange_status",
            "registration",
            "scheme",
            "insurance",
            "discount",
            "accounts",
            "pdi_status",
            "view_document",
            "download_documents"
        )
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class DeliveryPendingTable(PlanPendingBaseTable):
    download_documents = columns.TemplateColumn(template_name="app/partials/download_document_buttons.html", verbose_name="Download Documents",orderable=False)
    action = columns.TemplateColumn(template_name="app/partials/table_actions_delivary_pending.html", orderable=False)
    registration_remarks = columns.TemplateColumn(
        """
        {% for remark in record.get_registration_remarks %}
            {{ remark.remark }} <br>
            {{ remark.created|date:"d/m/Y" }}
             <div class="reg-line"> <hr class="solid"></div>
        {% endfor %}
        """,
        orderable=False,
    )
    view_document = columns.TemplateColumn(template_name="app/partials/view_document_modal.html", verbose_name="Documents",orderable=False)
    
    class Meta:
        model = BookingInvoice
        fields = (
            "branch_dse",
            "enquiry_booking",
            "customer_details",
            "vehicle_details",
            "billing_details",
            "finance_status",
            "accessory_status",
            "exchange_status",
            "registration",
            "scheme",
            "insurance",
            "discount",
            "accounts",
            "pdi_status",
            "registration_remarks",
            "plan_ok_date",
            "view_document",
            "download_documents"
        )
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class AfterDeliveryFollowupTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{% url 'crm:after_delivery_followup_print' record.pk %}" target="_blank">Print Followup</a></li>
            </ul>
        </div>

        """,
        orderable=False,
    )

    class Meta:
        model = AfterDeliveryFollowup
        fields = ("invoice__customer_name", "invoice__mobile", "invoice__vehicle_delivered_date","invoice__dse", "dcall_date")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class InvoiceRejectUpdateTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{% url 'crm:invoice_rejected_update' record.pk %}">Update</a></li>
            </ul>
        </div>

        """,
        orderable=False,
    )

    branch_dse = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.dse}}<br>
        {{record.booking_request.opportunity.dse.branch.all.first}}

        """,
        orderable=False,
        verbose_name="Branch / DSE",
    )

    enquiry_details = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.opt_id}}<br>
        {{record.booking_request.opportunity.opt_date}}
        """,
        orderable=False,
        verbose_name="Enquiry Details",
    )

    name_place = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.customer_name}}<br>
        {{record.booking_request.opportunity.place}}
        """
    )

    booking_details = columns.TemplateColumn(
        """
        {{record.booking_request.order_date}}<br>
        {{record.booking_request.order_no}}
        """,
        orderable=False,
        verbose_name="Booking Details",
    )

    vehicle_variant = columns.TemplateColumn(
        """
        {{record.booking_request.variant.car_model}}<br>
        {{record.booking_request.variant.trim}}<br>
        {{record.booking_request.variant.transmission}} - {{record.booking_request.variant.fuel}}

        """,
        orderable=False,
        verbose_name="Vehicle / Variant",
    )

    class Meta:
        model = BookingInvoice
        fields = ("branch_dse", "enquiry_details", "name_place", "booking_details", "vehicle_variant", "status")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class BookingInvoiceDocumentTable(BaseTable):
    action = None
    created = None

    class Meta:
        model = BookingInvoiceDocument
        fields = ("user", "document_name", "document")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class DeliveredFollowupTable(BaseTable):
    created = None

    customer_details = columns.TemplateColumn(
        """
        Name : {{record.customer_name}} <br>
        Phone : {{record.mobile}} <br>
        Address : {{record.house_name}} <br>
        {{record.place}} - {{record.village}}<br>
        {{record.district}} <br>
        """,
        orderable=False,
    )

    branch_dse = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.dse.branch.all.first}} <br>
        {{record.booking_request.opportunity.dse}} <br>
         """,
        orderable=False,
    )

    enquiry_booking = columns.TemplateColumn(
        """
        {{record.booking_request.opportunity.opt_id}} <br>
        {{record.booking_request.opportunity.opt_date}} <br>
        OBF No: {{record.booking_request.obf_no}} <br>
        Order No: {{record.booking_request.order_no}} <br>
        Order Date :{{record.booking_request.order_date}} <br>
         """,
        orderable=False,
    )
    
    vehicle_details = columns.TemplateColumn(
        """
        <b>Vehicle</b> :{{record.chassis.variant.car_model}} <br>
        <b>Variant</b> :{{record.chassis.variant.vehicle_code}} <br>
        <b>Trim</b> :{{record.chassis.variant.trim}} <br>
        <b>Chassis</b> :{{record.chassis.chassis_number}} <br>
        <b>Type</b> :{{record.chassis.bs_type}} <br>
         """,
        orderable=False,
    )

    billing_details = columns.TemplateColumn(
        """
        Invoice Date :{{record.invoice_date}} <br>
        Order No :{{record.invoice_no}} <br>
         """,
        orderable=False,
    )

    action = columns.TemplateColumn(template_name="app/partials/table_actions_delivered.html", orderable=False)
    
    class Meta:
        model = BookingInvoice
        fields = (
            "customer_details",
            "branch_dse",
            "enquiry_booking",
            "vehicle_details",
            "billing_details",
        )
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class DailyReportTable(BaseTable):
    action = None

    class Meta:
        model = DailyReport
        fields = (
            "customer_name",
            "phone",
            "place",
            "profession",
            "segment",
            "existing_vehicle_details",
            "interested_in_new_car",
        )
        exclude = ("created",)
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class DigitalLeadEnquiryTable(BaseTable):
    action = None

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
        exclude = ("created",)
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class DigitalLeadEnquiryTeamLeadTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{% url 'crm:digital_lead_followup_create' record.pk %}">Update Follow Up</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:digital_lead_lost_create' record.pk %}">Lost Update</a></li>
            </ul>
        </div>

        """,
        orderable=False,
    )

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
        exclude = ("created",)
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class DigitalLeadFollowUpTable(BaseTable):
    action = None
    created = None

    class Meta:
        model = DigitalLeadFollowUp
        fields = (
            "followup_date",
            "followup_via",
            "opt_status",
            "exp_booking_date",
            "exp_retail_date",
            "next_followup_date",
            "remarks",
            
        )
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class DigitalLeadEnquiryLostTable(BaseTable):
    action = None
    reason = columns.TemplateColumn(
        """
        {{record.reason}}

        """,
        orderable=False,
        verbose_name="Lost Reason",
    )

    class Meta:
        model = DigitalLeadEnquiryLost
        fields = ("digital_lead", "reason", "sub_reason", "remarks")
        attrs = {"class": "table key-buttons border-bottom table-hover"}


class EventReportTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Edit Event</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:event_photo_create' record.pk %}">Upload Event Image</a></li>
                <li><a class="dropdown-item" href="{% url 'crm:event_customer_details_create' record.pk %}">Add Customer Details</a></li>
               

                
            </ul>
        </div>

        """,
        orderable=False,
    )

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
        exclude = ("created",)
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class EventPhotoTable(BaseTable):
    action = None
    created = None

    file = columns.TemplateColumn(
        """
        <a class="btn btn-sm btn-primary mb-1" href="{{record.file.url}}" target="_blank"><i class="fe fe-eye bs-light align-middle"></i>  View Photo</a>
         """
    )

    class Meta:
        model = EventPhoto
        fields = (
            "file",     
        )
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class EventCustomerDetailsTable(BaseTable):
    action = None
    created = None

    class Meta:
        model = EventCustomerDetails
        fields = (
            "customer_name",
            "phone",
            "enquiry_model",
            "existing_model",
            "enquiry_status",
            "customer_profile",
            "exp_booking_date",
            "ca_name",    
        )
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}