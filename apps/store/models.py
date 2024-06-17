import random
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField
from django_resized import ResizedImageField

from apps.channels.models import TimeStampAbstractModel
# Create your models here.

class Color(models.Model):
    name = models.CharField(
        _("Название"), 
        max_length=50
        )
    color = ColorField()

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self) -> str:
        return self.name    


class Currency(models.Model):
    name = models.CharField(
        _("Навзвание"),
        max_length=50
        )
    code = models.CharField(
        _("Код"), 
        max_length=5
        )
    
    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self) -> str:
        return f"{self.name}-{self.code}"


class ItemCategory(TimeStampAbstractModel):
    name = models.CharField(
        _("Название"), 
        max_length=150
        )
    description = models.TextField(
        _("Описание"),
        blank=True, 
        null=True
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Категория Товаров'
        verbose_name_plural = 'Категории Товаров'

    def __str__(self) -> str:
        return self.name


class ItemSubCategory(models.Model):
    category = models.ForeignKey(
        "ItemCategory", 
        verbose_name=_("Главная категория"), 
        on_delete=models.CASCADE,
        related_name="subcategories" 
        )
    name = models.CharField(
        _("Название"), 
        max_length=150
        )
    description = models.TextField(
        _("Описание"),
        blank=True, 
        null=True
    )
    image = ResizedImageField(
        upload_to='subcategories/', 
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        blank=True,
        null=True,
    ) 

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Подкатегория Товаров'
        verbose_name_plural = 'подкатегории Товаров'

    def __str__(self) -> str:
        return self.name



class ItemViews(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,blank=True,null=True,related_name="view_items")
    ip = models.CharField(max_length=50,blank=True,null=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE,related_name="views")
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'item')
        verbose_name = 'Просмотр Товара'
        verbose_name_plural = 'Просмотры Товаров'

    def __str__(self) -> str:
        return f"{self.ip}-{self.user}"    


class Item(TimeStampAbstractModel):
    code = models.CharField(
        max_length=6,
        blank=True,
        null=True 
    )
    company = models.ForeignKey(
        'companies.Company',
        related_name="items",
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        "ItemCategory", 
        verbose_name=_("Категория"), 
        on_delete=models.CASCADE,
        related_name="items",
        blank=True, 
        null=True
        )
    subcategory = models.ForeignKey(
        'ItemSubCategory', 
        related_name='items', 
        on_delete=models.CASCADE,
        )
    name = models.CharField(
        _("Название"), 
        max_length=250
        )
    description = models.TextField(
        _("Описание Товара")
        )
    main_features = models.TextField(
        _("Особенности Товара")
        )
    is_new = models.BooleanField(
        _("Новинка"),
        default=True,
        )
    is_popular = models.BooleanField(
        _("Популярный"),
        default=False,
    )
    views_count = models.IntegerField(
        _("Кол-во просмотров"),
        default=0
    )

    class Meta:
        db_table = 'items'
        managed = True
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return self.name
    
    @property
    def price(self):
        return self.models.first().price
    
    @property
    def discount_price(self):
        return self.models.first().discount
    
    @property
    def image(self):
        model = self.models.first()
        image = model.images.first() if model else None
        if image:
            return image.image
        else:
            return None

    def increment_views(self, user,ip):
        view,created = ItemViews.objects.get_or_create(ip=ip,item=self)
        if created:
            self.views_count +=1
            self.save()
        
        
        if user:
            try:    
                view.user = user

            except Exception as er:
                print(er)
                pass


        view.timestamp = timezone.now()    
        view.save()

    
    @property
    def raiting(self):
        marks = [x.quality for x in self.reviews.all()]
        sum_marks = sum(marks)
        raitng = sum_marks/self.reviews.count() if sum_marks else None
        return raitng

    @property
    def buys_count(self):
        orders = [x.quantity for x in self.orders.all()]
        if len(orders) >0:
            return sum(orders)
        return None
    
    @property
    def favorites_count(self):
        return self.favorites.count()



class ItemModelName(models.Model):
    item = models.ForeignKey(
        "Item", 
        verbose_name=_("Товар"), 
        on_delete=models.CASCADE,
        related_name="models_name",
    )
    name = models.CharField(
        _("Name"), 
        max_length=150
        )
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Типы Товара'
        verbose_name_plural = 'Типы Товара'

    def __str__(self) -> str:
        return f"{self.item.name}-{self.name}"    



