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
    # path('treatmentPlan/<patientId>', views.treatmentPlan, name='treatmentPlan'),
    # path('treatmentPlan/<patientId>', views.treatmentPlan, name='treatmentPlan'),
    path('counselling/<patientId>', views.counselling, name='counselling'),
    # path('updateCounselling/<patientId>/<formId>', views.updateCounselling, name='updateCounselling')
    path('updateCounselling/<int:patientId>/<int:formId>/', views.updateCounselling, name='updateCounselling')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
