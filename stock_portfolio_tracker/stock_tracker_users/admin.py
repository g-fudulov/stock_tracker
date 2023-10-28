from django.contrib import admin
# from models import MyUser
from ..stock_tracker_stocks.models import MyUser


# Register your models here.
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_filter = ('email', "id", 'is_staff', 'is_superuser')
    list_display = ('email', "id", 'is_staff', 'is_superuser')
    search_fields = ('email', "id")
    ordering = ('-id',)
