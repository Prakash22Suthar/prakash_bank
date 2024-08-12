from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, LoginTokenObtainSerializer, PasswordChangeSerializer
from .models import User
from base.pagination import CustomPagination
from base.permissions import UserCreatePermission
from base.throttles import CustomThrottleClass
# Create your views here.



class UserViewset(ModelViewSet):

    """User CURD With custom permission and jwt authentication"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, UserCreatePermission]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        actions = {
            # "create":UserSerializer,
            "change_password":PasswordChangeSerializer,
        }
        if self.action in actions:
            self.serializer_class = actions.get(self.action)
        return super().get_serializer_class()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == User.CUSTOMER:
            queryset = queryset.filter(id=self.request.user.id, is_deleted=False)
        if self.request.user.role == User.STAFF:
            queryset = queryset.filter(role=User.STAFF, is_deleted=False)
        return queryset
    
    @action(
     methods=["PUT"], 
     detail=True, 
     url_path="change-password", 
     url_name="change_password"
     )
    def change_password(self, request, pk):

        """ user password change with various validation"""

        user = User.objects.get(id=pk)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        insatance = serializer.save()
        user = UserSerializer(insatance)
        return Response(user.data, status=status.HTTP_200_OK)

class LoginTokenGenerateView(TokenObtainPairView):

    """ login and generate JWT token"""

    serializer_class = LoginTokenObtainSerializer
    # authentication_classes = [CustomAuthenticationBackend]
    # throttle_classes = [CustomThrottleClass]
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
    
