from django.contrib import admin

from chatapp.models import User, Message, Chat


# Register your models here.
class TokenAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(User)
admin.site.register(Message)
admin.site.register(Chat)
