from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path

from shop import views

urlpatterns = [
    path('customer/', views.CustomerList.as_view(), name='customer-list'),
    path('customer/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail'),
    path('category/', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('product/', views.ProductList.as_view(), name='product-list'),
    path('product/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
    path('order/', views.OrderList.as_view(), name='order-list'),
    path('order/<int:pk>', views.OrderDetail.as_view(), name='order-detail'),
    path('order-item/', views.OrderItemList.as_view(), name='order-item-list'),
] + debug_toolbar_urls()
