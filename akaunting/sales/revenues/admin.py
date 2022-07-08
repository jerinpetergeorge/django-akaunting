from django.contrib import admin

from .models import Revenue


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "date", "customer", "category")
