from django.contrib import admin

from .models import Event, Webhook


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "enabled")
    list_display_links = ("id", "name")
    list_filter = ("enabled",)
    search_fields = ("name",)


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nickname",
        "url",
        "enabled",
    )
    list_display_links = ("id", "nickname")
    list_filter = ("enabled",)
    search_fields = ("nickname", "url", "events__name")
    readonly_fields = ["user"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        return super().save_model(request, obj, form, change)
