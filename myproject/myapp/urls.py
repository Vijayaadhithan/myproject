from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from .views import UserViewSet, TraderViewSet, ProductViewSet, ServiceViewSet, OrderViewSet, AppointmentViewSet, ReviewViewSet, MilkDeliveryViewSet, MonthlyBillViewSet, NotificationViewSet, PaymentViewSet, ReportViewSet, ServiceProviderViewSet, LocationViewSet, BookingViewSet, AvailabilityViewSet 
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'traders', TraderViewSet)
router.register(r'products', ProductViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'milk_deliveries', MilkDeliveryViewSet)
router.register(r'monthly_bills', MonthlyBillViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'service_providers', ServiceProviderViewSet)
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'locations', LocationViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
