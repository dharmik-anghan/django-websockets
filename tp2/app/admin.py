from django.contrib import admin
from app.models import Chat, Group


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'created_at', 'group']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']