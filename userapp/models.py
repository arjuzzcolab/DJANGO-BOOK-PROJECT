from django.db import models
from accounts.models import loginTable
# Create your models here.
from bookapp.models import Book,Author
class Cart(models.Model):
    user = models.OneToOneField(loginTable,on_delete=models.CASCADE)
    items = models.ManyToManyField(Book)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
