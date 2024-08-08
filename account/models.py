from typing import Iterable
from django.db import models

from base.models import BaseModel
from users.models import User
# Create your models here.


class Account(BaseModel):
    SAVING = "s"
    CURRENT = "c"
    ACCOUNT_TYPE = (
        (SAVING, "Saving"),
        (CURRENT, "Current")
    )
    account_number = models.PositiveIntegerField(unique=True)
    account_holder = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name="accounts")
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPE, default=SAVING)
    initial_balance = models.FloatField(null=True, blank=True)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.account_number)

class Transaction(BaseModel):
    CREDIT = "c"
    DEBIT = "d"
    TRANSACTION_TYPE = (
        (CREDIT, "Credit"),
        (DEBIT, "Debit"),
    )
    transaction_id = models.CharField(unique=True, max_length=200)
    t_account = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name="transactions")
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    amount = models.FloatField()
    location = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        print('➡ account/models.py:39 self:', self.__dict__)
        flag = kwargs.pop('account_open_flag', False)
        # import ipdb
        # ipdb.set_trace()
        if not flag:
            account : Account = self.t_account
            if self.type == "c":
                account.balance += self.amount if self.amount else 0.0
            elif self.type == "d":
                account.balance -= self.amount if self.amount else 0.0
            account.save()
        super(Transaction, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        account : Account = self.t_account
        if self.type == "c":
            account.balance += self.amount if self.amount else 0.0
        elif self.type == "d":
            account.balance -= self.amount if self.amount else 0.0
        account.save()