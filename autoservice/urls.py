from django.urls import path
from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>', views.car, name='car'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("myorders/", views.MyOrdersListView.as_view(), name="myorders"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path("orders/create/", views.OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:pk>/update/", views.OrderUpdateView.as_view(), name="order-update"),
    path("orders/<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order-delete"),
    path("order/<int:pk>/add_line/", views.OrderLineCreateView.as_view(), name="order-line-create"),
    path("order_line/<int:pk>/update/", views.OrderLineUpdateView.as_view(), name="order-line-update"),
    path("order_line/<int:pk>/delete/", views.OrderLineDeleteView.as_view(), name="order-line-delete"),
]