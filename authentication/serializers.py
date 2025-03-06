from rest_framework import serializers
from authentication.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("No user found with this email.")

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:8000/api/auth/reset-password/{uid}/{token}/"

        # Mock email backend (print instead of sending)
        print(f"Password reset link: {reset_link}")

        return data



class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "Invalid email or password"})

        if not user.check_password(password):
            raise serializers.ValidationError({"message": "Invalid email or password"})

        if not user.is_active:
            raise serializers.ValidationError({"message": "User account is not active"})

        attrs["username"] = user.username  # Required for TokenObtainPairSerializer
        return super().validate(attrs)