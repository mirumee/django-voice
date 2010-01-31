from django.contrib import admin
from djangovoice.models import Feedback, Status, Type


class StatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Feedback)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)
