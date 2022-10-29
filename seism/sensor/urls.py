from django.urls import path

from . import views

app_name = 'sensor'
urlpatterns = [
    path('', views.startpage, name = 'sensorviwer'),
    path('showsens/', views.showsens, name = 'showsens'),
    path('ajaxpost/', views.ajaxpost, name = 'ajaxpost'),
    path('ajaxdel/', views.ajaxdel, name = 'ajaxdel'),
]