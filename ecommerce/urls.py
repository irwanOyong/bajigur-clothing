from django.urls import include, path, re_path
from rest_framework import routers

from . import views, api_views

router = routers.DefaultRouter()

router.register(r'category', views.CategoryViewSet)
router.register(r'color', views.ColorViewSet)
router.register(r'size', views.SizeViewSet)
router.register(r'catalog', views.CatalogViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'wishlist', views.WishlistViewSet)
router.register(r'cart', views.CartViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'order-detail', views.OrderDetailViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/member-statistics/', api_views.MemberStatistics.as_view()),
    path('api/catalog-statistics/', api_views.CatalogStatistics.as_view()),
    path('api/wishlist-statistics/', api_views.WishlistStatistics.as_view()),
    path('api/cart-statistics/', api_views.CartStatistics.as_view()),
    path('api/order-statistics/', api_views.OrderStatistics.as_view()),
]