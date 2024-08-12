from typing import Any, Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser

from base.models import BaseModel
# Create your models here.

class User(AbstractUser, BaseModel):
    CUSTOMER = 'c'
    STAFF = 's'
    BRANCH_MANAGER = 'bm'
    ADMIN = "a"
    # AREA_MANAGER = 'am'

    ROLE = (
        (CUSTOMER, "Customer"),
        (STAFF, "Staff"),
        (BRANCH_MANAGER, "Branch Manager"),
        (ADMIN, "Admin"),
        # (AREA_MANAGER, "Area Manager"),
    )
    
    ADHAR_CARD_ID = 'aci'
    PAN_CARD_ID = 'pci'
    PASPORT_ID = 'pd'

    KYC_TYPE = (
        (ADHAR_CARD_ID, "Adhar Card"),
        (PAN_CARD_ID, "Pan Card"),
        (PASPORT_ID, "Passport"),
    )

    email = models.EmailField(unique= True)
    role = models.CharField(max_length=20, choices=ROLE, default=CUSTOMER)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(max_length=500, null=True, blank=True)
    is_kyc = models.BooleanField(default=False)
    kyc_doc = models.CharField(max_length=20, choices=KYC_TYPE, null=True, blank=True)
    kyc_id_number = models.CharField(max_length=20, null=True, blank=True)
    failed_attempts = models.PositiveIntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self) -> str:
        return self.full_name if self.full_name !=" " else self.email
    

    # over ride save method for admin use to rest failed attempts of customer
    # def save(self, *args, **kwargs):
    #     if not self.is_locked:
    #         self.failed_attempts = 0
    #     super(User, self).save(*args, **kwargs)

class AccountPassword(BaseModel):
    account_holder = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="passwords") 
    password = models.CharField(max_length=255)