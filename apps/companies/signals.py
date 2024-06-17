from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


from rest_framework.response import Response


from .models import CompanyApplication, Company,CompanyBalance


@receiver(post_save, sender=CompanyApplication)
def create_store_on_approval(sender, instance:CompanyApplication, created, **kwargs):
    if created or not instance.is_approved:
        return
    
    try:
        company=Company.objects.create(
            owner=instance.user, 
            legal_name=instance.legal_name, 
            phone=instance.phone,
            index=instance.index
            )
        if instance.legal_address: company.legal_address = instance.legal_address
        if instance.city: company.city = instance.city
        if instance.site_url: company.site_url = instance.site_url
        if instance.image: company.image = instance.image
        company.save()
        company.owner.role = "company"
        company.owner.save()
        company_balance = CompanyBalance.objects.create(company=company)
    
    except IntegrityError:
        raise ValidationError ("this user had a company or applications")

