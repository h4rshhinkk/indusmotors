from core.base import BaseAdmin

from .models import CarModel, Tellecaller
from .models import Color
from .models import CorpScheme
from .models import FinancingCategory
from .models import Fuel
from .models import LostReason
from .models import LostSubReason
from .models import OpportunitySource
from .models import Profession
from .models import Stock
from .models import Transmission
from .models import Trim
from .models import Variant
from .models import State
from .models import District
from .models import Discount
from .models import Accessory
from .models import Rto
from .models import Document
from .models import ExchangeVehicleBrand
from django.contrib import admin


@admin.register(Document)
class DocumentAdmin(BaseAdmin):
    list_display = ("name","department", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(ExchangeVehicleBrand)
class ExchangeVehicleBrandAdmin(BaseAdmin):
    list_display = ("name","is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(Rto)
class RtoAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Accessory)
class AccessoryAdmin(BaseAdmin):
    list_display = ("accessory_type", "name", "is_active")
    list_filter = ("is_active", "accessory_type")
    search_fields = ("name",)


@admin.register(Discount)
class DiscountAdmin(BaseAdmin):
    list_display = ("discount_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("discount_name",)


@admin.register(CarModel)
class CarModelAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Color)
class ColorAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Fuel)
class FuelAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Trim)
class TrimAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Transmission)
class TransmissionAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Variant)
class VariantAdmin(BaseAdmin):
    list_display = ("vehicle_code", "car_model", "fuel", "trim", "color", "transmission", "is_active")
    list_filter = ("car_model", "fuel", "trim", "color", "transmission", "is_active")
    search_fields = ("vehicle_code", "car_model__name", "fuel__name", "trim__name", "color__name", "transmission__name")
    ordering = ("car_model",)


@admin.register(Profession)
class ProfessionAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(OpportunitySource)
class OpportunitySourceAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Stock)
class StockAdmin(BaseAdmin):
    list_display = ("chassis_number", "is_active", "variant", "bs_type", "allocation_status", "is_chassis_blocked")
    list_filter = ("is_active", "is_chassis_blocked", "variant__car_model")
    search_fields = ("chassis_number",)
    autocomplete_fields = ("variant",)


@admin.register(FinancingCategory)
class FinancingCategoryAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(LostReason)
class LostReasonAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(LostSubReason)
class LostSubReasonAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(CorpScheme)
class CorpSchemeAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(State)
class StateAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(District)
class DistrictAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Tellecaller)
class TellecallerAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)