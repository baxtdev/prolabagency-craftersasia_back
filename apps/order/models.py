from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


from phonenumber_field.modelfields import PhoneNumberField
from apps.users.models import User
from apps.channels.models import TimeStampAbstractModel
# Create your models here.


class Order(TimeStampAbstractModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("Заказчик")
    )
    name = models.CharField(
        _("Имя Заказчика"),
        max_length=100,
    )
    phone = PhoneNumberField(
        _("Телефон Заказчика"),
    )
    comment = models.TextField(
        _("Коментария Заказчика"),
        blank=True,
        null=True
    )
    IN_BROWSING = "in browsing"
    IN_PROCESSING = "in processing"
    DONE = "Done"
    REJECT = "Reject"
    
    STATUS_CHOICE = (
        (IN_BROWSING,"в просмотре"),
        (IN_PROCESSING,"в процессе"),
        (DONE,"Получено"),
        (REJECT,"ОТКЛОНЕН")
    )

    status = models.CharField(
        max_length=30,
        choices = STATUS_CHOICE,
        default = IN_BROWSING,
    )

    class Meta:
        verbose_name = "Заказ от клиента"
        verbose_name_plural = "Заказы от клиентов"

    def __str__(self) -> str:
        return f"{self.user.email}--{self.name}"    

    @property
    def total(self):
            total = [x.item_totals for x in self.items.all()]
            return sum(total)
    
    @property
    def count_items(self):
        total = [x.quantity for x in self.items.all()]
        return sum(total)
    



class OrderItems(TimeStampAbstractModel):
    company = models.ForeignKey(
        "companies.Company", 
        verbose_name=_("Компания"), 
        on_delete=models.CASCADE,
        related_name="orders",
        blank=True, null=True
        )
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Товары заказа")
    )
    item = models.ForeignKey(
        'store.Item',
        related_name="orders",
        on_delete=models.CASCADE,
        verbose_name="Товара"
    )
    item_model = models.ForeignKey(
        'store.ItemModel',
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("Модель Товара"),
        blank=True,
        null=True
    )
    quantity = models.PositiveIntegerField(
        _("Количество"),
        default=1,
    )
    color = models.ForeignKey(
        'store.Color',
        on_delete = models.SET_NULL,
        blank=True, 
        null=True,
    )
    IN_BROWSING = "in browsing"
    IN_PROCESSING = "in processing"
    DONE = "Done"
    REJECT = "Reject" 

    STATUS_CHOICE = (
        (IN_BROWSING,"в просмотре"),
        (IN_PROCESSING,"в процессе"),
        (DONE,"Получено"),
        (REJECT,"ОТКЛОНЕН")
    )

    status = models.CharField(
        max_length=30,
        choices = STATUS_CHOICE,
        default = IN_BROWSING,
    )

    class Meta:
        verbose_name = "Товар Заказа"
        verbose_name_plural = "Товары Заказа"

    def __str__(self) -> str:
        return f"{self.item.name}-{self.order.user.email}"    

    def clean(self):
        super().clean()
        if not self.item_model in self.item.models.all():
            raise ValidationError(f'Товар {self.item} не имеет такого Модела {self.item_model}')
        
        if self.company and not self.item in self.company.items.all():
            raise ValidationError(f'Кмпания {self.company} не имеет такого товра как {self.item}')

        if self.order.user.role is User.ORG:
            if self.item in self.order.user.company.items.all():
                raise ValidationError('Не полуться купить свой же тур')
    
    @property
    def item_totals(self):
        return self.quantity*self.item_model.price
    
