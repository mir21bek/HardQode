from django.db.models import Count, ExpressionWrapper, F, FloatField
from django.utils import timezone
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
from users.models import CustomUser
from rest_framework import permissions
from rest_framework.views import APIView
from services.utils.add_user_group import distribute_users_to_group, choose_group_for_user


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


class GroupAddAPIView(APIView):
    @swagger_auto_schema(
        request_body=GroupAddSerializer,
        responses={201: "User added to group", 404: "No available groups",
                   200: "message Groups rebuilt"},
    )
    def post(self, request, product_id, user_id):
        product = Product.objects.get(pk=product_id)
        user = CustomUser.objects.get(id=user_id)
        if product.start_time <= timezone.now():
            group = choose_group_for_user(product)
            if group:
                GroupMembership.objects.create(group=group, user=user)
                return Response({"message": "User added to group."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No available groups."}, status=status.HTTP_404_NOT_FOUND)
        else:
            distribute_users_to_group(product.id, user)
            return Response({"message": "Groups rebuilt."}, status=status.HTTP_200_OK)
