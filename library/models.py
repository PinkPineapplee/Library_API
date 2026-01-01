from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField(default = 1)

    def __str__(self):
     return f"{self.title} by {self.author}"
    


class Transaction(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     book = models.ForeignKey(Book, on_delete=models.CASCADE)
     checked_out_at = models.DateTimeField(auto_now_add=True)
     returned_at = models.DateTimeField(null=True, blank=True)

     class Meta:
         unique_together = ("user", "book", "returned_at")

     def __str__(self):
         return f"{self.user.username} - {self.book.title}"    
    