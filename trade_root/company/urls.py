from django.urls import path


#views
from .views import CompanyListView , CompanyCreateView , CompanyUpdateInfoView

urlpatterns = [
    path('company/',CompanyListView.as_view(),name="list-companies"),
    path('company/create',CompanyCreateView.as_view(),name="create-company"),
    path('company/<int:company_id>/update',CompanyUpdateInfoView.as_view(),name="update-company"),
]