from django.urls import path
from . import views


urlpatterns = [
    path('', views.airline_form, name='airline_form'),
    path('process-speech/', views.process_speech, name='process_speech'),
    path('submit-booking/', views.submit_booking, name='submit_booking'),
]