class ItemModel(TimeStampAbstractModel):
    item_model = models.ForeignKey(
        'ItemModelName',
        related_name="colors",
        on_delete=models.CASCADE,
        blank=True,null=True,verbose_name="Тип Товара"
        )
    item = models.ForeignKey(
        "Item", 
        verbose_name=_("Товар"), 
        on_delete=models.CASCADE,
        related_name="models"
        )
    name_model = models.CharField(
        _("Название модела"), 
        max_length=150
        )
    color = models.ForeignKey(
        'Color', 
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name=_("Цвет"),
        )
    quantity = models.PositiveSmallIntegerField(
        _("Количество"),
        default=1
    )
    price = models.PositiveSmallIntegerField(
        _("Цена"),
    )
    currency = models.ForeignKey(
        'Currency',
        on_delete=models.CASCADE,
    )
    discount = models.PositiveSmallIntegerField(
        _("Скидка"),
        blank=True, 
        null=True
        )


    class Meta:
        db_table = 'item_models'
        managed = True
        verbose_name = 'Модель Товара'
        verbose_name_plural = 'Модели Товара'

    def __str__(self) -> str:
        return f"{self.name_model}-{self.item.name}"    
    

class ItemImages(TimeStampAbstractModel):
    image = models.ImageField(
        upload_to="items/",
    )    
    item_model = models.ForeignKey(
        "ItemModel", 
        verbose_name=_("Моде Товара"), 
        on_delete=models.CASCADE,
        related_name="images"
        )
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Фотографии модели  товара'
        verbose_name_plural = 'Фотографии модели  товара'

    def __str__(self) -> str:
        return f"{self.item_model.name_model}"    
    

class ItemPayment(TimeStampAbstractModel):
    item = models.OneToOneField(
        "Item", 
        verbose_name=_("Товар"), 
        on_delete=models.CASCADE,
        related_name="payments"
        )
    terms_of_payment = models.TextField(
        _("Условия платежа"),
        )    
    delivery_conditions = models.TextField(
        _("Условия доставки")
        )
    use_mbank = models.BooleanField(
        _("Мтод Платежа (MBANK)"),
        default=False,
        blank=True, 
        null=True
        )
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Платеж Товара'
        verbose_name_plural = 'Платежы Товара'

    def __str__(self) -> str:
        return self.item.name


class FavoriteItems(TimeStampAbstractModel):
    item = models.ForeignKey(
        "Item", 
        verbose_name=_("Товар"), 
        on_delete=models.CASCADE,
        related_name="favorites" 
        )
    user = models.ForeignKey(
        'users.User', 
        related_name='favorites', 
        on_delete=models.CASCADE
        )
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Избранный Товар'
        verbose_name_plural = 'Избранные Товары'
        unique_together = ('user', 'item')

    
    def __str__(self):
        return f"{self.item.name}-{self.user.email}"

    @property
    def count_add_users(self):
        return self.item.favorites.count()


class ItemReviews(models.Model):
    order = models.ForeignKey(
        'order.OrderItems',
        on_delete = models.SET_NULL,
        blank=True, 
        null=True
    )
    company = models.ForeignKey(
        'companies.Company', 
        related_name='reviews', 
        on_delete=models.CASCADE,
        verbose_name=_('Компания'),
        )
    item = models.ForeignKey(
        'Item', 
        related_name='reviews', 
        on_delete=models.SET_NULL,
        blank=True, 
        null=True,
        verbose_name=_("Товар")
        )
    user = models.ForeignKey(
        "users.User", 
        verbose_name=_("Клиент"), 
        on_delete=models.CASCADE,
        related_name = "feedbacks"
        )
    delivery = models.PositiveSmallIntegerField(
        _("Оценка для доставка"),
        blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    quality = models.PositiveSmallIntegerField(
        _("Оценка для качество"),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )    
    price_relevance = models.PositiveSmallIntegerField(
        _("Оценка для актуальность цены"),
        blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    advantages = models.CharField(
        _("Преимущества"), 
        max_length=250,
        blank=True, null=True
    )
    disadvantages = models.CharField(
        _("Недостатки"),
        max_length=250,
        blank=True, null=True
    )
    comment = models.TextField(
        _("Комментарий"),
        blank=True, null=True
    )
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-id',)

    def __str__(self):
        return f"{self.user.email}-{self.order}"
    
    def clean(self):
        super().clean()
        if not self.item in self.company.items.all():
            raise ValidationError(f'Товар {self.company} не имеет такого Товара {self.item}')
        
        if self.order.order.user!=self.user:
            raise ValidationError(f'Товар {self.user} не имеет права добавить отзыв на заказ{self.order}')
        if self.order.item != self.item:
            raise ValidationError(f'Товар {self.order} не имеет такого товара {self.item}')
        