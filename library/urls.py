from django.urls import path
from .views import BookInventoryCreateAPIView, BookShowUpdateDestroyAPIView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", BookInventoryCreateAPIView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookShowUpdateDestroyAPIView.as_view(), name= "book-detail"),
]