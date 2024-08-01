from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Trader, Product, Service, Order, Appointment, Review, MilkDelivery, MonthlyBill, Notification, Payment, Location, Booking, Availability, ServiceProvider

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

class TraderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trader
        fields = ('user', 'services', 'rating')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class MilkDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkDelivery
        fields = '__all__'

class MonthlyBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBill
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ServiceProviderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    available_locations = serializers.PrimaryKeyRelatedField(many=True, queryset=Location.objects.all())

    class Meta:
        model = ServiceProvider
        fields = ('user', 'profession', 'rating', 'available_locations')

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'