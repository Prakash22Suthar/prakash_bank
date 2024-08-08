from django.contrib import admin

from .models import User
# Register your models here.


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ["full_name","email","role","is_active"]
    list_display_links = ["full_name","email"]

