from django.contrib import admin
from .models import RobotAlert

@admin.register(RobotAlert)
class RobotAlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'robot', 'alert_type', 'created_at')
    search_fields = ('alert_type', 'message', 'robot__name')
    list_filter = ('alert_type', 'created_at')
