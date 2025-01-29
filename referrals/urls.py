from django.urls import path

from .views import invite_code_activation_view, api_invite_code_activation


urlpatterns = [
    path('invite_code_activation/', invite_code_activation_view, name='invite_code_activation'),
    path('api_invite_code_activation/', api_invite_code_activation, name='api_invite_code_activation'),
]
