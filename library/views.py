from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Book, Transaction



class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()

        # Optional query params
        available = self.request.query_params.get("available")
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        isbn = self.request.query_params.get("isbn")

        # Filter by availability
        if available == "true":
            queryset = queryset.filter(copies_available__gt=0)


             # Search filters
        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            queryset = queryset.filter(author__icontains=author)

        if isbn:
            queryset = queryset.filter(isbn__icontains=isbn)

        return queryset
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'date_joined']


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
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class CheckoutBookAPIView(APIView):
    def post(self, request, book_id):
        user = request.user


        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)


        if book.copies_available < 1:
            return Response({"error": "No copies available"}, status=400)


        already_borrowed = Transaction.objects.filter(
            user=user,
            book=book,
            returned_at__isnull=True
        ).exists()


        if already_borrowed:
            return Response({"error": "You already borrowed this book"}, status=400)

        Transaction.objects.create(user=user, book=book)
        book.copies_available -= 1
        book.save()


        return Response({"message": "Book checked out successfully"}, status=200)


class ReturnBookAPIView(APIView):
    def post(self, request, book_id):
        user = request.user


        try:
            transaction = Transaction.objects.get(
                user=user,
                book_id=book_id,
                returned_at__isnull=True
            )  
        except Transaction.DoesNotExist:
            return Response({"error": "No active checkout found"}, status=400)

        transaction.returned_at = timezone.now()
        transaction.save()

        book = transaction.book
        book.copies_available += 1
        book.save()

        return Response({"message": "Book returned successfully"}, status=200)
                  
class BookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()

        # filter by availability
        available = self.request.query_params.get('available')
        if available == 'true':
            queryset = queryset.filter(copies_available__gt=0)

        # search query
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(isbn__icontains=search)
            )

        return queryset

