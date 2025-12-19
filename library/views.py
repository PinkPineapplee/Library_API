from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Book, User
from .serializers import BookSerializer, UserSerializer

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# List all books / create new book
class BookInventoryCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer = BookSerializer

# Get / Update/ Delete a single book
class BookShowUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer = UserSerializer

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer = UserSerializer
