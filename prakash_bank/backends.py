from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from base import constants

User = get_user_model()

class CustomAuthenticationBackend(ModelBackend):

    """ To Count Failed Login Attemps and if limit exided account will be locked for 
    user role [User.CUSTOMER, User.STAFF]"""

    def authenticate(self, request, email=None, password=None, **kwargs):

        """ override the django authenticate method to achieve account lock functionality"""

        if email is None:
            email = request.POST.get("username")
            password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:  # Corrected case
            raise AuthenticationFailed(_('Invalid email or password.'))

        # Determine maximum allowed login attempts based on user role
        max_limit = {
            "c": constants.CUSTOMER_LOGIN_LIMIT,
            "s": constants.STAFF_LOGIN_LIMIT
        }.get(user.role, None)

        # Check if the account is locked 
        if  user.is_locked:
            raise AuthenticationFailed(_('Your account has been locked due to too many failed login attempts.'))

        # If password is incorrect
        if not user.check_password(password):
            # Special handling for roles 'a' and 'bm'
            if user.role in [User.ADMIN, User.BRANCH_MANAGER]:
                raise AuthenticationFailed("Wrong password. Please try again")
            if user.role in [User.CUSTOMER, User.STAFF]:
                # Increment failed attempts
                user.failed_attempts += 1
                user.save()

                # Lock the account if max limit is reached
                if max_limit is not None and user.failed_attempts >= max_limit:
                    user.is_locked = True
                    user.save()
                    raise AuthenticationFailed(_('Your account has been locked due to too many failed login attempts.'))
                else:
                    remaining_attempts = max_limit - user.failed_attempts
                    raise AuthenticationFailed(_(f'Wrong password. You have {remaining_attempts} attempt(s) left.'))

        # Reset failed attempts on successful login
        user.failed_attempts = 0
        user.save()
        return user