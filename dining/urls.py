from django.urls import path

from dining import views

urlpatterns = [
    path('test/', views.test),
    path('program/<program_id>/receipt/', views.receipt)
]
