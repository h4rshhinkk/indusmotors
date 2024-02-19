from core.base import BaseTable
from crm.models import BookingInvoice, BackOrder

from django_tables2 import columns


class BookingInvoiceTable(BaseTable):
    action = columns.TemplateColumn(
        """
        {% if request.user.usertype == 'invoice_team' or request.user.usertype == 'stock' %}
        <a href="{{record.get_update_url}}" class="btn btn-sm btn-light btn-outline-info">Update</a>
        {% endif %}

        {% if request.user.usertype == 'invoice_team' %}
        <a href="{{record.get_absolute_url}}" class="btn btn-sm btn-light btn-outline-success">View Plan</a>
        <form action="{{record.get_invoice_team_reject_url}}" method="post" class="d-inline" id="invoice-reject-form">
        <button type="submit"   class="btn btn-sm btn-light btn-outline-danger">Reject</button>
        </form>
        {% endif %}
        
        """,
        orderable=False,
    )
    created_at = None

    vehicle_details = columns.TemplateColumn(
        """
        <b>Model</b> :{{record.chassis.variant.car_model}} <br>
        <b>Trim</b> :{{record.chassis.variant.trim}} <br>
        <b>Variant</b> :{{record.chassis.variant.vehicle_code}} <br>
        
         """,
        orderable=False,
    )

    class Meta:
        model = BookingInvoice
        fields = ("booking_request__opportunity", "booking_request__order_no", "vehicle_details", "chassis")
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class InvoicedTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{{record.get_discount_create_url}}">Add Discount</a></li>
                <li><a class="dropdown-item" href="{{record.get_accessory_create_url}}">Add Accessory</a></li>
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Request For Delivery Plan</a></li>
            </ul>
        </div>
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

    vehicle_details = columns.TemplateColumn(
        """
         <b>Model</b> :{{record.chassis.variant.car_model}} - {{record.chassis.variant.trim}}<br>
         {{record.chassis.variant}}<br>
         <b>Color</b> :{{record.chassis.variant.color}}<br>
         <b>Type</b> :{{record.chassis.bs_type}} <br>
        <b>Chassis</b> :{{record.chassis.chassis_number}} <br>
        
         """,
        orderable=False,
    )

    billing_details = columns.TemplateColumn(
        """
        <b>Invoice Date</b>:{{record.invoice_date}} <br>
        <b>Invoice No</b>:{{record.invoice_no}} <br>
         """,
        orderable=False,
    )

    contact_details = columns.TemplateColumn(
        """
        <b>Name</b>: {{record.customer_name}} <br>
        <b>Mobile</b>: {{record.mobile}} <br>
        <b>Address</b>: {{record.house_name}},{{record.place}},{{record.post}} <br> {{record.pin}},{{record.state}},{{record.district}} <br>
         """,
        orderable=False,
    )

    class Meta:
        model = BookingInvoice
        fields = ("branch_dse", "enquiry_booking", "contact_details", "vehicle_details", "billing_details")
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class BookingInvoiceTableInvoiceTeam(BaseTable):
    action = columns.TemplateColumn(
        """
        <a href="{{record.get_update_url}}" class="btn btn-sm btn-light btn-outline-info">Update</a>
        
        """,
        orderable=False,
    )

    class Meta:
        model = BookingInvoice
        fields = ("booking_request__opportunity", "booking_request__order_no", "booking_request__variant")
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class BackOrderRequestTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <a href="{% url 'stock:back_order_request_update' record.pk %}" class="btn btn-sm btn-light btn-outline-info">Update</a>
        
        """,
        orderable=False,
    )

    vehicle_details = columns.TemplateColumn(
        """
         <b>Model</b> :{{record.booking_request.variant.car_model}} - {{record.booking_request.variant.trim}}<br>
         <b>Variant</b> :{{record.booking_request.variant}}<br>
         <b>Color</b> :{{record.booking_request.variant.color}}<br>
         
       
        
         """,
        orderable=False,
    )

    class Meta:
        model = BackOrder
        fields = (
            "booking_request",
            "booking_request__opportunity__dse",
            "vehicle_details",
            "booking_request__order_no",
            "back_order_need",
            "remarks",
            "back_order_no",
        )
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}
