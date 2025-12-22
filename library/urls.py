from django.urls import path, include
from .views import (BookListView, UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView, CheckoutBookAPIView, ReturnBookAPIView, BookInventoryCreateAPIView, BookShowUpdateDestroyAPIView)

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", BookInventoryCreateAPIView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookShowUpdateDestroyAPIView.as_view(), name= "book-detail"),
    path('users/', UserListCreateAPIView.as_view()),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view()),
    path('books/<int:book_id>/checkout/', CheckoutBookAPIView.as_view()),
    path('books/<int:book_id>/return/', ReturnBookAPIView.as_view()),
    path('library/', include('library.urls')),
    path("books/", BookListView.as_view(), name="book-list"),
]