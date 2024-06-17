import random
from celery import shared_task
from apps.channels.services import ChekPopularItem
from apps.channels.utils import send_code

@shared_task(name="chek_popular_items")
def che_popular_items():
    cheking =  ChekPopularItem()
    return cheking.chek_items_to_popular()

@shared_task(name="send_to_email")
def send_email(code,email):
    task = send_code(code,email)
    return task