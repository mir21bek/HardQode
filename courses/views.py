from django.db.models import Count, ExpressionWrapper, F, FloatField
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import (
    ProductListSerializer,
    ProductCreateSerializer,
    ListGroupSerializer,
    GroupCreateSerializer,
    GroupAddSerializer,
)
from .models import Product, Group, GroupMembership
from rest_framework import permissions
from rest_framework.views import APIView
from services.utils.add_user_group import distribute_users_to_group


class ProductListAPIView(generics.ListAPIView):
    queryset = (
        Product.objects.annotate(
            sum_students=Count("group_product__group__user", distinct=True),
            total_users=Count("author", distinct=True),
            percentage=ExpressionWrapper(
                100.0 * F("sum_students") / F("total_users"), output_field=FloatField()
            ),
        )
    ).filter(available=True)
    serializer_class = ProductListSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ListGroupAPIView(generics.ListAPIView):
    queryset = Group.objects.annotate(
        fill_percentage=ExpressionWrapper(
            100.0 * Count("group") / F("max_users"), output_field=FloatField()
        )
    )
    serializer_class = ListGroupSerializer


class CreateGroupAPIView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupAddAPIView(generics.CreateAPIView):
    queryset = GroupMembership.objects.all()
    serializer_class = GroupAddSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
