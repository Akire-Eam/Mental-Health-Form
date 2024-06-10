from django.urls import path
from . import views


urlpatterns = [
    path('createpsychologist/', views.addNurse),
    path('createpsychiatrist/', views.addDoctor),
    path('checkusercheck/<roledata>' ,views.doctor_register),
    path('loginpage' , views.docter_login),
    path('logout' , views.doctor_logout),
    path('choise/', views.choiseview)
]