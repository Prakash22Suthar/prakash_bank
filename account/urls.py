from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import AccountViewset, TransactionViewset

app_name = "account"

router = DefaultRouter()

router.register("account", AccountViewset, basename= "account")
router.register("transaction", TransactionViewset, basename= "transaction")


urlpatterns = [
    path("", include(router.urls))
]