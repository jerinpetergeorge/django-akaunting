from django.contrib import admin


class FileFilter(admin.SimpleListFilter):
    title = "File"
    parameter_name = "has_files"

    def lookups(self, request, model_admin):
        return [
            (True, "Has files"),
            (False, "Has no files"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "True":
            return queryset.exclude(attachment="")
        elif value == "False":
            return queryset.filter(attachment="")
        return queryset
