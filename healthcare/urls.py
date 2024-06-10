from django.contrib import admin
from django.urls import path
from healthcare import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('newPatient', views.newPatient, name='newPatient'),
    path('updatePatient/<patientId>', views.updatePatient, name='updatePatient'),
    path('patientRecord/<patientId>', views.patientRecord, name='patientRecord'),
    path('consentForm/<patientId>', views.consentForm, name='consentForm'),
    path('updatePatientRecord/<patientId>', views.updatePatientRecord, name='updatePatientRecord'),
    path('updateConsentForm/<patientId>', views.updateConsentForm, name='updateConsentForm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
