from django.db import IntegrityError
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models import Q

from apps.chat.models import ChatRoom,ChatUser,MessageChat
from apps.chat.consumers import SEND_MESSAGE, NEW_MESSAGE

from .models import OrderItems,Order

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=OrderItems)
def send_message_for_orders(sender, instance:OrderItems, created, **kwargs):
    if created:
        chat_user,created_user = ChatUser.objects.get_or_create(
            user=instance.order.user,
            )
        chat_user.name=instance.order.user.get_full_name
        chat_user.avatar=instance.order.user.image if instance.order.user.image else None
        chat_user.save()        
    
        company_owner,created_company = ChatUser.objects.get_or_create(
            user=instance.company.owner
            )     
        company_owner.name=instance.company.owner.get_full_name
        company_owner.avatar=instance.company.owner.image if instance.company.owner.image else None
        company_owner.save()

        chat_room = ChatRoom.objects.filter(users__user=chat_user.user).filter(users__user=company_owner.user)
        
        if chat_room.exists():
            chat_room = chat_room.first()
            message_chat = MessageChat.objects.create(chat_user=company_owner,room=chat_room,
                                                    body=f"""Уважаемый (-ая), {chat_user.name}!\n
                                                    Поздравляем! Ваша заявка (№ {instance.id}) для продавца {instance.company.legal_name} принята.\n
                                                    Всего товаров: \n
                                                    1. {instance.item.name}-{instance.item_model.name_model}-{instance.item_model.color.name}\n
                                                    Количество: {instance.quantity}\n
                                                    Цена: {instance.item_model.price} {instance.item_model.currency}.\n
                                                    Сумма: {instance.item_totals}.\n
                                                    Спасибо за Вашу заявку. Продавец {company_owner.name} свяжется с Вами для подтверждения.\n
                                                    Будем рады ответить на Ваши вопросы: {company_owner.user.email} ежедневно с 9:00 до 18:00. Мы всегда готовы помочь Вам!
                                                    С уважением, команда CRAFTER ASIA"""
                                                      )
            message_chat.save()

        else:
            chat_room = ChatRoom.objects.create(name=f"{instance.company.owner.email}-{instance.order.user.email}")
            chat_room.users.add(chat_user,company_owner)
            message_chat = MessageChat.objects.create(chat_user=company_owner,room=chat_room,
                                                      body=f"""Уважаемый (-ая), {chat_user.name}!
                                                    Поздравляем! Ваша заявка (№ {instance.id}) для продавца {instance.company.legal_name} принята.
                                                    Всего товаров: 
                                                    1. {instance.item.name}-{instance.item_model.name_model}-{instance.item_model.color.name}-Кабель мультимедийный Display Port to DVI 24+1pin, 1.0m Cablexpert (CC-DPM-DVIM-1M)
                                                    Количество: {instance.quantity}
                                                    Цена: {instance.item_model.price} {instance.item_model.currency}.
                                                    Сумма: {instance.item_totals}.
                                                    Всего: 246.00 грн.

                                                    Спасибо за Вашу заявку. Продавец {company_owner.name} свяжется с Вами для подтверждения.
                                                    Будем рады ответить на Ваши вопросы: {company_owner.user.email} ежедневно с 9:00 до 18:00. Мы всегда готовы помочь Вам!

                                                    С уважением, команда CRAFTER ASIA"""
                                                    )
            message_chat.save()


        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{chat_room.uuid}',
            {
                'type': SEND_MESSAGE,
                'body': message_chat.body,
                'file': None,
                'photo': None,
                'created_at': str(message_chat.created_at),
                'name': message_chat.chat_user.name,
                'type_message': message_chat.type,
                'avatar': message_chat.chat_user.user.image.url if message_chat.chat_user.user.image else None,
                'chat_user_id': message_chat.chat_user.id,
                'user_id': message_chat.chat_user.user.id
            }
        )
        to_chat_user: ChatUser = chat_room.users.exclude(user=company_owner.user).first()
        async_to_sync(channel_layer.group_send)(
            f'online_user_{to_chat_user.id}',
            {
                'type': NEW_MESSAGE,
                'created_at': str(message_chat.created_at),
                'room_uuid': str(chat_room.uuid),
                'message_id': message_chat.id,
                'type_message': message_chat.type,
                'chat_user_id': message_chat.chat_user.id,
                'user_id': message_chat.chat_user.user.id
            }
        )    