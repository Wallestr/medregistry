from django.urls import path

from registry import views

urlpatterns = [
    path("", views.home, name="home"),
    path("patients/", views.patient_list, name="patient_list"),
    path("patients/<int:pk>/", views.patient_detail, name="patient_detail"),
    path("immunizations/", views.immunization_journal, name="immunization_journal"),
]
