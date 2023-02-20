from rest_framework import serializers

from .models import Product, Category


class CategorySerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)
    class Meta:
        model = Category
        fields = ('id','name','ancestor')


class ProductSerializers(serializers.ModelSerializer):
    categories = CategorySerializers(source=str('categoryMany'), many=True)
    class Meta:
        model = Product
        fields = ('id','name','price','categories')

    def create(self, validated_data):
        productObj=Product(name=validated_data['name'], price = validated_data['price'])
        productObj.save()

        for i in validated_data['categoryMany']:
            categoryObj = Category.objects.get(id=i['id'])
            productObj.categoryMany.add(categoryObj)
        productObj.save()

        return productObj
