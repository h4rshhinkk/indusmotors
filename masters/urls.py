from . import views
from django.urls import path


app_name = "masters"

urlpatterns = [
    path("stocklist/", views.StockListView.as_view(), name="stock_list"),
    path("stock-report/list/", views.StockReportListView.as_view(), name="stock_report_list"),
    path("new/stock/", views.StockCreateView.as_view(), name="stock_create"),
    path("stock/<str:pk>/update/", views.StockUpdateView.as_view(), name="stock_update"),
    path("stock/<str:pk>/delete/", views.StockDeleteView.as_view(), name="stock_delete"),
    path("price_list/", views.PriceList.as_view(), name="price_list"),
    path("variant/<str:pk>/detail/", views.VariantDetailView.as_view(), name="variant_detail"),
    path("variant/<str:pk>/update/", views.VariantUpdateView.as_view(), name="variant_update"),
]
