from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PostiveIntegerField(default = 1)

def __str__(self):
    return f"{self.title} by {self.author}"
    

class User(models.Model):
    ID = models.primarykey
    Username = models.CharField(max_length= 255, unique= True)
    Email = models.CharField(max_length= 255, unique =True)  
    Date_of_Membership = models.DateField()
    Active_Status = models.BooleanField()  

def __str__(self):
    return f"{self.Username}"  



class Transactions(models.Model):
     book = models.ForeignKey(Book, on_delete=models.CASCADE)
     student = models.ForeignKey(User, on_delete=models.CASCADE)
     check_out_date = models.DateField()
     return_date = models.DateField(null=True, blank=True)

def __str__(self):
    return f"{self.student}"    