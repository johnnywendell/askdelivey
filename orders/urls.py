from django.urls import path
from . import views as v


app_name = 'orders'
urlpatterns = [
    ### views api
    path('orders/dashboard/', v.OrdersDashboardView.as_view(), name='orders_dashboard'),
    path('orders/', v.OrderListAPIView.as_view(), name='orders-lists'),
    path('orders/create', v.CreateOrderAPIView.as_view()),
    path('<int:pk>/accept/',v.AcceptOrderAPIView.as_view(),name='accept_order'),
    
    
    ###views django
    path('orders/list/', v.OrderListView.as_view(), name='orders_list'),
    path('orders/criar/', v.OrderCreateView.as_view(), name='orders_criar'),
    path('orders/update/<uuid:public_id>/', v.OrderUpdateView.as_view(), name='order_update'),
    path('orders/detail/<uuid:public_id>/', v.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<uuid:public_id>/start-delivery/',
        v.OrderStartDeliveryView.as_view(),name='order_start_delivery'),
    path('orders/<uuid:public_id>/delivered/',
        v.OrderDeliveredView.as_view(),name='order_delivered'),
    path('orders/<uuid:public_id>/delivered/',
        v.OrderCanceledView.as_view(),name='order_canceled'),
    
]