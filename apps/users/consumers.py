import json

from channels import Channel, Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.sessions import channel_session
from django.core.cache import cache


def msg_consumer(message):
    # Save to model
    room = message['room']

    # Broadcast to listening sockets
    Group("chat-%s" % room).send({
        "text": message['message'],
    })


@channel_session_user_from_http
def users_ws_connect(message):
    # Work out room name from path (ignore slashes)
    print(message.content)
    room = message.content['query_string'].strip("room=").strip("/")
    print(room)
    # Save room in session and add us to the group
    message.channel_session['room'] = room
    Group("chat-%s" % room).add(message.reply_channel)

    if not message.user.is_anonymous():

        Group('users').add(message.reply_channel)
        Group('users').send({
            'text': json.dumps({
                'username': message.user.username,
                'full_name': message.user.get_full_name(),
                'is_logged_in': True
            })
        })


@channel_session
def users_ws_message(message):
    # Stick the message onto the processing queue
    Channel("chat-messages").send({
        "room": message.channel_session['room'],
        "message": message['text'],
    })


@channel_session_user
def users_ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)

    if not message.user.is_anonymous():

        Group('users').send({
            'text': json.dumps({
                'username': message.user.username,
                'full_name': message.user.get_full_name(),
                'is_logged_in': False
            })
        })
        Group('users').discard(message.reply_channel)


def ws_add(message):
    # Accept the incoming connection

    message.reply_channel.send({"accept": True})
    # Add them to the chat group

    Group("chat").add(message.reply_channel)
    # Connected to websocket.disconnect


def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)


def ws_message(message):

    print(f"ws_message: {message.channel}, {message.content}")

    ws_messages = cache.get("ws_messages")

    if not ws_messages:
        ws_messages = list()

    ws_messages.append(message.content['text'])

    cache.set("ws_messages", ws_messages)

    Group("chat").send({
        "text": message.content['text']
    })