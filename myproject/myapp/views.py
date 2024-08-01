from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta, datetime
from .models import Trader, Product, Service, Order, Appointment, Review, MilkDelivery, MonthlyBill, Notification, Payment, ServiceProvider, Booking, Availability, Location
from .serializers import UserSerializer, TraderSerializer, ProductSerializer, ServiceSerializer, OrderSerializer, AppointmentSerializer, ReviewSerializer, MilkDeliverySerializer, MonthlyBillSerializer, NotificationSerializer, PaymentSerializer, ServiceProviderSerializer, AvailabilitySerializer, BookingSerializer, LocationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .permissions import IsAdmin, IsCustomer, IsTrader


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role'],
            membership=data['membership'],
            location=data['location']
        )
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        data = request.data
        user = User.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role'],
            membership=data['membership'],
            location=data['location']
        )
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class TraderViewSet(viewsets.ModelViewSet):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer
    permission_classes = [IsAuthenticated,IsTrader]

    @action(detail=False, methods=['post'])
    def update_profile(self, request):
        user = request.user
        data = request.data
        trader = Trader.objects.get(user=user)
        trader.services = data['services']
        trader.rating = data['rating']
        trader.save()
        serializer = TraderSerializer(trader)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(store=self.request.user if self.request.user.role == 'store' else None, trader=self.request.user.trader if self.request.user.role == 'trader' else None)

class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def update_profile(self, request):
        user = request.user
        data = request.data
        provider = ServiceProvider.objects.get(user=user)
        provider.profession = data['profession']
        provider.rating = data['rating']
        provider.available_locations.set(data['available_locations'])
        provider.save()
        serializer = ServiceProviderSerializer(provider)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(trader=self.request.user.trader)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        total_price = product.price * quantity
        if product.stock < quantity:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
        product.stock -= quantity
        product.save()
        serializer.save(user=self.request.user, total_price=total_price)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    @csrf_exempt
    @api_view(['POST'])
    def make_payment(request):
        # Placeholder for payment logic
        # Integrate with actual payment gateway API
        data = request.data
        order_id = data.get('order_id')
        amount = data.get('amount')
        payment_method = data.get('payment_method')
        # Assume payment is successful
        return Response({'status': 'Payment Successful'}, status=status.HTTP_200_OK)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def initiate_payment(self, request):
        data = request.data
        user = request.user
        order = Order.objects.get(id=data['order_id'])
        amount = order.total_price
        payment = Payment.objects.create(user=user, order=order, amount=amount, status='pending')
        # Integrate with actual payment gateway here
        payment.status = 'completed'  # Example status after payment success
        payment.save()
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def my_payments(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        service = serializer.validated_data['service']
        num_persons = serializer.validated_data['num_persons']
        total_price = service.price_per_person * num_persons
        if service.max_capacity < num_persons:
            return Response({'error': 'Service capacity exceeded'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user, total_price=total_price)

    @action(detail=False, methods=['get'])
    def my_appointments(self, request):
        appointments = Appointment.objects.filter(user=request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def submit_review(self, request):
        data = request.data
        review = Review.objects.create(
            user=request.user,
            trader_id=data['trader_id'],
            rating=data['rating'],
            comment=data['comment']
        )
        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MilkDeliveryViewSet(viewsets.ModelViewSet):
    queryset = MilkDelivery.objects.all()
    serializer_class = MilkDeliverySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def record_delivery(self, request):
        user = request.user
        data = request.data
        delivery = MilkDelivery.objects.create(
            user_id=data['user_id'],
            trader=user.trader,
            date=data['date'],
            litres_delivered=data['litres_delivered']
        )
        delivery.save()
        serializer = MilkDeliverySerializer(delivery)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def view_deliveries(self, request):
        user = request.user
        deliveries = MilkDelivery.objects.filter(user=user)
        serializer = MilkDeliverySerializer(deliveries, many=True)
        return Response(serializer.data)

class MonthlyBillViewSet(viewsets.ModelViewSet):
    queryset = MonthlyBill.objects.all()
    serializer_class = MonthlyBillSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def calculate_monthly_bill(self, request):
        user = request.user
        data = request.data
        month = data['month']
        start_date = month + "-01"
        end_date = (now().replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        deliveries = MilkDelivery.objects.filter(user=user, date__range=[start_date, end_date])
        total_litres = sum(d.litres_delivered for d in deliveries)
        price_per_litre = 50  # Example price per litre
        total_price = total_litres * price_per_litre
        bill = MonthlyBill.objects.create(
            user=user,
            trader=user.trader,
            month=start_date,
            total_litres=total_litres,
            total_price=total_price,
            confirmed_by_customer=False,
            confirmed_by_trader=False
        )
        bill.save()
        serializer = MonthlyBillSerializer(bill)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def view_monthly_bills(self, request):
        user = request.user
        bills = MonthlyBill.objects.filter(user=user)
        serializer = MonthlyBillSerializer(bills, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm_bill(self, request, pk=None):
        bill = self.get_object()
        if request.user.role == 'customer':
            bill.confirmed_by_customer = True
        elif request.user.role == 'trader':
            bill.confirmed_by_trader = True
        bill.save()
        serializer = MonthlyBillSerializer(bill)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_notifications(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        notification.save()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]

    @action(detail=False, methods=['get'])
    def user_activity(self, request):
        user_count = User.objects.count()
        trader_count = Trader.objects.count()
        order_count = Order.objects.count()
        appointment_count = Appointment.objects.count()
        data = {
            'user_count': user_count,
            'trader_count': trader_count,
            'order_count': order_count,
            'appointment_count': appointment_count
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def financial_report(self, request):
        total_revenue = Payment.objects.filter(status='completed').aggregate(sum('amount'))['amount__sum']
        data = {
            'total_revenue': total_revenue
        }
        return Response(data, status=status.HTTP_200_OK)

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def set_availability(self, request):
        user = request.user
        data = request.data
        availability = Availability.objects.create(
            provider=user.serviceprovider,
            date=data['date'],
            start_time=data['start_time'],
            end_time=data['end_time']
        )
        availability.save()
        serializer = AvailabilitySerializer(availability)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        service = serializer.validated_data['service']
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']
        total_hours = (datetime.combine(datetime.min, end_time) - datetime.combine(datetime.min, start_time)).seconds / 3600
        total_price = service.price_per_hour * total_hours

        availability = Availability.objects.filter(
            provider=service.provider,
            date=serializer.validated_data['date'],
            start_time__lte=start_time,
            end_time__gte=end_time
        ).exists()

        if not availability:
            return Response({'error': 'Service provider is not available at this time'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(customer=self.request.user, total_price=total_price)

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        bookings = Booking.objects.filter(customer=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available_services(self, request):
        user_location = request.user.location
        providers = ServiceProvider.objects.filter(
            available_locations__name=user_location
        ).order_by('-rating')
        services = Service.objects.filter(provider__in=providers)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]