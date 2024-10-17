from django.db import models
from django.contrib.auth.models import User
# Create your models here.

    
# choices
class Category(models.TextChoices):
    COMPUTERS = 'computers'
    FOOD      = 'food'
    KIDS      = 'kids'
    HOME      = 'home'



class Product(models.Model):
    name = models.CharField(max_length=200 , default="" , blank= False  )
    description = models.TextField(max_length=1000 , default="" ,  blank=False )
    price = models.DecimalField(max_digits=7 , decimal_places=2, default=0 )
    brand = models.CharField(max_length=200 , default="" , blank= False  )
    category  = models.CharField(max_length=40  , blank= False , choices=Category.choices  )
    ratings = models.DecimalField(max_digits=3 , decimal_places=2, default=0  )
    stock  = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add =True  )
    user  = models.ForeignKey(User ,  null=True, on_delete=models.SET_NULL )

    def __str__(self):
        return self.name



# review :   لما يحي المستخدم يحاول يعطي تفيم المنتج
# عمل تفيم 
class Review(models.Model):
    product  = models.ForeignKey(Product ,  null=True, on_delete=models.CASCADE , related_name='reviews' )  # بدي اعرف اي مستخد قيم على انو منتج  # CASCADE  لانو اذا حذفت المنتج ليش يبقى التقيم 
    user  = models.ForeignKey(User ,  null=True, on_delete=models.SET_NULL )  # مين قيم على هذا المنتح 
    name = models.CharField(max_length=200 , default="" , blank= False  )
    rating  = models.IntegerField(default=0)
    comment = models.TextField(max_length=1000 , default="" ,  blank=False )
    createdAt = models.DateTimeField(auto_now_add =True  )

    def __str__(self):
        return self.comment