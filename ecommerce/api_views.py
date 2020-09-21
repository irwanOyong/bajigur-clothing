from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q, Avg, Sum, Max, Min
from django.db import connection
from django.db.models.functions import Coalesce

from .models import Category, Size, Color, Catalog, Profile, Wishlist, Cart, Order, OrderDetail
from django.db.models import Count

class MemberStatistics(APIView):
    def get(self, request, format = None):
        average_weight = sum(Profile.objects.all().aggregate(x=Coalesce(Avg('weight'),0)).values())
        average_height = sum(Profile.objects.all().aggregate(x=Coalesce(Avg('height'),0)).values())
        address_counts = Profile.objects.values('address').annotate(count=Count('address')).order_by('-count')
        favourite_color_counts = Profile.objects.values('favourite_color__name').annotate(count=Count('favourite_color')).order_by('-count')
        
        full_data = {
                    "average_weight":average_weight,
                    "average_height":average_height,
                    "address_counts":address_counts,
                    "favourite_color_counts":favourite_color_counts,
                    }

        response = {**full_data}
        
        return Response(response)

class CatalogStatistics(APIView):
    def get(self, request, format = None):
        category_counts = Catalog.objects.values('category__name').annotate(count=Count('category')).order_by('-count')
        size_counts = Catalog.objects.values('size__name').annotate(count=Count('size')).order_by('-count')
        color_counts = Catalog.objects.values('color__name').annotate(count=Count('color')).order_by('-count')
        max_price = sum(Catalog.objects.all().aggregate(x=Coalesce(Max('unit_price'),0)).values())
        average_price = sum(Catalog.objects.all().aggregate(x=Coalesce(Avg('unit_price'),0)).values())
        min_price = sum(Catalog.objects.all().aggregate(x=Coalesce(Min('unit_price'),0)).values())
        
        full_data = {
                    "category_counts":category_counts,
                    "size_counts":size_counts,
                    "color_counts":color_counts,
                    "max_price":max_price,
                    "average_price":average_price,
                    "min_price":min_price,
                    }

        response = {**full_data}
        
        return Response(response)

class WishlistStatistics(APIView):
    def get(self, request, format = None):
        user_counts = Wishlist.objects.values('user__username').annotate(count=Count('user')).order_by('-count')
        category_counts = Wishlist.objects.values('catalog__category__name').annotate(count=Count('catalog__category')).order_by('-count')
        size_counts = Wishlist.objects.values('catalog__size__name').annotate(count=Count('catalog__size')).order_by('-count')
        color_counts = Wishlist.objects.values('catalog__color__name').annotate(count=Count('catalog__color')).order_by('-count')
        
        full_data = {
                    "user_counts":user_counts,
                    "category_counts":category_counts,
                    "size_counts":size_counts,
                    "color_counts":color_counts,
                    }

        response = {**full_data}
        
        return Response(response)

class CartStatistics(APIView):
    def get(self, request, format = None):
        user_counts = Cart.objects.values('user__username').annotate(count=Count('user')).order_by('-count')
        category_counts = Cart.objects.values('catalog__category__name').annotate(count=Count('catalog__category')).order_by('-count')
        size_counts = Cart.objects.values('catalog__size__name').annotate(count=Count('catalog__size')).order_by('-count')
        color_counts = Cart.objects.values('catalog__color__name').annotate(count=Count('catalog__color')).order_by('-count')
        
        full_data = {
                    "user_counts":user_counts,
                    "category_counts":category_counts,
                    "size_counts":size_counts,
                    "color_counts":color_counts,
                    }

        response = {**full_data}
        
        return Response(response)

class OrderStatistics(APIView):
    def get(self, request, format = None):
        user_counts = Order.objects.values('user__username').annotate(count=Count('user')).order_by('-count')
        is_paid_counts = Order.objects.values('is_paid').annotate(count=Count('is_paid')).order_by('-count')
        payment_method_counts = Order.objects.values('payment_method').annotate(count=Count('payment_method')).order_by('-count')
        category_counts = OrderDetail.objects.values('catalog__category__name').annotate(count=Count('catalog__category')).order_by('-count')
        size_counts = OrderDetail.objects.values('catalog__size__name').annotate(count=Count('catalog__size')).order_by('-count')
        color_counts = OrderDetail.objects.values('catalog__color__name').annotate(count=Count('catalog__color')).order_by('-count')
        
        full_data = {
                    "user_counts":user_counts,
                    "is_paid_counts":is_paid_counts,
                    "payment_method_counts":payment_method_counts,
                    "category_counts":category_counts,
                    "size_counts":size_counts,
                    "color_counts":color_counts,
                    }

        response = {**full_data}
        
        return Response(response)