from django.contrib import admin

from user.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    prepopulated_fields = {'slug': ('username',)}


admin.site.register(Profile, ProfileAdmin)
