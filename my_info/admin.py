from django.contrib import admin
from my_info.models import Contact, LoggedRequest


class ContactAdmin(admin.ModelAdmin):
    search_fields = ['last_name', 'name']


class LoggedRequestAdmin(admin.ModelAdmin):
    list_display = ['url', 'request_type', 'timestamp', 'priority']

admin.site.register(Contact, ContactAdmin)
admin.site.register(LoggedRequest, LoggedRequestAdmin)
