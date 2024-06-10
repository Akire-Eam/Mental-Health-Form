from django.contrib import admin
from django.urls import path
from healthcare import views

urlpatterns = [
    path('newPatient', views.newPatient, name='newPatient'),
    path('updatePatient/<patientId>', views.updatePatient, name='updatePatient'),
    path('patientRecord/<patientId>', views.patientRecord, name='patientRecord'),
    path('updatePatientRecord/<patientId>', views.updatePatientRecord, name='updatePatientRecord'),
    path('treatmentPlan/<patientId>', views.treatmentPlan, name='treatmentPlan'),
    path('counselling/<patientId>', views.counselling, name='counselling')
]
