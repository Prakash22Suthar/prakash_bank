from rest_framework.permissions import BasePermission
from users.models import User

class AccountCreatePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.role in [User.STAFF, User.BRANCH_MANAGER, User.ADMIN]:
            return True
        return False


class UserCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            authenticate_user : User = request.user
            new_user_role = request.data.get("role", "c")
            if new_user_role =="c" and authenticate_user.role in [User.STAFF, User.BRANCH_MANAGER, User.ADMIN]:
                return True
            if new_user_role == "s" and authenticate_user.role in [User.BRANCH_MANAGER, User.ADMIN]:
                return True
            if new_user_role == "bm" and authenticate_user.role == User.ADMIN:
                return True
            return False
        return True


# class TransactionPermission(BaseException):
#     def has_permission(self, request, view):
