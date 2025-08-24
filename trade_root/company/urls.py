from django.urls import path


#views
from .views import CompanyListView , CompanyCreateView , CompanyUpdateInfoView

urlpatterns = [
    path('',CompanyListView.as_view(),name="list-companies"),
    path('create',CompanyCreateView.as_view(),name="create-company"),
    path('<int:company_id>/update',CompanyUpdateInfoView.as_view(),name="update-company"),
]