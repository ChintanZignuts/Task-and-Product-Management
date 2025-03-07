from rest_framework import serializers
from authentication.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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

        email_html_content = render_to_string("emails/password_reset_email.html", {"reset_link": reset_link})
        email_text_content = strip_tags(email_html_content)  

        email_message = EmailMultiAlternatives(
            subject="Password Reset Request",
            body=email_text_content,
            from_email="noreply@example.com",
            to=[email]
        )
        email_message.attach_alternative(email_html_content, "text/html")
        email_message.send()
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