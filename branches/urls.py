from . import views
from django.urls import path


app_name = "branches"

urlpatterns = [
    # Branch
    path("branch/list", views.BranchListView.as_view(), name="branch_list"),
    path("branch/<str:pk>/", views.BranchDetailView.as_view(), name="branch_detail"),
    path("new/branch/", views.BranchCreateView.as_view(), name="branch_create"),
    path("branch/<str:pk>/update/", views.BranchUpdateView.as_view(), name="branch_update"),
    path("branch/<str:pk>/delete/", views.BranchDeleteView.as_view(), name="branch_delete"),
]
