from users.models import User
from rest_framework import exceptions
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import get_hasher, check_password
from datetime import datetime, timedelta, timezone
import random
import string

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



def generate_password(min_length=6):
    if min_length < 6:
        raise ValueError("Minimum password length should be at least 6 characters.")

    # Required characters
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    special = random.choice(string.punctuation)
    digit = random.choice(string.digits)

    # Generate the rest of the password
    remaining_length = min_length - 4
    remaining_chars = random.choices(string.ascii_letters + string.digits + string.punctuation, k=remaining_length)

    # Combine all parts and shuffle the result
    password_list = list(uppercase + lowercase + special + digit + ''.join(remaining_chars))
    random.shuffle(password_list)

    # Return the password as a string
    return ''.join(password_list)