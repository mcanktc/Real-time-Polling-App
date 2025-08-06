from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Vote, Option, Poll
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError

class PollConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.poll_id = self.scope["url_route"]["kwargs"]["poll_id"]
        self.group_name = f"poll_{self.poll_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):

        data = json.loads(text_data)
        poll_id = data.get("poll_id")
        option_id = data.get("option_id")

        user = self.scope["user"]

        if isinstance(user, AnonymousUser):
            await self.send(text_data=json.dumps({"error" : "Log In please!"}))
            return
        
        try:
            poll = await Poll.objects.aget(pk=poll_id)
            option = await Option.objects.aget(pk=option_id)

            await Vote.objects.acreate(user=user, poll=poll, option=option)

        except:
            await self.send(text_data=json.dumps({"error" : "You already voted."}))
            return
        
        votes_for_option = await Vote.objects.filter(option=option).acount()

        total_votes = await Vote.objects.filter(poll=poll).acount()

        await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "poll_update",
                    "message": {
                        "poll_id": poll.id,
                        "option_id": option.id,
                        "option_title": option.title,
                        "votes_for_option": votes_for_option,
                        "total_votes": total_votes,
                        "voted_by": user.username,
                    }
                }
        )

    
    async def poll_update(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )


