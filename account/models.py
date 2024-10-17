from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


# Create ProFile 
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile' , on_delete=models.CASCADE)
    reset_password_token = models.CharField( max_length=50 , default="" , blank=True)
    reset_password_expire = models.DateTimeField(blank=True , null=True)
    
    

#  لازم يتم عمل ملف شخص الها اليا  register المستخدم يلي نصنعها اتوماتيكا يصنع ملغ شخصي تلها يعني اما يعمل 
#  signals : لما تعمل حستب جديد نلقائيا يرسل اشارة لصنع ملف شخصي 
# @receiver(post_save, sender=User)
# def save_profile(sender, instance , created  ,**kwargs):
    
#     print('instace',instance)
#     user=instance
#     if created:# بعد ما تم صنعتها 
#         profile =  Profile(user=user) # البيانات تجي من المستخدم
#         profile.save()
        
@receiver(post_save, sender=User)
def save_profile(sender,instance, created, **kwargs):

    print('instance',instance)
    user = instance

    if created:
        profile = Profile(user = user)
        profile.save()
     
 
   