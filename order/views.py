from django.shortcuts import   get_object_or_404
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from product.models import Product
from .serializers import OrderSerializer
from .models import Order  , OrderItem

# get All Orders
@api_view(['GET'])
@permission_classes({IsAuthenticated})
def get_order(request):
    order = Order.objects.all()
    serizlizer  = OrderSerializer(order , many=True)
    return Response({"Order :":serizlizer.data})


# get Order id
@api_view(['GET'])
@permission_classes({IsAuthenticated})
def get_order_id(request , pk):
    order = get_object_or_404(Order , id=pk)
    serizlizer  = OrderSerializer(order , many=False)
    return Response({"Order :":serizlizer.data})


# Update Order 
@api_view(['PUT'])
@permission_classes({IsAuthenticated})
def get_order_update(request , pk):
    order = get_object_or_404(Order , id=pk)
    order.status = request.data['status'] # المستخدم هوي يرسل الحلة ونحنا نعدل حسبها 
    order.save()
    serizlizer  = OrderSerializer(order , many=False)
    return Response({"Order :":serizlizer.data})



# delete order 
@api_view(['DELETE'])

@permission_classes({IsAuthenticated,IsAdminUser})
def get_order_delete(request , pk):
    order = get_object_or_404(Order , id=pk)
    order.status = request.data['status'] # المستخدم هوي يرسل الحلة ونحنا نعدل حسبها 
    order.delete()
    
    return Response({"details :Order Is deleted"})




# new Order 
@api_view(['POST'])
@permission_classes({IsAuthenticated})
def new_order(request):
    print(request.user)
    user =request.data # يدي اعرف منو الشخث يلي عامل تسجيل دخول 
    data  = request.data # get Data
    order_items = data['order_Items']
    
    if order_items and len(order_items) == 0:
        return Response({"error" : 'No Order recieved'} , status=status.HTTP_400_BAD_REQUEST)
    else:
        total_amount = sum( item['price']* item['quantity'] for item in order_items)
        # get Data User

        order = Order.objects.create(
            user = user,
            city = data['city'],
            zip_code = data['zip_code'],
            street = data['street'],
            phone_no = data['phone_no'],
            country = data['country'],
            total_amount = total_amount,
        )
        
        #  بدنا نعرف كل عنصر انت اشتريت من المنتح 
        for i in order_items:
            product  = Product.objects.get(id=i['product'])
            item  = OrderItem.objects.create(
                product = product ,
                order  = order,
                name = product.name,
                quantity = i['quantity'],
                price = i['price'],
            )
            #  تنفص من المخزون تبع المنتجات بحال انو اشنرا  منتج يعني عمل عليها طلب
            product.stock -= item.quantity
            product.save()
            # serializer بعد ما حفضة ارسال الى ال 
            # order: obj هي جاي من   objecy   هدا يتعبر 
            serialzer =  OrderSerializer(order , many=False)  # رخ اسر لي شخص ةاحد
            return Response(serialzer.data)
        
        
