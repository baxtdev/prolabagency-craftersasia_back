from django.contrib import admin

from .models import Order,OrderItems
# Register your models here.

class OrderItemsInlin(admin.TabularInline):
    model = OrderItems
    extra = 0
    readonly_fields = ('company','order','item','item_model','quantity','color')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemsInlin,]
    list_display = ('user','name','phone','status','created_at')
    readonly_fields = ('user','name','phone','comment')
    list_filter = ('status',)

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order','item','status','quantity','color')
    list_filter = ('status',)
    search_fields = ('order__user__first_name','order__user__last_name','item__name','item_model__item_model__name')