from datetime import datetime
from django.utils import timezone
from decimal import Decimal
from django.db import models
import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'category'

    def __str__(self):
        return str(self.name)

class Size(models.Model):
    name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = True
        db_table = 'size'

    def __str__(self):
        return str(self.name)

class Color(models.Model):
    name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = True
        db_table = 'color'

    def __str__(self):
        return str(self.name)

def get_catalog_path(instance, filename):
    return os.path.join('catalogs', str(instance.sku), filename)

class Catalog(models.Model):
    sku = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category')
    size = models.ForeignKey(Size, models.DO_NOTHING, db_column='size')
    color = models.ForeignKey(Color, models.DO_NOTHING, db_column='color')
    unit_price = models.DecimalField(max_digits=11, decimal_places=2)
    stock = models.IntegerField(default=0)
    photo = models.ImageField(upload_to=get_catalog_path)

    class Meta:
        managed = True
        db_table = 'catalog'
        unique_together = (('sku', 'size', 'color'),)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=30, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bust = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hip = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    favourite_color = models.ManyToManyField(Color)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Wishlist(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')
    catalog = models.ForeignKey(Catalog, models.DO_NOTHING, db_column='catalog')
    wishlist_timestamp = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        managed = True
        db_table = 'wishlist'
        unique_together = (('user', 'catalog'),)

class Cart(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')
    catalog = models.ForeignKey(Catalog, models.DO_NOTHING, db_column='catalog')
    updated_timestamp = models.DateTimeField(default=timezone.now, blank=True)
    qty = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'cart'
        unique_together = (('user', 'catalog'),)

class Order(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')
    order_timestamp = models.DateTimeField(default=timezone.now, blank=True)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    is_paid = models.SmallIntegerField(default=0)
    paid_timestamp = models.DateTimeField(default=timezone.now, blank=True)
    payment_method = models.CharField(max_length=30, blank=True)
    payment_ref = models.CharField(max_length=30, blank=True)

    class Meta:
        managed = True
        db_table = 'order'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, models.DO_NOTHING, db_column='order', related_name='orders')
    catalog = models.ForeignKey(Catalog, models.DO_NOTHING, db_column='catalog')
    unit_price = models.DecimalField(max_digits=11, decimal_places=2)
    qty = models.IntegerField()
    sub_total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'order_detail'