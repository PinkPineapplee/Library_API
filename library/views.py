from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

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
