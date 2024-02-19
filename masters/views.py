from core import mixins
from masters.forms import PdiupdatestockForm

from . import tables
from .models import Stock, Variant
from django.urls import reverse_lazy


class StockListView(mixins.HybridListView):
    model = Variant
    table_pagination = {"per_page": 500}
    table_class = tables.StockTable
    filterset_fields = {"car_model": ["exact"], "trim": ["exact"], "color": ["exact"]}
    template_name = "stock/stock_list.html"
    context_object_name = "variants"

    def get_queryset(self):
        # Get the distinct variants that have entries in the Stock model
        return Variant.objects.filter(stock__isnull=False).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Stock List"
        context["is_stock"] = True
        context["transit_count"] = Stock.objects.filter(
            is_active=True, is_chassis_blocked=False, status="Transit", variant__in=self.object_list
        ).count()
        context["physical_count"] = Stock.objects.filter(
            is_active=True, is_chassis_blocked=False, status="Physical", variant__in=self.object_list
        ).count()
        context["total_back_order"] = sum([i.back_orders_count() for i in self.object_list])
        return context


# class StockDetailView(mixins.HybridDetailView):
#     model = Variant
#     template_name = 'stock/stock_list.html'
#     table_class = tables.StockListTable
#     filterset_fields = ("status",)


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         variant = self.get_object()
#         stocks = variant.stock_set.all()  # Fetch related stocks for the variant
#         context['stocks_table'] = tables.StockListTable(stocks)  # Assuming you have a django-tables2 table for Stock
#         context["title"] = "Stock Report"
#         return context


class StockReportListView(mixins.HybridListView):
    model = Stock

    table_class = tables.StockListTable
    filterset_fields = {"status": ["exact"], "variant": ["exact"]}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Stock Report"
        context["can_add"] = True
        context["is_stock_report_list"] = True
        context["new_link"] = reverse_lazy("masters:stock_create")

        return context


class StockCreateView(mixins.HybridCreateView):
    model = Stock
    exclude = ("is_active", "is_chassis_blocked")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add New Stock"
        context["is_stock_create"] = True
        return context


class StockUpdateView(mixins.HybridUpdateView):
    model = Stock
    exclude = [ "is_active"]

    def get_form_class(self):
        usertype = self.request.user.usertype
        if usertype == "pdi":
            return PdiupdatestockForm
        return super().get_form_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Stock"
        return context


class StockDeleteView(mixins.HybridDeleteView):
    model = Stock


class PriceList(mixins.HybridListView):
    model = Variant
    table_class = tables.PriceListTable
    filterset_fields = ("car_model", "trim", "color")
    template_name = "stock/price_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Price List"
        context["is_price_list"] = True
        return context


class VariantDetailView(mixins.HybridDetailView):
    model = Variant
    template_name = "stock/vehicle_price_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Vehicle Details"
        return context


class VariantUpdateView(mixins.HybridUpdateView):
    model = Variant
    exclude = ("is_active",)

    def get_success_url(self):
        return reverse_lazy("masters:price_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Variant"
        return context


class VariantDeleteVIew(mixins.HybridDeleteView):
    model = Variant

    def get_success_url(self):
        return reverse_lazy("masters:price_list")
