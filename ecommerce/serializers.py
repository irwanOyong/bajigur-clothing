from django.utils import timezone
from datetime import datetime
from rest_framework import serializers
from .models import (
    Category, Size, Color, Catalog, Profile, Wishlist, Cart, Order, OrderDetail
)

from os import path
import json

from django.db.models import Sum
from django.db.models.functions import Coalesce

class CategorySerializers(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['url','id','name']

class SizeSerializers(serializers.ModelSerializer):
  class Meta:
    model = Size
    fields = ['url','id','name']

class ColorSerializers(serializers.ModelSerializer):
  class Meta:
    model = Color
    fields = ['url','id','name']

class CatalogSerializers(serializers.ModelSerializer):
  in_stock = serializers.SerializerMethodField(method_name='check_in_stock')

  class Meta:
    model = Catalog
    depth = 1
    fields = ['url','id','sku','name','category','size','color','unit_price','stock','photo','in_stock']

  def check_in_stock(self, instance):
    in_stock = True
    if instance.stock == 0 : in_stock = False 
    return in_stock

class ProfileSerializers(serializers.ModelSerializer):
  class Meta:
    model = Profile
    depth = 1
    fields = ['url','id','user','phone_number','address','height','weight','bust','waist','hip','favourite_color']

class WishlistSerializers(serializers.ModelSerializer):
  class Meta:
    model = Wishlist
    depth = 1
    fields = ['url','id','user','catalog']

class CartSerializers(serializers.ModelSerializer):
  class Meta:
    model = Cart
    depth = 1
    fields = ['url','id','user','catalog','updated_timestamp','qty']

class OrderDetailSerializers(serializers.ModelSerializer):
  class Meta:
    model = OrderDetail
    depth = 1
    fields = ['url','id','order','catalog','unit_price','qty','sub_total']

class OrderSerializers(serializers.ModelSerializer):
  grand_total = serializers.SerializerMethodField(method_name='get_grand_total')
  orders = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='order-detail'
    )
  
  class Meta:
    model = Order
    depth = 1
    fields = ['url','id','user','order_timestamp','grand_total','is_paid','paid_timestamp','payment_method','payment_ref','orders']

  def get_grand_total(self, instance):
    grand_total = sum(OrderDetail.objects.filter(order=instance.id).aggregate(x=Coalesce(Sum('sub_total'),0)).values())
    return grand_total