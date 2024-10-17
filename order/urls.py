from django.urls import path
from . import views

urlpatterns = [
    path('orders/new/' , views.new_order  , name="new_order"),
    path('orders/' , views.get_order  , name="get_order"),
    path('orders/<str:pk>/' , views.get_order_id  , name="get_order_id"),
    path('orders/delete/<str:pk>/' , views.get_order_delete  , name="get_order_delete"),
    path('orders/update/<str:pk>/' , views.get_order_update  , name="get_order_update"),
]
