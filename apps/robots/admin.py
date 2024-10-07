from django.contrib import admin
from .models import Robot


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'ip_address', 'platform', 'status')
    list_filter = ('status', 'platform')
    search_fields = ('id', 'user_id__username', 'ip_address')
