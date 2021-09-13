from django.contrib import admin
from Lenders.models import Lenders

# admin.site.register(Lenders)

class FileAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "upfront_commission_rate",   "trial_commission_rate", "active"]

admin.site.register(Lenders, FileAdmin)
