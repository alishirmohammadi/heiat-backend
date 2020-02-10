from django.urls import path

from dining import views

urlpatterns = [
    path('test/', views.test),
    path('receipt/<eskan>/', views.receipt),
    path('history/<eskan>/', views.status),
    path('program/<program_id>/', views.status)
]
