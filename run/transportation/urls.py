from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_auction/', views.add_auction, name='add_auction'),

    path('auction_detail/<int:pk>/', views.auction_detail, name='auction_detail'),

    path('start_timer/<int:pk>/', views.start_timer, name='start_timer'),
    path('stop_timer/<int:pk>/', views.stop_timer, name='stop_timer'),

    path('auction_detail/take_step/<int:pk>/', views.take_step, name='take_step'),

]
