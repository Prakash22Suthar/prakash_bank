from rest_framework import serializers

from .models import Account, Transaction
from users.models import User
from users.serializers import UserSerializer
import random


class AccountSerializer(serializers.ModelSerializer):
    account_holder = serializers.SerializerMethodField()
    class Meta:
        model = Account
        fields = ["id","account_number","account_holder","type","initial_balance","balance"]
        extra_kwargs = {
            "account_number":{"read_only":True}
        }
    
    def get_account_holder(self, obj:Account):
        user : User = obj.account_holder
        return UserSerializer(user).data


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["type","initial_balance"]
    
    def create(self, validated_data):
        account_holder_data = self.context.get("account_holder") 
        account_holder = self.get_user(account_holder_data)
        account_obj : Account = Account(**validated_data)
        account = Account.objects.order_by("-id")
        # import ipdb
        # ipdb.set_trace()
        if account.exists():
            new_account_number = account[0].account_number + 1
        else:
            new_account_number = 4474001500000001
        account_obj.account_number = new_account_number
        account_obj.account_holder = account_holder
        account_obj.balance = validated_data["initial_balance"]
        account_obj.save()
        # make a transection entry
        transaction_data = {
            "transaction_id": random.randint(11111111,99999999),
            "t_account":account_obj,
            "type":"c",
            "amount": validated_data["initial_balance"],
            "location": "Home Branch",
        }
        transaction=Transaction(**transaction_data)
        transaction.save(account_open_flag=True)
        return account_obj

    def get_user(self,account_holder_data):
        email = account_holder_data.get("email",None)
        username = account_holder_data.get("username",None)
        try:
            user = User.objects.filter(email=email, username=username).last()
            if user and user.is_deleted:
                raise serializers.ValidationError("User exists and status is deleted")
            elif not user:
                user = User.objects.create(**account_holder_data)
        except Exception as e:
            print(":::::::::::excepiton caught::::::::::", e)
        return user



class TransactionSerializer(serializers.ModelSerializer):
    t_account = serializers.StringRelatedField()
    class Meta:
        model = Transaction
        fields = "__all__"
         
class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["t_account","type","amount","location"]

    def create(self, validated_data):
        transaction_id = random.randint(1111111111111111111111,9999999999999999999999)
        all_t_ids = list(Transaction.objects.values_list("transaction_id", flat=True))
        while transaction_id in all_t_ids:
            transaction_id = random.randint(1111111111111111111111,9999999999999999999999)
        transection = Transaction(**validated_data)
        transection.transaction_id = transaction_id
        transection.save()

        # add functionality send email/sms to account holder

        return transection
    