from django.contrib import admin
from django.utils.html import format_html

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display_links = ("id", "item", "file")
    list_display = (
        "id",
        "item",
        "amount",
        "date",
        "vendor",
        "category",
        "payment_method",
        "file",
    )
    readonly_fields = ["user"]
    list_filter = ["category", "vendor", "payment_method"]

    def file(self, obj: Payment):
        if not obj.attachment:
            return
        return format_html(
            f"<a href='{obj.attachment.url}'  " f"target='_blank' >Link</a>"
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request=request)
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        return super().save_model(request, obj, form, change)
