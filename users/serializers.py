from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

from prakash_bank.twilio_service import MessageServices
from .models import User, AccountPassword
from .utils import _authenticate, encode_password, check_password, generate_password

class LoginTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        attrs["email"] = attrs.get("email").lower()
        # _authenticate(attrs.get("email"), attrs.get("password"))
        email = attrs.get("email")
        password=attrs.get("password")
        request = self.context.get("request")
        authenticate(request, email=email, password=password)


        data = super().validate(attrs)
        data["id"] = self.user.id
        data["full_name"] = self.user.full_name
        data["email"] = self.user.email
        return data
    
class PasswordChangeSerializer(serializers.Serializer):

    """ serializer to validate and update password"""

    current_password = serializers.CharField(max_length=255)
    new_password1 = serializers.CharField(max_length=255)
    new_password2 = serializers.CharField(max_length=255)

    def update(self, user: User, validated_data):
        current_password = validated_data.get("current_password")
        encoded_new_password = encode_password(validated_data.get("new_password2"))
        password_check = check_password(current_password, user.password)
        if not password_check:
            raise serializers.ValidationError({"Password_error": "Current Password is Wrong"})
        
        if validated_data.get("new_password1") != validated_data.get("new_password2"):
            raise serializers.ValidationError({"Password_error":"password and confirm password is not same"})

        if validated_data.get("current_password") == validated_data.get("new_password2"):
            raise serializers.ValidationError({"Password_error": "Current Password and New Password Should not be same"})
        

        previous_passwords = AccountPassword.objects.filter(account_holder=user).values_list("password", flat=True)
        for old_password in previous_passwords:
            if check_password(validated_data.get("new_password2"), old_password):
                raise serializers.ValidationError({"password_error": "This password has been used before. Please choose a different password."})

        user.set_password(validated_data.get("new_password2"))
        user.save()

        AccountPassword.objects.create(account_holder=user, password= encoded_new_password)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                "id",
                "first_name",
                "last_name",
                "username",
                "email",
                # "password",
                "dob",
                "role",
                "address",
                "is_kyc",
                "created_at",
                "updated_at",
                "is_deleted"
            ]

        # extra_kwargs = {
        #     "email": {"read_only":True},
        # }

    def create(self, validated_data):
        # password = validated_data.pop("password")
        user = User(**validated_data)
        password = generate_password(6) # parameter passed for length of password
        print('➡ System Generated password::::::::::::', password)
        user.set_password(password)
        user.save()

        # # send welcome message with password
        # account_holder_number = user.mobile_number
        # message = f"Hi {user.full_name}, Welcome to be an customer of Prakash_Bank, \n this is your login password {password}"
        # service = MessageServices()
        # service.send_sms(account_holder_number, message)

        # save encoded password to account password table
        AccountPassword.objects.create(
            account_holder = user,
            password = encode_password(password)
        )
        return user
    
    def update(self, instance, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        instance = super().update(instance, validated_data)
        instance.set_password(password)
        instance.save()
        return instance