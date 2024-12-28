from rest_framework import serializers
from .models import Account

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'phone', 'password')
    
    def validate_phone(self, value):
        """
        validate duplicate phone number
        """
        if Account.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def validate(self, data):
        """
        validate required fields
        """
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'password']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} is required")
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Account(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True) 