from django.urls import path

from .views import number_input_view, api_number_input, api_otp_input, otp_input_view, logout_view


urlpatterns = [
    path('number_input/', number_input_view, name='authentication_number_input'),
    path('api_number_input/', api_number_input, name='api_authentication_number_input'),
    path('otp_input/', otp_input_view, name='authentication_otp_input'),
    path('api_otp_input/', api_otp_input, name='api_authentication_otp_input'),
    path('logout/', logout_view, name='logout'),
]
