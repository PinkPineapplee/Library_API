from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Book, Transaction




def index(request):
    return JsonResponse({"message": "Welcome to the Library API"})
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
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Get / Update/ Delete a single book
class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
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
    permission_classes = [IsAuthenticated]


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
    permission_classes = [IsAuthenticated]


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

class MyTransactionsAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class LibrarianChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get("message", "").lower().strip()
        user = request.user

        if not message:
            return Response({
                "reply": "Please type a question so I can help you."
            }, status=400)

        # 1. Borrowing instructions
        if "borrow" in message or "checkout" in message:
            return Response({
                "reply": "To borrow a book, go to the book list and use the checkout endpoint for the book you want."
            })

        # 2. Returning instructions
        if "return" in message:
            return Response({
                "reply": "To return a book, use the return endpoint for the book you borrowed."
            })

        # 3. Available books
        if "available" in message:
            count = Book.objects.filter(copies_available__gt=0).count()
            return Response({
                "reply": f"There are {count} books currently available."
            })

        # 4. Author search
        if "author" in message:
            words = message.split()
            author_name = words[-1]

            books = Book.objects.filter(author__icontains=author_name)
            if books.exists():
                titles = [book.title for book in books]
                return Response({
                    "reply": f"Books by {author_name}: {', '.join(titles)}"
                })

            return Response({
                "reply": f"No books found by {author_name}."
            })

        # 5. Overdue warning
        overdue = Transaction.objects.filter(
            user=user,
            returned_at__isnull=True,
            due_date__lt=timezone.now()
        ).exists()

        if overdue:
            return Response({
                "reply": "You currently have overdue books. Please return them before borrowing new ones."
            })

        # Fallback response
        return Response({
            "reply": "I'm the librarian bot. I can help you find books, explain borrowing rules, or check availability."
        })
