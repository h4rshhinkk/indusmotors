from core.base import BaseTable

from .models import Stock, Variant
from django_tables2 import columns


class StockTable(BaseTable):
    physical = columns.TemplateColumn(
        """
        
        <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#stock-physical{{record.id}}">
        {{record.physical_count}}
        </button>
        """,
        orderable=False,
    )
    transit = columns.TemplateColumn(
        """
        
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#stock-transit{{record.id}}">
        {{record.transit_count}}
        </button>
        """,
        orderable=False,
    )

    action = None

    created = None
    back_orders_count = columns.Column(verbose_name="Back Order", orderable=False)

    class Meta:
        model = Variant
        fields = ("car_model", "trim", "color", "vehicle_code", "physical", "transit", "back_orders_count")


class StockListTable(BaseTable):
    action = columns.TemplateColumn(
        """
       
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            {% if request.user.usertype == 'pdi' %}
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Update</a></li>
            {% else %}
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Update</a></li>
                <li><a class="dropdown-item" href="{{record.get_delete_url}}">Delete</a></li>
            {% endif %}
            </ul>
        </div>
        
        
        """,
        orderable=False,
    )

    class Meta:
        model = Stock
        fields = ("variant", "chassis_number", "bs_type", "age", "status", "allocation_status")
        attrs = {"class": "table key-buttons border-bottom table-hover table-striped table-bordered"}


class PriceListTable(BaseTable):
    created = None

    class Meta:
        model = Variant
        fields = (
            "vehicle_code",
            "car_model",
            "trim",
            "color",
            "showroom_price",
            "insurance",
            "road_tax",
            "registration_charge",
            "tcs",
            "rsa",
            "p2p",
            "extended_warranty",
        )
        attrs = {"class": "table key-buttons border-bottom table-hover stocktable table-striped table-bordered"}
