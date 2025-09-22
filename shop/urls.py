from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path

from shop import views

urlpatterns = [
    path('customer/', views.CustomerList.as_view(), name='customer-list'),
    path('customer/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail')
    # path('category/', views.CategoryList.as_view(), name='category-list'),
    # path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
] + debug_toolbar_urls()
