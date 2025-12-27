from django.urls import path
from .views import (
    BookListCreateAPIView,
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    CheckoutBookAPIView,
    ReturnBookAPIView,
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    MyTransactionsAPIView)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path("books/", BookListCreateAPIView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookRetrieveUpdateDestroyAPIView.as_view(), name= "book-detail"),
    path('users/', UserListCreateAPIView.as_view(),  name="user-list"),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(),  name="user-detail"),
    path('books/<int:book_id>/checkout/', CheckoutBookAPIView.as_view(), name="checkout-book"),
    path('books/<int:book_id>/return/', ReturnBookAPIView.as_view(), name="return-book"),
    path("my-transactions/", MyTransactionsAPIView.as_view.as_view(), name="my-transactions"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]