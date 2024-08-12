from rest_framework.throttling import ScopedRateThrottle
from users.models import User

class CustomThrottleClass(ScopedRateThrottle):
    
    """ Define throttle according to user role throttle_scope defines """

    def allow_request(self, request, view):
        email = request.data.get("email")
        password = request.data.get("password")
        user = User.objects.get(email=email)
        print(":::::::::::::throttle check started::::::::::::::")
        if user.role == "c":
            throttle_scope = "login_customer"
        elif user.role == "s":
            throttle_scope = "login_staff"
        elif user.role == "bm":
            throttle_scope = "login_branch_manager"
        return super().allow_request(request, view)