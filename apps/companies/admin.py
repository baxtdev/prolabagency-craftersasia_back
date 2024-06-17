from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.safestring import mark_safe 

from .models import Company,CompanyApplication,RateComission,CompanyBalance
# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('legal_name','legal_address','phone','rate','get_image')
    list_filter = ('rate',)
    readonly_fields = ('owner','legal_name','legal_address','phone')
    search_fields = ('legal_name','legal_address','phone','owner__first_name','owner__last_name','owner__middle_name')
   
    @admin.display(description="img")
    def get_image(self, instance):
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="100px" />')
        else:
            return None

@admin.register(CompanyApplication)
class CompanyApplicationAdmin(admin.ModelAdmin):
    list_display = ('user','legal_name','legal_address','phone','is_approved','get_image')
    readonly_fields = ('user','phone',)
    list_filter = ('is_approved',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name','legal_name', 'legal_address')
    @admin.display(description="img")
    def get_image(self, instance):
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="100px" />')
        else:
            return None

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        return queryset.filter(is_approved=False)
    
@admin.register(CompanyBalance)
class ConmpanyBalanceAdmin(admin.ModelAdmin):
    list_display = ('company','amount','balance','is_active')
    search_fields = ('company__legal_name','company__owner__first_name','company__owner__last_name')
    list_filter = ('is_active',)

@admin.register(RateComission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('name','comission_percent')
    search_fields = ('name',)
    ordering = ('comission_percent',)
    