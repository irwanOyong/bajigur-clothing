from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics, viewsets, pagination, status
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters import rest_framework as filters
from django_filters import DateRangeFilter, DateFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import Filter
from django_filters.fields import Lookup

from .serializers import (
    CategorySerializers, SizeSerializers, ColorSerializers, CatalogSerializers, ProfileSerializers, WishlistSerializers, CartSerializers, OrderSerializers, OrderDetailSerializers
)

from .models import (
    Category, Size, Color, Catalog, Profile, Wishlist, Cart, Order, OrderDetail
)

class SmallResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'limit'

class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    filter_backends =(filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    filter_class=CategoryFilter

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializers

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializers

class CatalogFilter(filters.FilterSet):
    stock = filters.RangeFilter(field_name='stock')
    unit_price = filters.RangeFilter(field_name='unit_price')

    class Meta:
        model = Catalog
        fields = ['id', 'sku', 'name', 'category', 'size', 'color', 'unit_price', 'stock']

class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializers
    filter_backends =(filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('sku', 'name', 'category', 'size', 'color', 'unit_price', 'stock')
    search_fields = ('sku', 'name', 'category', 'size', 'color', 'unit_price', 'stock')
    filter_class=CatalogFilter

class ProfileFilter(filters.FilterSet):
    height = filters.RangeFilter(field_name='weight')
    weight = filters.RangeFilter(field_name='height')

    class Meta:
        model = Profile
        fields = ['id', 'address', 'height', 'weight', 'favourite_color']

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers
    filter_backends =(filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('address', 'height', 'weight', 'favourite_color')
    search_fields = ('address', 'height', 'weight', 'favourite_color')
    filter_class=ProfileFilter

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializers
    filter_backends =(filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('user', 'catalog')
    search_fields = ('user', 'catalog')

class CartFilter(filters.FilterSet):
    start_date = DateFilter(field_name='updated_timestamp',lookup_expr=('gt'),)
    end_date = DateFilter(field_name='updated_timestamp',lookup_expr=('lt'))
    date_range = DateRangeFilter(field_name='updated_timestamp')
    qty = filters.RangeFilter(field_name='qty')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'catalog', 'updated_timestamp', 'qty']

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers
    filter_backends =(filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('user', 'catalog', 'updated_timestamp', 'qty')
    search_fields = ('user', 'catalog', 'updated_timestamp', 'qty')
    filter_class=CartFilter

class OrderFilter(filters.FilterSet):
    order_start_date = DateFilter(field_name='order_timestamp',lookup_expr=('gt'),)
    order_end_date = DateFilter(field_name='order_timestamp',lookup_expr=('lt'))
    order_date_range = DateRangeFilter(field_name='order_timestamp')
    grand_total = filters.RangeFilter(field_name='grand_total')
    paid_start_date = DateFilter(field_name='paid_timestamp',lookup_expr=('gt'),)
    paid_end_date = DateFilter(field_name='paid_timestamp',lookup_expr=('lt'))
    paid_date_range = DateRangeFilter(field_name='paid_timestamp')

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_timestamp', 'grand_total', 'is_paid', 'paid_timestamp', 'payment_method', 'payment_ref']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    filter_backends =(filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('user', 'order_timestamp', 'grand_total', 'is_paid', 'paid_timestamp', 'payment_method', 'payment_ref')
    search_fields = ('user', 'order_timestamp', 'grand_total', 'is_paid', 'paid_timestamp', 'payment_method', 'payment_ref')
    filter_class=OrderFilter

class OrderDetailFilter(filters.FilterSet):
    unit_price = filters.RangeFilter(field_name='unit_price')
    qty = filters.RangeFilter(field_name='qty')
    sub_total = filters.RangeFilter(field_name='sub_total')
    
    class Meta:
        model = OrderDetail
        fields = ['id', 'order', 'catalog', 'unit_price', 'qty', 'sub_total']

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializers
    filter_backends =(filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('order', 'catalog', 'unit_price', 'qty', 'sub_total')
    search_fields = ('order', 'catalog', 'unit_price', 'qty', 'sub_total')
    filter_class=OrderDetailFilter

