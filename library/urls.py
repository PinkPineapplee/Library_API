from django.urls import path
from .views import BookInventoryCreateAPIView, BookShowUpdateDestroyAPIView

from . import views

urlpatterns = [
    path("", views.index, name="index"),

]