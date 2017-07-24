from django.conf.urls import url
from .views import signup_view

urlpatterns = [
    url('',signup_view),
]