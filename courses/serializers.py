from rest_framework import serializers
from .models import Product, Group, GroupMembership


class ProductListSerializer(serializers.ModelSerializer):
    sum_students = serializers.IntegerField()
    percentage = serializers.FloatField()

    class Meta:
        model = Product
        fields = (
            "product_name",
            "start_time",
            "price",
            "lesson_count",
            "author",
            "sum_students",
            "percentage",
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "product_name",
            "description",
            "start_time",
            "price",
            "lesson_count",
            "author",
            "available",
        )


class ListGroupSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source="product.product_name")
    fill_percentage = serializers.FloatField()

    class Meta:
        model = Group
        fields = ("group_name", "product", "fill_percentage")


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("group_name", "product", "min_users", "max_users")


class GroupAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMembership
        fields = ("group",)
