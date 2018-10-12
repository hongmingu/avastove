from django.contrib import admin
from .models import *

# Register your models here.

'''
class TestModelAdmin(admin.ModelAdmin):
    fields = ('description', 'updated', 'created')


class TestModelLogAdmin(admin.ModelAdmin):
    fields = ('description', 'status', 'created')


admin.site.register(TestModel, TestModelAdmin)
admin.site.register(TestModelLog, TestModelLogAdmin)

'''
admin.site.register(UserUsername)
admin.site.register(UserTextName)
admin.site.register(UserPrimaryEmail)
admin.site.register(UserPrimaryEmailAuthToken)

admin.site.register(UserPasswordResetToken)
admin.site.register(UserDelete)
admin.site.register(UserPhoto)
