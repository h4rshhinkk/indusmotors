from core.base import BaseTable
from crm.models import BookingRequest

from django_tables2 import columns


class BookingRequestTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{{record.get_absolute_url}}">View Order</a></li>
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Update Order</a></li>
                
            </ul>
        </div>
        
        """,
        orderable=False,
    )

    variant = columns.TemplateColumn(
        """
        {{record.car_model}}<br>
        {{record.variant.fuel}}<br> 
        {{record.variant.trim}}<br>
        {{record.variant.transmission}}<br>
        {{record.variant.color}}<br>
        {{record.variant}}
        
        """,
        orderable=False,
        verbose_name="Vehicle Details",
    )

    class Meta:
        model = BookingRequest
        fields = ("opportunity", "opportunity__place", "variant")
        attrs = {"class": "table key-buttons border-bottom table-hover"}
