from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField

from apps.channels.models import TimeStampAbstractModel
from apps.channels.utils import generate_code
from .managers import UserManager


class User(AbstractUser,TimeStampAbstractModel):
    phone=PhoneNumberField(
        'Телефон',
        unique=True,
        blank=True, 
        null=True
    )
    image = ResizedImageField(
        upload_to='avatars/', 
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        blank=True,
        null=True,
    ) 
    username = None
    middle_name = models.CharField(
        max_length=255, 
        verbose_name='Отчество',
        )
    last_activity = models.DateTimeField(
        auto_now=True,
        verbose_name=('last activity'),
    )
    email = models.EmailField(
        _("Эл.почта"), 
        max_length=254,
        unique = True,
        )
    ORG = 'company'
    CLI = 'client'
    ROLE_CHOICE=(
        (ORG,'Компания'),
        (CLI,'Клиент'),
    )
    role = models.CharField(
        choices = ROLE_CHOICE,
        max_length = 30,
        default = CLI,
        verbose_name=_("Роль")
    )
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()
    
    class Meta:
        db_table = 'users'
        managed = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name} {self.middle_name}"




class AccountSettings(TimeStampAbstractModel):  
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name='settings',
        verbose_name=_("Пользователь")
        )
    delivery_info = models.TextField(
        _("Политика доставки"),
        blank=True,
        null=True
        )
    terms_of_payment = models.TextField(
        _("Условия платежа"),
        blank=True,
        null=True
        )
    mbank = models.BooleanField(
        _("Метод Платежа (MBANK)"),
        default=False
    )
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Поитика Оплаты Аканута'
        verbose_name_plural = 'Поитика Оплаты Аканутов'

    def __str__(self) -> str:
        return f"{self.user.email}-{self.mbank}"


class ResetPasword(TimeStampAbstractModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='codes',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Активность")
    )
    code = models.IntegerField(
        unique=True,
        blank=True,
        null=True
    )
    data = models.DateField(
        auto_now_add=True,
        auto_created=True,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        code = generate_code()
        if not self.code:
            self.code = code
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.email}---{self.data}"
        
    class Meta:
        db_table = 'codes_res_password'
        managed = True
        verbose_name = 'Код для сброса пароля'
        verbose_name_plural = 'Коды для  сброса пароля'  

