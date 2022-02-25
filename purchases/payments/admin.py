from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "item",
        "amount",
        "date",
        "vendor",
        "category",
        "payment_method",
        "user",
    )
    readonly_fields = ["user"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)
