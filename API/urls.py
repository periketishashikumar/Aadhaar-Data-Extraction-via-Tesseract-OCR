from django.urls import path
from .views import *
urlpatterns= [
    path("adhaar_details",adhaar,name="adhaar_details")
]