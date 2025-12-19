from rest_framework import serializers
from .models import Book, User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'copies_available']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'Username', 'Email','Date_of_Membership', 'Active_Status']
