from users.models import User
from rest_framework import exceptions
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import get_hasher, check_password
from datetime import datetime, timedelta, timezone
from .models import AccountPassword

def _authenticate(email, password):
    user = User.objects.filter(email=email).last()
    print(":::::::::::authentication started:::::::::::::")

    if not user:
        raise exceptions.AuthenticationFailed({"email_error":"Please enter your registered email"})
    
    if user.is_blocked:
        raise exceptions.ValidationError("Your account is locked due to multiple failed login attempts. Please contact support.")

    authenticated = authenticate(**{get_user_model().USERNAME_FIELD: email, "password":password})

    if not authenticated:
        raise exceptions.AuthenticationFailed({"password_error":"incorrect Password","user_role":user.role})
        
    # if authenticated:
    #     account_password = AccountPassword.objects.filter(account_holder__email=email).last()
    #     password_set_days = (datetime.now(timezone.utc) - account_password.created_at).days() 
    #     if password_set_days < 1 :
    #         raise exceptions.ValidationError("password is old please change password")
        


def encode_password(password):
        hasher = get_hasher()
        encoded_password = hasher.encode(password, hasher.salt())
        return encoded_password