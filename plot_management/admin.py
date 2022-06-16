from django.contrib import admin
from .models import *

# Register your models here.


class StatusAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'title', 'payment_range']
    list_per_page = 10


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'prouser', 'image']
    list_per_page = 10


class UserAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'email', 'is_staff']
    list_per_page = 10


class PlotPositionAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'plot_no', 'road_no', 'date']
    list_per_page = 10


class TrackPlotOwnershipAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'owner_email', 'plot_no', 'road_no', 'date']
    list_per_page = 10


class MemberAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'email', 'member_firstname', 'member_lastname', 'member_nid', 'member_phone', 'member_status', 'onetime_payment']
    list_per_page = 10


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(PaymentStatus)
admin.site.register(OfflinePayment)
admin.site.register(RoadNumber)
admin.site.register(PlotNumber)
admin.site.register(PlotPosition, PlotPositionAdmin)
admin.site.register(OnetimeMembershipPayment)
admin.site.register(AdminUserInfo)
admin.site.register(PaymentDateFix)
admin.site.register(TrackPlotOwnership, TrackPlotOwnershipAdmin)
admin.site.register(TrackMembershipPayment)



