from rest_framework import serializers 
from .models import Product , Review


class ProdductSerializer(serializers.ModelSerializer):
    # method_name اخنار التابع يلي رح يجب كل التفيم تبع هاد المنتج 
    # read_only :  يعني عدم التلاعب بي هاد ال التابع 
    reviews = serializers.SerializerMethodField(method_name='get_reviews' , read_only=True) 
    class Meta:  # البينات الصوصفية 
        model  = Product
        fields = "__all__"
        # fields= ('name' , 'price' , 'brand')
        
    def get_reviews(self, obj):  #obj  يرحهعا م كائن التاريح والتفيم
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews , many=True)
        return serializer.data
        
         
    

# Rating Reviw  التقيم 
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:  # البينات الصوصفية 
        model  = Review
        fields = "__all__"

        
        
        
         
    