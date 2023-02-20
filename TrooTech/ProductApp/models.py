from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    ancestor = models.ForeignKey('self',models.SET_NULL,blank=True,null=True,)
    def __str__(self):
        return str(self.ancestor)  + '->' + self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    categoryMany = models.ManyToManyField(Category, blank=True, null=True)
