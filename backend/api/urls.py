from django.urls import path
from . import views

urlpatterns = [
    path('purchase/', views.purchase, name='purchase'),
    path('analytics/', views.analytics, name='analytics'),
    path('products/', views.products_list, name='products_list'),
    path('checkout/', views.checkout, name='checkout'),
]
