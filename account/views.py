import datetime
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from base.permissions import AccountCreatePermission

from .models import Account, Transaction
from users.models import User
from .serializers import AccountSerializer, AccountCreateSerializer, TransactionSerializer, TransactionCreateSerializer
# Create your views here.


class AccountViewset(ModelViewSet):

    """Account CURD With custom permission and jwt authentication"""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AccountCreatePermission]

    def get_serializer_class(self):
        actions = {
            "create":AccountCreateSerializer,
            "transaction_history":TransactionSerializer,
            # "update":AccountCreateUpdateSerializer,
        }
        if self.action in actions:
            self.serializer_class = actions.get(self.action)
        return super().get_serializer_class()


    def create(self, request, *args, **kwargs):
        account_holder = request.data.pop("account_holder")
        serializer = self.get_serializer(data=request.data, context={"account_holder":account_holder})   
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(AccountSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(
        methods=["GET"], 
        detail=False, 
        url_path="(?P<pk>[^/.]+)/transaction-history", 
        url_name="transaction_history", 
    )
    def transaction_history(self, request, pk:None):

        """action method to get transaction history of an individual account"""

        current_time = datetime.datetime.now().date()
        three_month_old_time = current_time - datetime.timedelta(days=90)
        start_date = request.query_params.get("start_date", three_month_old_time)
        end_date = request.query_params.get("end_date", current_time)

        filters = {
            "t_account__id":pk, 
            "is_deleted":False,
            "created_at__date__lte":end_date,
            "created_at__date__gte":start_date,
            }
        
        transactions = Transaction.objects.filter(**filters)
        
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    

class TransactionViewset(ModelViewSet):

    """Transaction CURD With custom permission and jwt authentication"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    # def get_queryset(self):
    #     queryest = super().get_queryset()
    #     if self.request.user and self.request.user.role == User.CUSTOMER :
    #         queryset = queryest.filter(t_account__account_holder__id=self.request.user.id)
    #     return queryest
    
    def get_serializer_class(self):
        actions = {
            "create":TransactionCreateSerializer,
        }
        if self.action in actions:
            self.serializer_class = actions.get(self.action)
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)