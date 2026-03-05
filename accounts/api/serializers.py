from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration via API"""

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        trim_whitespace=False,
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "first_name": {"trim_whitespace": True},
            "last_name": {"trim_whitespace": True},
        }

    def validate(self, attrs):
        """Validation with proper error messages"""
        username = attrs.get("username")
        email = attrs.get("email")
        password = attrs.get("password")
        password2 = attrs.get("password2")

        # Check password match first
        if password != password2:
            raise serializers.ValidationError(
                {"password2": "Password fields must match."}
            )

        # Check uniqueness
        errors = {}

        if User.objects.filter(username__iexact=username).exists():
            errors["username"] = "A user with this username already exists."

        if User.objects.filter(email__iexact=email).exists():
            errors["email"] = "A user with this email already exists."

        if errors:
            raise serializers.ValidationError(errors)

        attrs["email"] = email.lower()
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adds user profile data to JWT login response"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Minimal claims only - keep tokens small
        token["username"] = user.username
        token["email"] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for reading/updating user profile via API"""

    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("id", "date_joined", "last_login", "username")
        extra_kwargs = {
            "first_name": {"trim_whitespace": True},
            "last_name": {"trim_whitespace": True},
        }

    def get_full_name(self, obj):
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return obj.first_name or obj.last_name or ""

    def update(self, instance, validated_data):
        """Update with update_fields for efficiency"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if validated_data:
            instance.save(update_fields=validated_data.keys())

        return instance
