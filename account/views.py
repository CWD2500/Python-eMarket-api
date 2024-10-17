
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers  import make_password
from rest_framework import status
from .serializers import SignUPSerializer , UserSerializer
from rest_framework.permissions import IsAuthenticated
# libery ProFile Email
from django.utils.crypto import get_random_string

from django.core.mail import  send_mail  
# Create your views here.

@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUPSerializer(data= data)
    
    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():  #  اتخقق انو مانو مسجل مسبقا 
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'], 
                email  = data['email'], 
                username= data['email'],
                password = make_password(data['password'])
            )
            return Response({'details':'Your Account Registerd SeccessFully!'} , status= status.HTTP_201_CREATED)
        else:
            return Response({'error':'This email already exists!'} , status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)


# Show a ProFile
#   التاكدي من انو انت اعمل تسحيل وبدكل تشوف المعلومات تبع ال مسجل  
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def  current_user(request):
    user = UserSerializer(request.user , many=False)
    return Response(user.data)



# Update ProFile User => IF Login 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def  update_user(request):
    user = request.user  # Login 
    data = request.data
    
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.username = data['email']
    
    # if data['password'] != " ":
    #     user.password = make_password(data['password'])
         
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)



# =============================
#  reset  يولد رابط تبع ال 
def get_current_host(request):
    protocol = request.is_seucre() and 'https' or 'https'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol , host=host)
    #  مقال :  https/host/


#  Create ProFile And Foreget Email 
# @api_view(['POST'])
# def foreget_password(request):
#     data = request.data 
#     user = get_object_or_404(User , email=data['email'])
#     token = get_random_string(40)
#     exprire_date = datetime.now()+ timedelta(minutes=30)     # هذا الرابط يلي نسرهل تبع نسيت كلمة المرور لازك يكوم الها وقت انتها ء
#     user.profile.reset_password_token  = token  # profile : realted_name : Models
#     user.profile.reset_password_expire  = exprire_date 
#     user.profile.save()
#     host = get_current_host(request)
#     # link = "{host}api/reset_password/token" # طريقة اول يكون الرابط ديناميكي 
#     link = "http:localhost:8000/api/reset_password/token"   # طريقة تانية يكون الرابط ثابت 
#     body = "Your password reset link is : {link}".format(link=link)
#     send_mail(
#         "password reset form eMarket ",
#         body,
#         "eMarket@gmail.com",
#         [data['email']] # resetيلي هوي يطلب ال   email 
#     )
    
#     return Response({"details":"Password reset send to {email}".format(email=data['email'])})
    

@api_view(['POST']) 
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User,email=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()
    
    host = get_current_host(request)
    link = "http://localhost:8000/api/reset_password/{token}".format(token=token)
    body = "Your password reset link is : {link}".format(link=link)
    send_mail(
        "Paswword reset from eMarket",
        body,
        "eMarket@gmail.com",
        [data['email']]
    )
    return Response({'details': 'Password reset sent to {email}'.format(email=data['email'])})


@api_view(['POST']) 
def reset_password(request , token):
    data = request.data
    user = get_object_or_404(User,profile__reset_password_token=token)
    
    #  هاد الرابط يلي ام ارسالها ألك اذا مر عليها فترة  طويل ة   reset  في حالة ال 
    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now(): 
        return Response({"error":'Token is expire ..!'} , status=status.HTTP_400_BAD_REQUEST)
     #exipre بالتالي رح يكون  reset وخلا الفترة ماملت  token   اذا تم ارسال ال 
    
    #data =  request.data  => data['password']
    if data['password'] != data['confirmPassword']:
        return Response({"error":"password are to not  same"})
    
    
    
    
    # Save Password
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()
    
    return Response({'details': 'Password reset Done ...! '})

 
