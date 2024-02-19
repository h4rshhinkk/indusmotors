from core.base import BaseModel

from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone

from crm.models import BookingRequest


class CarModel(BaseModel):
    LOB_CHOICES = [('EVBU', 'EVBU'), ('Cars', 'Cars'), ('UVs', 'UVs')]
    lob = models.CharField(max_length=128, null=True, choices=LOB_CHOICES)
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)


class Fuel(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)


class Trim(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)


class Color(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)


class Transmission(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)


class Variant(BaseModel):
    vehicle_code = models.CharField(max_length=128)
    car_model = models.ForeignKey('CarModel', on_delete=models.PROTECT)
    fuel = models.ForeignKey('Fuel', on_delete=models.PROTECT)
    trim = models.ForeignKey('Trim', on_delete=models.PROTECT)
    color = models.ForeignKey('Color', on_delete=models.PROTECT)
    transmission = models.ForeignKey('Transmission', on_delete=models.PROTECT)
    # price
    showroom_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    insurance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    road_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    registration_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tcs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rsa = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    p2p = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extended_warranty = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.vehicle_code} ({self.car_model.name})"

    def get_stocks(self):
        return Stock.objects.filter(variant=self, is_active=True)

    def get_physical(self):
        return self.stock_status_count('Physical')

    def get_transit(self):
        return self.stock_status_count('Transit')

    def stock_status_count(self, status):
        return self.stock_set.filter(status=status, is_chassis_blocked=False)

    def transit_count(self):
        return self.stock_status_count('Transit').count()

    def physical_count(self):
        return self.stock_status_count('Physical').count()

    def back_orders_count(self):
        return BookingRequest.objects.filter(variant=self, is_active=True, stage='back_order_requested').count()

    def get_absolute_url(self):
        return reverse_lazy('masters:variant_detail', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse_lazy('masters:variant_update', kwargs={'pk': self.id})


class Stock(BaseModel):
    STATUS_CHOICES = [('Transit', 'Transit'), ('Physical', 'Received - OK'), ('Testdrive', 'Test Drive Vehicle'), ('Blocked', 'Blocked')]
    DISPLAY_STATUS_CHOICES = [('ready_for_sale', 'Ready For Sale'), ('display', 'Display')]
    BS_CHOICES = [('BS1', 'BS I'), ('BS2', 'BS II'), ('BS3', 'BS III'), ('BS4', 'BS IV'), ('BS5', 'BS V'), ('BS6', 'BS VI'), ('NA', 'NA')]
    ALLOCATION_CHOICES = [('option 1', 'Option 1'), ('option 2', 'Option 2')]

    variant = models.ForeignKey('masters.Variant', on_delete=models.PROTECT)
    chassis_number = models.CharField(max_length=128)
    bs_type = models.CharField(max_length=128, choices=BS_CHOICES)
    status = models.CharField(max_length=128, choices=STATUS_CHOICES)
    allocation_status = models.CharField(null=True, blank=True, max_length=128, choices=ALLOCATION_CHOICES)
    tm_invoice_date = models.DateField(null=True, blank=True)
    product_description = models.CharField(max_length=128, null=True, blank=True)
    dealer_purchase_order_price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    engine_no = models.CharField(max_length=128, null=True, blank=True)
    key_no = models.CharField(max_length=128, null=True, blank=True)
    manufacturing_date = models.DateField(null=True, blank=True)
    sales_order_no = models.CharField(max_length=128, null=True, blank=True)
    dealer_location = models.CharField(max_length=128, null=True, blank=True)
    transferred_date = models.DateField(null=True, blank=True)
    display_status = models.CharField(max_length=128, null=True, blank=True, choices=DISPLAY_STATUS_CHOICES)
    transit_date = models.DateField(null=True, blank=True)
    is_chassis_blocked = models.BooleanField("Is Chassis Blocked(Tick to Block)",default=False)

    def __str__(self):
        age_in_days = self.age()  # Calculate the age in days
        age_str = f"{age_in_days} days" if age_in_days is not None else "Unknown age"
        return f"{self.chassis_number} - {age_str}"

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    def age(self):
        if self.manufacturing_date:
            today = timezone.now().date()
            age_delta = today - self.manufacturing_date
            return age_delta.days
        return None  # or return a default value if manufacturing_date is None

    @staticmethod
    def get_list_url():
        return reverse_lazy("masters:stock_list")

    def get_update_url(self):
        return reverse_lazy("masters:stock_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("masters:stock_delete", kwargs={"pk": self.pk})

    @staticmethod
    def get_transit_count():
        return Stock.objects.filter(status='Transit').count()

    @staticmethod
    def get_physical_count():
        return Stock.objects.filter(status='Physical').count()


class Profession(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)


class OpportunitySource(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)


class FinancingCategory(BaseModel):
    name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = "Financing Category"
        verbose_name_plural = "Financing Categories"

    def __str__(self):
        return str(self.name)


class LostReason(BaseModel):
    name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class LostSubReason(BaseModel):
    reason = models.ForeignKey('masters.LostReason', related_name="sub_reason", on_delete=models.PROTECT)
    name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.reason.name})"


class CorpScheme(BaseModel):
    name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = "Corp Scheme"
        verbose_name_plural = "Corp Schemes"

    def __str__(self):
        return str(self.name)


class State(BaseModel):
    name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class District(BaseModel):
    state = models.ForeignKey('masters.State', related_name="state", on_delete=models.PROTECT)
    name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.state.name})"


class Accessory(BaseModel):
    ACCESSORY_CHOICES = [('TMGA', 'TMGA'), ('VAS', 'VAS')]
    accessory_type = models.CharField(max_length=20, choices=ACCESSORY_CHOICES)
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Accessory"
        verbose_name_plural = "Accessories"

    def __str__(self):
        return f"{self.name} ({self.accessory_type})"


class Discount(BaseModel):
    discount_name = models.CharField(max_length=128)

    def __str__(self):
        return self.discount_name


class Rto(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Document(BaseModel):
    DOC_DEPT = [('registration', 'Registration'), ('scheme', 'Scheme'), ('exchange', 'Exchange'),]
    name = models.CharField(max_length=128)
    department = models.CharField(max_length=128, choices=DOC_DEPT,blank=True, null=True)

    def __str__(self):
        return self.name

class ExchangeVehicleBrand(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    

class Tellecaller(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name