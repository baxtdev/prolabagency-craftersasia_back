from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver

from .models import Item


@receiver(post_save, sender=Item)
def create_item_code(instance:Item, created,*args,**kwargs):
    number_example = "000000"

    if created:
        len_id = len(str(instance.id))
        number_example_len = len(number_example)    
        number_example = number_example[0:number_example_len-len_id]
        card_number = str(number_example)+str(instance.id)
        instance.code=card_number
        instance.save()