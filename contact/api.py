from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import (
    Owner, Barber, Review, GalleryItem, Appointment, Message, Service, Category
)
from .serializers import (
    OwnerSerializer, BarberSerializer, ReviewSerializer, GalleryItemSerializer,
    AppointmentSerializer, MessageSerializer, ServiceSerializer, CategorySerializer
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .mypagination import MyPagination
from .myfilter import (
    OwnerFilter, BarberFilter, ReviewFilter, CategoryFilter,
    ServiceFilter, GalleryItemFilter, AppointmentFilter, MessageFilter
)
import hashlib
from django.http import Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string 


class ContactAPIView(APIView):
    def get(self, request):
        owner = Owner.objects.first()
        serializer = OwnerSerializer(owner)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModelListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = []

    def get_queryset(self):
        raise NotImplementedError("Subclasses must implement this method.")

class ModelCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

class ModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    

class BarberListAPIView(ModelListAPIView):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer
    filterset_fields = ['name', 'expertise', 'experience_years']
    search_fields = ['name', 'expertise', 'experience_years']
    filterset_class = BarberFilter
    
    def get_queryset(self):
        return self.queryset

class BarberCreateAPIView(ModelCreateAPIView):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer

class BarberRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer

class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['barber', 'customer_name', 'rating']
    search_fields = ['barber__name', 'customer_name', 'rating']
    filterset_class = ReviewFilter
    pagination_class = MyPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class GalleryItemListAPIView(generics.ListAPIView):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'category', 'service']
    search_fields = ['name', 'category__name', 'service__name']
    filterset_class = GalleryItemFilter
    pagination_class = MyPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

class GalleryItemCreateAPIView(generics.CreateAPIView):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    permission_classes = [IsAuthenticated]

class GalleryItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    permission_classes = [IsAuthenticated]

class AppointmentListAPIView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['barber', 'date', 'service_type']
    search_fields = ['barber__name', 'date', 'service_type__name']
    filterset_class = AppointmentFilter
    pagination_class = MyPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

class AppointmentCreateAPIView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        service_type_id = self.request.data.get('service_type')
        if service_type_id is None:
            return Response({"service_type": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            service_type = Service.objects.get(pk=service_type_id)
        except Service.DoesNotExist:
            return Response({"service_type": ["Invalid service type ID."]}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(service_type=service_type)

class AppointmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

class MessageListAPIView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'email', 'phone', 'message']
    search_fields = ['name', 'email', 'phone', 'message']
    filterset_class = MessageFilter
    pagination_class = MyPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

class MessageCreateAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

class MessageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'category__name', 'price']
    search_fields = ['name', 'category__name', 'price']
    filterset_class = ServiceFilter
    pagination_class = MyPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

class ServiceCreateAPIView(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

class ServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.prefetch_related('service_category').all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name','service_category__name']
    search_fields = ['name','service_category__name']   
    filterset_class = CategoryFilter
    pagination_class = MyPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class VisitorInfoAndHashMixin:
    def get_visitor_info_and_hash(self, request):
        visitor_info = request.META.get('REMOTE_ADDR', '') + request.META.get('HTTP_USER_AGENT', '')
        visitor_hash = hashlib.sha256(visitor_info.encode()).hexdigest()
        return visitor_info, visitor_hash


class VisitorAppointmentCreateAPIView(VisitorInfoAndHashMixin, CreateAPIView):
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        visitor_info, visitor_hash = self.get_visitor_info_and_hash(self.request)

        existing_appointment = Appointment.objects.filter(
            visitor_hash=visitor_hash,
            date=serializer.validated_data['date'],
            time=serializer.validated_data['time']
        ).first()

        if existing_appointment:
            return Response({'error': 'Sie haben bereits einen Termin für dieses Datum und diese Uhrzeit.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(visitor_hash=visitor_hash)


class VisitorReviewCreateAPIView(VisitorInfoAndHashMixin, CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        visitor_info, visitor_hash = self.get_visitor_info_and_hash(self.request)

        existing_review = Review.objects.filter(
            visitor_hash=visitor_hash,
            barber=serializer.validated_data['barber'],
            customer_name=serializer.validated_data['customer_name']
        ).first()

        if existing_review:
            return Response({'error': 'Sie haben bereits eine Bewertung für diesen Friseur mit dem gleichen Namen abgegeben.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(visitor_hash=visitor_hash)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        review_data = response.data
        # Render the new review HTML
        new_review_html = render_to_string('include/reviews.html', {'review': review_data})
        return Response({'html': new_review_html})


class VisitorAppointmentListAPIView(VisitorInfoAndHashMixin, ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        visitor_info, visitor_hash = self.get_visitor_info_and_hash(self.request)
        email = self.request.POST.get('email', '')

        if email:
            return Appointment.objects.filter(Q(email=email) | Q(visitor_hash=visitor_hash))
        else:
            return Appointment.objects.filter(visitor_hash=visitor_hash)


class VisitorReviewListAPIView(VisitorInfoAndHashMixin, ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        visitor_info, visitor_hash = self.get_visitor_info_and_hash(self.request)
        return Review.objects.filter(visitor_hash=visitor_hash)


class ManagementAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination

    def get_queryset(self):
        appointment_queryset = Appointment.objects.all()
        barber_queryset = Barber.objects.all()
        review_queryset = Review.objects.all()
        gallery_item_queryset = GalleryItem.objects.all()
        category_queryset = Category.objects.all()
        service_queryset = Service.objects.all()

        return {
            'appointment_list': appointment_queryset,
            'barber_list': barber_queryset,
            'review_list': review_queryset,
            'gallery_item_list': gallery_item_queryset,
            'category_list': category_queryset,
            'service_list': service_queryset,
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {
            'appointment_list': AppointmentSerializer(queryset['appointment_list'], many=True).data,
            'barber_list': BarberSerializer(queryset['barber_list'], many=True).data,
            'review_list': ReviewSerializer(queryset['review_list'], many=True).data,
            'gallery_item_list': GalleryItemSerializer(queryset['gallery_item_list'], many=True).data,
            'category_list': CategorySerializer(queryset['category_list'], many=True).data,
            'service_list': ServiceSerializer(queryset['service_list'], many=True).data,
        }
        return Response(data)