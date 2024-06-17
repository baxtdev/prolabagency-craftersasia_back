from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from phonenumber_field.modelfields import PhoneNumberField
from django_resized import ResizedImageField

from apps.channels.models import TimeStampAbstractModel

class RateComission(models.Model):
    name = models.CharField(
        _("Название"), 
        max_length=350
        )
    comission_percent = models.FloatField(
        _("Процент"),
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        verbose_name = 'Комиссия'
        verbose_name_plural = 'Комиссии'

    def __str__(self) -> str:
        return self.name
    

    
class Company(TimeStampAbstractModel):
    owner = models.OneToOneField(
        "users.User", 
        verbose_name=_("Владелец"), 
        on_delete=models.CASCADE,
        related_name="company" 
        )
    legal_name = models.CharField(
        _("Название"), 
        max_length=350
        )
    legal_address = models.CharField(
        _("Aдрес"), 
        max_length=150,
        blank=True, null=True
        )
    phone = PhoneNumberField(
        _("Телефон"),
        )
    city = models.CharField(
        _("Город"), 
        max_length=100,
        blank=True, null=True
        )
    index = models.PositiveIntegerField(
        _("Индекс")
    )
    site_url = models.URLField(
        _("Ссылка сайта"), 
        max_length=200,
        blank=True, null=True
        )
    image = ResizedImageField(
        upload_to='avatars/', 
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        blank=True,
        null=True,
    ) 
    rate = models.ForeignKey(
        'RateComission',
        verbose_name=_('Рейтинг'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='company'
        )
    
    
    class Meta:
        db_table = 'companies'
        managed = True
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ('-created_at', '-updated_at','-id')

    def __str__(self) -> str:
        return f"{self.legal_name}-{self.owner.email}"    


    @property
    def buys_count(self):
        items = self.orders.all().count()
        return items

    @property
    def raiting(self):
        score = 5
        return score
    
    @property
    def buys_count(self):
        items = self.items.all().count()
        return items
    
    @property
    def count_of_fives(self):
        items = self.items.all().count()
        return items
    
    @property
    def count_of_fourths(self):
        items = self.items.all().count()
        return items
    
    @property
    def count_of_threes(self):
        items = self.items.all().count()
        return items
    
    @property
    def count_of_twos(self):
        items = self.items.all().count()
        return items
    
    @property
    def count_of_ones(self):
        items = self.items.all().count()
        return items
    
    @property
    def marks_in_last_month(self):
        delivery = self.items.all().count()
        qulaity = self.items.all().count()
        price = self.items.all().count()

        data = {
            "delivery": delivery,
            "price": price,
            "quality": qulaity
        }

        return data
    
    @property
    def marks_in_two_month(self):
        delivery = self.items.all().count()
        qulaity = self.items.all().count()
        price = self.items.all().count()

        data = {
            "delivery": delivery,
            "price": price,
            "quality": qulaity
        }

        return data
    
    @property
    def marks_in_last_year(self):
        delivery = self.items.all().count()
        qulaity = self.items.all().count()
        price = self.items.all().count()

        data = {
            "delivery": delivery,
            "price": price,
            "quality": qulaity
        }

        return data
    

    


class CompanyBalance(TimeStampAbstractModel):
    company = models.OneToOneField(
        "Company", 
        verbose_name=_("Компания"),
        on_delete=models.CASCADE,
        related_name="balance"
    )
    amount = models.DecimalField(
        _("Сумма депозита"),
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    balance = models.DecimalField(
        _("Сумма продажи"),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    is_active=models.BooleanField(
        _("Активность"),
        default=False
    )


    class Meta:
        db_table = 'company_deposits'
        managed = True
        verbose_name = 'Депозит и Баланс компании'
        verbose_name_plural = 'Депозиты и Баланс компаний'

    def __str__(self):
        return f"{self.company} - {self.amount}"

    @property
    def sold_items(self):
        items = self.company.items.all().count()
        return items

    @property
    def days_transaction_closing(self):
        days = 3
        return days   

    def clean(self):
        super().clean()
        if not self.company.rate:
            raise ValidationError(f'Компания {self.company} не имеет рейтинг')


class CompanyPayAccount(TimeStampAbstractModel):
    MBANK="MBANK"
    VISA="VISA"
    WITH_OUT="WITH_OUT"

    company = models.ForeignKey(
        "Company", 
        verbose_name=_("Компания"),
        on_delete=models.CASCADE,
        related_name="payment"
        )
    PAYMENT_CHOICES = (
        (MBANK, "МБАНК"),
        (VISA, "VISA"),
        (WITH_OUT, "Без оплаты"),
    )
    payment_type = models.CharField(
        _("Тип оплаты"), 
        max_length=15,
        choices=PAYMENT_CHOICES,
        default=WITH_OUT
        )
    api_key = models.CharField(max_length=255)  
    bank_account = models.CharField(max_length=255)
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Счет Компании для Оплаты '
        verbose_name_plural = 'Счета Компании для Оплаты'
        unique_together = ('company','payment_type')
        ordering = ('-id','created_at',)

    def __str__(self) -> str:
        return f"{self.company.name}--{self.payment_type}"    



class CompanyApplication(TimeStampAbstractModel):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name="applications"
        )
    
    legal_name = models.CharField(
        _("Название"), 
        max_length=350
        )
    legal_address = models.CharField(
        _("Aдрес"), 
        max_length=150,
        blank=True, null=True
        )
    phone = PhoneNumberField(
        _("Телефон"),
        )
    city = models.CharField(
        _("Город"), 
        max_length=100,
        blank=True, null=True
        )
    index = models.PositiveIntegerField(
        _("Индекс")
    )
    site_url = models.URLField(
        _("Ссылка сайта"), 
        max_length=200,
        blank=True, null=True
        )
    image = ResizedImageField(
        upload_to='avatars/', 
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        blank=True,
        null=True,
    )
    is_approved = models.BooleanField(
        _("Статус"),
        default=False,
        help_text="Чтобы принимать заявку установите этот флажок"
        )
    
    class Meta:
        db_table = 'store_aplications'
        managed = True
        verbose_name = "Заявка на открытие магазина"
        verbose_name_plural = "Заявки на открытие магазинов"
        ordering = ('-created_at', '-updated_at','-id')

    def __str__(self) -> str:
        return f"{self.legal_name}-{self.user.email}"    
