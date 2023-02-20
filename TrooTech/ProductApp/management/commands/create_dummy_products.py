from django.core.exceptions import FieldDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from ... import models


class Command(BaseCommand):
    help = 'Create 100 products'

    def handle(self,*args, **options):
        try:
            productList=[]
            totNum=0
            try:
                id=models.Product.objects.latest('id').id
                totNum=id
            except:
                pass
            for i in range(100):
                productObj =models.Product(name='TestName-'+str(totNum),price=-999)
                productList.append(productObj)
                totNum+=1
            models.Product.objects.bulk_create(productList)
            self.stdout.write("100 Products are added")

        except FieldDoesNotExist:
            self.stdout.write(self.style.ERROR('Error got!'))

