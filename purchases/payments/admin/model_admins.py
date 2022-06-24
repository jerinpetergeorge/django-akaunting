from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from import_export.admin import ExportMixin
from rangefilter.filters import DateRangeFilter

from ..admin import views
from ..models import Payment
from .resource import PaymentResource


@admin.register(Payment)
class PaymentAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PaymentResource
    search_fields = ("item", "vendor__name", "category__name", "amount")
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
    list_filter = ["category", "vendor", "payment_method", ("date", DateRangeFilter)]

    def get_admin_action_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = [
            path(
                "actions/bulk-update/",
                views.PaymentBulkUpdateView.as_view(),
                name="%s_%s_bulk_update" % info,
            ),
        ]
        return urls

    def get_urls(self):
        admin_action_urls = self.get_admin_action_urls()
        urls = super().get_urls()
        return admin_action_urls + urls

    def file(self, obj: Payment):
        if not obj.attachment:
            return
        return format_html(
            f"<a href='{obj.attachment.url}'  " f"target='_blank' >Link</a>",
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request=request)
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        return super().save_model(request, obj, form, change)

    #################
    # Admin Actions #
    #################

    actions = ["bulk_update"]

    def bulk_update(self, request, queryset):
        changelist_url = reverse("admin:payments_payment_changelist")
        bulk_update_url = reverse("admin:payments_payment_bulk_update")
        pks = ",".join(map(str, queryset.values_list("pk", flat=True)))
        return HttpResponseRedirect(
            redirect_to=f"{bulk_update_url}?pks={pks}&from={changelist_url}",
        )
