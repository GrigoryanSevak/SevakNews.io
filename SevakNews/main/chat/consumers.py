import json

from django.shortcuts import render
from django.db.models import Q
from django.http import Http404
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_slug"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]

        if self.user.is_superuser or await self.check_user(room_name=(self.room_name).split('_')[0], user=self.user):
            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )

            # Add the user when the client connects
            await self.add_user(self.room_name, self.user)

            await self.accept()

    async def disconnect(self, close_code):

        # Remove the user when the client disconnects
        # await self.remove_user(self.room_name, self.user)

        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.user
        sender = user.username
        photo = await self.get_icon(user=user)
        room = self.room_name

        if self.user.is_superuser or await self.check_user(room_name=(self.room_name).split('_')[0], user=self.user):
            await self.save_message(room, user, message)

            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender,
                    "photo": photo,
                }
            )
        

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        photo = event["photo"]

        message_html = f"<div hx-swap-oob='beforeend:#messages'><div class='person-a'><img class='icon' src='/media/{photo}' alt='User Photo'><div class='message'><p><b>{sender}:</b> {message}</p></div></div></div>"
        
        await self.send(
            text_data=json.dumps(
                {
                    "message": message_html,
                    "sender": sender,
                },
                ensure_ascii=False,
            )
        )
        
    @sync_to_async
    def get_icon(self, user):
        return user.user_base.photo
        
    @sync_to_async
    def check_user(self, room_name, user):
        return Room.objects.filter(Q(name__iregex=room_name) & Q(users__username=user.username)).exists()

    @sync_to_async
    def save_message(self, room, user, message):
        room = Room.objects.get(slug=room)
        Message.objects.create(room=room, user=user, message=message)

    @sync_to_async
    def add_user(self, room, user):
        room = Room.objects.get(slug=room)
        if user not in room.users.all():
            room.users.add(user)
            room.save()

    @sync_to_async
    def remove_user(self, room, user):
        room = Room.objects.get(slug=room)
        if user in room.users.all():
            room.users.remove(user)
            room.save()
            
            