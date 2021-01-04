from . import views
from django.urls import path


urlpatterns = [
    # path('', views.home, name='home'),
    path('list_item/', views.list_item, name='list_item'),
    path('add_items/', views.add_items, name='add_items'),
    path('add_category/', views.add_category, name='add_category'),
    path('select_item/', views.select_item, name="select_item"),
    path('update_items/<str:pk>/', views.update_items, name="update_items"),
    path('delete_items/<str:pk>/', views.delete_items, name="delete_items"),
    path('approve_items/<str:pk>/', views.approve_items, name="approve_items"),
    path('stock_detail/<str:pk>/', views.stock_detail, name="stock_detail"),
    path('request_items/<str:pk>/', views.request_items, name="request_items"),
    path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),
    path('list_approval/', views.list_approval, name='list_approval'),
    path('reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
    path('list_history/', views.list_history, name='list_history'),
    path('request_list_history/', views.request_list_history, name='request_list_history'),
]