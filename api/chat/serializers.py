from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User
from apps.chat.models import ChatRoom, ChatUser, MessageChat, RequestForSupport
from apps.channels.serializers import ShortDescUserSerializer


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = '__all__'


class ReadUserChatSerializer(serializers.ModelSerializer):
    user = ShortDescUserSerializer()

    class Meta:
        model = ChatUser
        fields = '__all__'


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'


class ReadChatRoomSerializer(serializers.ModelSerializer):
    users = ReadUserChatSerializer(many=True)
    unread_messages = serializers.SerializerMethodField('get_unread_messages')

    class Meta:
        model = ChatRoom
        fields = '__all__'

    def get_unread_messages(self, chat_room: ChatRoom) -> int:
        user: User = self.context['request'].user
        return chat_room.unread_messages(user)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        users = representation['users']
        for user in users:
            if user['user']['id'] != self.context['request'].user.id:
                representation['name'] = user['user']['email']

        return representation

class MessageChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageChat
        fields = '__all__'


class ReadMessageChatSerializer(serializers.ModelSerializer):
    chat_user = ReadUserChatSerializer()
    room = ChatRoomSerializer()

    class Meta:
        model = MessageChat
        fields = '__all__'


class CreateChatRoomSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    uuid = serializers.UUIDField(read_only=True)
    users = ReadUserChatSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ('name', 'user', 'users', 'uuid')

    def create(self, validated_data):
        request = self.context['request']
        user, to_user = request.user, validated_data.pop('user')
        if user == to_user:
            raise serializers.ValidationError({'user': [
                _(f'Пользователь "{user.get_full_name}" не может открыть чат сам собой.')
            ]})
        users = ChatRoom.objects.filter(users__user=user).filter(users__user=to_user)
        if users.exists():
            raise serializers.ValidationError({'user': [
                _(f'Пользователь "{user.get_full_name}" уже имеет совместный чат с "{to_user.get_full_name}".')
            ]})

        room: ChatRoom = super().create(validated_data)

        users = []
        for user_item in [user, to_user]:
            chat_user, created = ChatUser.objects.get_or_create(user=user_item)
            if created:
                chat_user.name = user_item.get_full_name
                chat_user.avatar = user_item.image
                chat_user.save()
            users.append(chat_user)

        room.users.add(*users)
        return room


class UploadFileByMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageChat
        fields = ('photo', 'file')

    def validate(self, attrs):
        photo = attrs.get('photo')
        file = attrs.get('file')

        if not file and not photo:
            raise serializers.ValidationError({'photo': [_('Нужно заполнить один из полей.')]})

        return attrs


class RequestForSupportSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestForSupport
        fields = '__all__'


class ReadRequestForSupportSerializer(serializers.ModelSerializer):
    user = ShortDescUserSerializer()

    class Meta:
        model = RequestForSupport
        fields = '__all__'


class CreateRequestForSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestForSupport
        exclude = ('user', 'status')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.setdefault('user', user)
        return super().create(validated_data)