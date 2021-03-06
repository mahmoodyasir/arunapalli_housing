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
    search_fields = ['id', 'owner_email']
    list_display = ['id', 'owner_email', 'plot_no', 'road_no', 'member_status', 'date']
    list_per_page = 10


class MemberAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'email', 'member_firstname', 'member_lastname', 'member_nid', 'member_phone', 'onetime_payment']
    list_per_page = 10


class OfflinePaymentAdmin(admin.ModelAdmin):
    search_fields = ['id', 'member_email']
    list_display = ['id', 'member_email', 'cheque_number', 'account_no', 'member_nid', 'plot_no', 'road_no', 'member_status', 'paid_amount', 'start_date', 'end_date', 'payment_date']
    list_per_page = 10


class TrackMembershipPaymentAdmin(admin.ModelAdmin):
    search_fields = ['id', 'member_email']
    list_display = ['id', 'member_email', 'online_email', 'member_status', 'plot_no', 'road_no', 'payment_type',
                    'payment_status', 'start_date', 'end_date', 'date']
    list_per_page = 10


class PayOnlineAdmin(admin.ModelAdmin):
    search_fields = ['id', 'email']
    list_display = ['id', 'email', 'transaction_id', 'medium', 'member_nid', 'plot_no', 'road_no', 'member_status',
                    'paid_amount', 'start_date', 'end_date', 'payment_date']
    list_per_page = 10


class MemberHistoryAdmin(admin.ModelAdmin):
    search_fields = ['id', 'owner_email']
    list_display = ['id', 'owner_email', 'member_firstname', 'member_lastname', 'member_nid', 'member_phone', 'plot_no', 'road_no', 'member_status', 'date']
    list_per_page = 10


class TrackDueTableAdmin(admin.ModelAdmin):
    search_fields = ['id', 'owner_email']
    list_display = ['id', 'owner_email', 'start_date', 'end_date', 'paid', 'plot_no', 'member_status', 'amount', 'date']
    list_per_page = 10


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(PaymentStatus)
admin.site.register(OfflinePayment, OfflinePaymentAdmin)
admin.site.register(RoadNumber)
admin.site.register(PlotNumber)
admin.site.register(PlotPosition, PlotPositionAdmin)
admin.site.register(OnetimeMembershipPayment)
admin.site.register(AdminUserInfo)
admin.site.register(PaymentDateFix)
admin.site.register(TrackPlotOwnership, TrackPlotOwnershipAdmin)
admin.site.register(TrackMembershipPayment, TrackMembershipPaymentAdmin)
admin.site.register(PayOnline, PayOnlineAdmin)
admin.site.register(MemberHistory, MemberHistoryAdmin)
admin.site.register(OnetimeAmount)
admin.site.register(BankName)
admin.site.register(TrackDueTable, TrackDueTableAdmin)



