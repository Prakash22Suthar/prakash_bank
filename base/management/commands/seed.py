from typing import Any
from django.core.management import BaseCommand, call_command
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import get_hasher
from django.conf import settings
from users.models import AccountPassword


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        self.user_class = get_user_model()
        super().__init__()
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        apps = settings.INSTALLED_APPS
        for app in apps :
            call_command("makemigrations", app.split(".")[-1])
        call_command("migrate")
        self.create_super_user()

    def create_super_user(self):
        admin_user = self.user_class.objects.filter(email="admin@mail.com")
        if admin_user.exists():
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(f"Admin account '{admin_user.last().email}' already exists")
            return False
        admin_user = self.user_class.objects.create(
            username="admin1",
            email="admin@mail.com"
        )
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.role = "a"
        admin_user.set_password("admin")
        admin_user.save()

        
        hasher = get_hasher()
        encoded_password = hasher.encode("admin", hasher.salt())
        AccountPassword.objects.create(
                account_holder = admin_user,
                password = encoded_password
            )
        self.stdout.write(f"Admin Account '{admin_user.email}' Created.")