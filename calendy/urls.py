from django.urls import path
from .views import ContactFormCreateView

urlpatterns = [
    path('email-send/', ContactFormCreateView.as_view(), name='contact-submit'),
]