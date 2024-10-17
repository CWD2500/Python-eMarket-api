from django.shortcuts import render , get_object_or_404
from .models import Product , Review 
from .serializers import ProdductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .filters import ProductsFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models  import Avg
# Create your views here.


@api_view(['GET'])
def get_all_product(request):
    filterSet = ProductsFilter(request.GET , queryset=Product.objects.all().order_by('id'))
    count  = filterSet.qs.count()
    resPage = 12
    paginator  = PageNumberPagination()
    paginator.page_size = resPage
    # products  = Product.objects.all()
    queryset = paginator.paginate_queryset(filterSet.qs, request)
    # serializer = ProdductSerializer(filterSet.qs , many=True)  # json هي البينات يلي اجا من فاعدة البينات ترجمها على 
    serializer = ProdductSerializer(queryset, many=True)  # json هي البينات يلي اجا من فاعدة البينات ترجمها على 
    # print(filterSet)
    return Response({"Products":serializer.data , "per Page":resPage  ,  "count Page" :count})



# Search Product   APi
@api_view(['GET'])
def get_by_id_product(request , pk):
    products = get_object_or_404(Product, id=pk) # 404  غي حالة المنتج مو موجود اضهر ال  
    serializer =  ProdductSerializer(products  , many=False)
    print(products)
    return Response({"Products":serializer.data})



# Create Produvt  IF  Login 
@api_view(['POST'])
@permission_classes([IsAuthenticated])#  يلي ما عامل تسجيل مارح يطلع البيانات عنده
def new_product(request):
    data = request.data
    serializer =  ProdductSerializer(data=data)
    if serializer.is_valid():
        product = Product.objects.create(**data , user=request.user)
        res = ProdductSerializer(product,many=False)
        return Response({"Products":res.data})
    else:
        return Response({"serializer":serializer.errors})



# Update Product => IF Login 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])#  يلي ما عامل تسجيل مارح يطلع البيانات عنده
def update_product(request , pk):
    product = get_object_or_404(Product, id=pk) # Finction  (def) get_by_id_product()
    if product.user != request.user:     #  هاد الشخص من حقا يعدل  مثال الشخص مايصير يعدل على منتجات غيرو
        # HTTP_403_FORBIDDEN :  يعني مايصير تعديل عليها 
        return Response({"error":"Sorry You Can not Update this Product" },  status=status.HTTP_403_FORBIDDEN)   # request.user : الشخص يلي عامل ال تسجيل 
    
    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']

    product.save()
    serializer = ProdductSerializer(product , many=False)
    return Response({"product":serializer.data})
    
    

# Delete Product => IF Login 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])#  يلي ما عامل تسجيل مارح يطلع البيانات عنده
def delete_product(request , pk):
    product = get_object_or_404(Product, id=pk) # Finction  (def) get_by_id_product()
    if product.user != request.user:     #  هاد الشخص من حقا يعدل  مثال الشخص مايصير يعدل على منتجات غيرو
        # HTTP_403_FORBIDDEN :  يعني مايصير تعديل عليها 
        return Response({"error":"Sorry You Can not Update this Product" },  status=status.HTTP_403_FORBIDDEN)   # request.user : الشخص يلي عامل ال تسجيل 
    
    product.delete()
    return Response({"Delete Product":"Delete Action  Done ...!"} , status=status.HTTP_200_OK)
    
    




#  create review [rating]   التقيمم
@api_view(['POST'])
@permission_classes([IsAuthenticated])#  يلي ما عامل تسجيل مارح يطلع البيانات عنده
def create_review(request , pk):
    user  = request.user #  يلي انت تحددها ألها   token     تحيد انو مستخدم هوي  عن طريق ال 
    product = get_object_or_404(Product , id=pk)
    data = request.data
    review = product.reviews.filter(user=user)   # reviews  : product   من ال  related_name   هاد جاي من ال 
 
 
    if data['rating'] <= 0 or data['rating'] > 5:  # حتى  المستخدم مايحط اكثر من خمسة او افل من خصفر 
             return Response({"Error":"Please Select between 1 to 5 only "} , status=status.HTTP_400_BAD_REQUEST)
    
    elif  review.exists(): # اذا كان موجود اصلن 
        #   كمان  comment  ضيف عليها اوراسل ال
        new_review = {'rating':data['rating'] , 'comment': data['comment']}
        review.update(**new_review)  #  تحديث واضاغة على السابق 

        # aggregate: اجمغ كل التفيمات  وطال المعدل  
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']  #avg_ratings اعمل عليها تعديل على اساس المعدالة يلي هوي 
    #    بعنى اذا اجا شخص وحط تقيم واهد والشخص القاني حظ 2 ف هوي رح ياخد المهدالة ويضيغا على اسا المعادلة 
        product.save()
        return Response({"details":"Product review update"})  # اذا نجحت المعالية يثول صار في تحديث بي التقيم ~
    
    else:  # او اذا كان التقيم جديد 
        Review.objects.create(
            user=user,  # ناخود معلومات المستخدم
            product = product,
            rating = data['rating'],
            comment = data['comment']
        )
        
         # aggragte: اجمغ كل التفيمات  وطال المعدل  
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']  #avg_ratings اعمل عليها تعديل على اساس المعدالة يلي هوي 
    #    بعنى اذا اجا شخص وحط تقيم واهد والشخص القاني حظ 2 ف هوي رح ياخد المهدالة ويضيغا على اسا المعادلة 
        product.save()
        return Response({"details":"Product review update"})
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request , pk):
    user = request.user
    product  = get_object_or_404(Product , id=pk)
    reivew = product.reviews.filter(user=user)
    if reivew.exists():
        reivew.delete()
        rating  =  product.reviews.aggregate(avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None:  # اذا غير موجود 
            rating['avg_ratings'] = 0 
            product.ratings =  rating['avg_ratings']
            product.save()
            return Response({"details":"Product review Deleted"})
    else:
        return Response({"Error":"Review Not Found "} , status=status.HTTP_404_NOT_FOUND)
