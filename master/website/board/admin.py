from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id',)
    # list_filter = ('updt_dt',)
    # search_fields = ('name', 'content')
