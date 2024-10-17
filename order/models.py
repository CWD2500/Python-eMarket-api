from django.db import models
from operator import mod   #  ماجل يعني باقي القسمة
from django.contrib.auth.models import  User  # حتى نعرف اي مستخدم عمل طلب 
from product.models import  Product
# Create your models here.


#   يكون في ثلاث مراحل  order  غي ال 
#  1 :  PROCESSING  المعالجة
#  2 : SHIPPET : يلي هوي  تم ارسالها لي شخص 
#  3 : DELIVERD : يلي هوي استلام الطلب 

class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing'
    SHIPPET    =  'Shippet'
    DELIVERD   = 'Deliverd'
    

# يعني تم دفعها او لم يتم الدفع
class PaymentStatus(models.TextChoices):
    PAID = 'Paid'
    UNPAID    =  'Unpaid'
    
    
# الية الدقع كاش او الكتروني يعني فيزا كارت
class PaymentMode(models.TextChoices):
    COD = 'Cod'  # دفع بي اليد 
    CARD ='Card' # دفع الكتروني 
    
    

class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=400, default="", blank=False)
    zip_code = models.CharField(max_length=100, default="", blank=False)
    street = models.CharField(max_length=500, default="", blank=False)
    state = models.CharField(max_length=100, default="", blank=False)
    country = models.CharField(max_length=100, default="", blank=False)
    phone_no = models.CharField(max_length=100, default="", blank=False)
    total_amount = models.IntegerField( default=0 )
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_mode = models.CharField(max_length=30, choices=PaymentMode.choices, default=PaymentMode.COD)
    status = models.CharField(max_length=60, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)

    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


#  order and product الية الربط بين ال 


class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE,related_name='orderitems')# related_name  كم عنصر قام بطلبها 
    name = models.CharField(max_length=200, default="", blank=False)
    quantity = models.IntegerField( default=1 )
    price = models.DecimalField( max_digits=7, decimal_places=2,blank=False )

    def __str__(self):
        return self.name

    
