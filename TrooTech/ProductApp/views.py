import os

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category
from .serializers import ProductSerializers
from .tasks import sendMailTask

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def get_object(pk):
    try:
        return Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404


class ParticularProductReadView(APIView):
    def get(self, request, pk, format=None):
        productObj = get_object(pk)
        serializer = ProductSerializers(productObj)
        return Response(serializer.data)


def getAllProducts():
    snippets = Product.objects.all()
    serializer = ProductSerializers(snippets, many=True)
    return serializer


class ProductReadView(APIView):
    def get(self, request, format=None):
        if 'product' in cache:
            # get results from cache
            products = cache.get('product')
            print("got from cache")

            return Response(products, status=status.HTTP_201_CREATED)
        else:
            serializer = getAllProducts()
            print("Not from cache")
            cache.set('product', serializer.data, timeout=CACHE_TTL)

            return Response(serializer.data)


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    success_url = '/products'


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products')
    cache.clear()

    def delete(self, request, *args, **kwargs):
        cache.delete("product")
        cache.clear()
        return super().delete(request, *args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    success_url = "/products"


def getAndStoreExcelData():
    from django.core.management import call_command

    call_command('create_dummy_products')
    import pandas as pd
    fileName = 'ProductsSheet.csv'
    data = getAllProducts().data
    jsonData = JSONRenderer().render(data, renderer_context={'indent': 4}).decode()
    print(type(jsonData))
    with open('productsJson.txt', 'w') as file:
        file.write(jsonData)
        df = pd.read_json(r'productsJson.txt')
        df.to_csv(fileName, index=None)
    os.remove('productsJson.txt')
    return fileName


def sendEmailImmediate(request):
    fileName = getAndStoreExcelData()
    sendMailTask.delay(fileName)

    return HttpResponse("Mail sent Successfully!")


def sendEmailAsync(request):
    fileName = getAndStoreExcelData()
    sendMailTask.delay(fileName, 120)

    return HttpResponse("Mail will be sent after 2 minutes!")


