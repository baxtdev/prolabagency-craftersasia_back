from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User,ResetPasword,AccountSettings

from apps.companies.models import Company
# Register your models here.

class CompanyInline(admin.StackedInline):
    model = Company
    extra = 0
    fk_name = 'owner'
    can_delete = False
    show_change_link = False
    show_delete = False
    show_add = False
    

class AccoountSettingsInline(admin.TabularInline):
    model = AccountSettings
    extra = 0
    can_delete = False
    show_change_link = False
    show_delete = False
    show_add = False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [CompanyInline,AccoountSettingsInline]
    list_display = ('email','phone','first_name','is_active','role','get_image')
    list_filter = ('is_active','role','is_staff','is_superuser',)

    @admin.display(description="Аватар")
    def get_image(self, instance):
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="100px" />')
        else:
            return None
        
@admin.register(ResetPasword)
class ResetPasswordAdmin(admin.ModelAdmin):
    list_display = ('user','is_active','code','data')
    readonly_fields = ('code','is_active','data')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')