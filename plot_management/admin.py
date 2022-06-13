from django.contrib import admin
from .models import *

# Register your models here.


class StatusAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'title']
    list_per_page = 10


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Status, StatusAdmin)
admin.site.register(Member)
admin.site.register(PaymentStatus)
admin.site.register(OfflinePayment)
