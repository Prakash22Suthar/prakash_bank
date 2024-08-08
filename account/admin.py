from django.contrib import admin

from .models import Account, Transaction
# Register your models here.


@admin.register(Account)
class Account(admin.ModelAdmin):
    list_display = ["account_number", "account_holder", "type", "initial_balance", "balance"]
    list_display_links = ["account_number"]



@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    list_display = ["t_account", "type", "amount", "location","created_at"]
    list_display_links = ["t_account"]