from django.urls import path

from .views import profile_view, api_profile

urlpatterns = [
    path('', profile_view, name='profile'),
    path('api_profile/', api_profile, name='api_profile'),
]