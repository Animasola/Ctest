from django.contrib import admin
from my_info.models import Contact


class ContactAdmin(admin.ModelAdmin):
    search_fields = ['last_name', 'name']


admin.site.register(Contact, ContactAdmin)
