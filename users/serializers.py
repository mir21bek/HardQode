from rest_framework import serializers

from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, help_text="Введите адрес эл. почты")

    class Meta:
        model = CustomUser
        fields = (
            "user_name",
            "email",
        )

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data["email"],
            user_name=validated_data["user_name"]
        )
        return user


class CheckOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("otp",)
