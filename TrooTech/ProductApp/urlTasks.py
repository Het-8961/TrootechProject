from django.urls import path, re_path,include
from . import views

urlpatterns=[
    path('products/<int:pk>/', views.ParticularProductReadView.as_view()),
    path('products/', views.ProductReadView.as_view(), name='products'),
    path('create/', views.ProductCreateView.as_view()),
    path('update/<int:pk>/', views.ProductUpdateView.as_view()),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view()),
    path('send_email_immediate/', views.sendEmailImmediate),
    path('send_email_async/', views.sendEmailAsync),

]