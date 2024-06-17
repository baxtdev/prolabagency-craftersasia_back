from django.contrib import admin
from django.utils.safestring import mark_safe


from . import models
# Register your models here.

class ItemSubcatgoryInline(admin.TabularInline):
    model = models.ItemSubCategory
    extra = 0

class ItemPaymentInline(admin.TabularInline):
    model = models.ItemPayment
    extra = 0

class  ItemModelInline(admin.TabularInline):
    model = models.ItemModel
    extra = 0

class ItemModelImageInline(admin.TabularInline):
    model = models.ItemImages
    extra = 0
           


@admin.register(models.ItemCategory)
class ItemaCategoryAdmin(admin.ModelAdmin):
    inlines = [ItemSubcatgoryInline,]
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name','-id')


@admin.register(models.ItemSubCategory)
class ItemSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','category','get_image')
    search_fields = ('name','category__name',)
    list_filter = ('category',)
    @admin.display(description="img")
    def get_image(self, instance):
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="100px" />')
        else:
            return None


@admin.register(models.ItemViews)
class ItemViewsAdmin(admin.ModelAdmin):
    list_display = ('ip','user','item','timestamp')
    readonly_fields = ('user','ip','item','timestamp')
    search_fields = ('user__email', 'user__first_name', 'user__last_name','item__name')
    list_filter = ('item',)


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemModelInline,ItemPaymentInline]
    list_display = ('name','code','company','is_new','is_popular','get_image')
    readonly_fields = ('code',)
    search_fields = ('name','company__legal_name','company__owner__first_name','company__owner__last_name')
    list_filter = ('category','company','is_new','is_popular')
   
    @admin.display(description="img")
    def get_image(self, instance):
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="100px" />')
        else:
            return None


@admin.register(models.ItemModelName)
class ItemModelNameAdmin(admin.ModelAdmin):
    list_display=('item','name')
    search_fields = ('item__name','name',)
    list_filter = ('item',)
    ordering = ('item','-id')



@admin.register(models.ItemModel)
class ItemModelAdmin(admin.ModelAdmin):
    inlines = [ItemModelImageInline,]
    list_display = ('name_model','color','quantity','price','item')
    search_fields = ('name_model','color__name','item__name')
    list_filter = ('color','item','item__company')

@admin.register(models.ItemImages)
class ItemImagesAdmin(admin.ModelAdmin):
    list_display = ('item_model','get_image')
    search_fields = ('item_model__name_model','item_model__name')
    list_filter = ('item_model__item',)

    @admin.display(description="img")
    def get_image(self, instance):
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="100px" />')
        else:
            return None
        
@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name','color')
    search_fields = ('name',)
    ordering = ('name','-id')


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name','code')
    search_fields = ('name',)
    ordering = ('name','-id')


@admin.register(models.FavoriteItems)
class FavoriteItemsAdmin(admin.ModelAdmin):
    list_display = ('item','user')
    search_fields = ('item__name','user__first_name','user__last_name')
    list_filter = ('item','user')


@admin.register(models.ItemPayment)
class ItemPaymentAdmin(admin.ModelAdmin):
    list_display = ('item','terms_of_payment','delivery_conditions','use_mbank')
    search_fields = ('item__name','terms_of_payment')
    list_filter = ('use_mbank',)

@admin.register(models.ItemReviews)
class ItemReviewsAdmin(admin.ModelAdmin):
    list_display = ('item','user','delivery','quality','price_relevance')
    search_fields = ('item__name','user__first_name','user__last_name','company__legal_name')
    list_filter = ('item','user')