from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, PairStatusEv, event
from neonize.types import MessageServerID
from datetime import timedelta

client = NewClient("your_database_file.sqlite3")


@client.event(ConnectedEv)
def on_connected(_: NewClient, __: ConnectedEv):
    print("⚡ Connected")


@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):
    handler(client, message)

# Define your custom message handler function


def handler(client: NewClient, message: MessageEv):
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat

    # Example scenarios
    if text == "ping":
        client.reply_message(chat, "pong", message)
    elif text == "_sticker":
        client.send_sticker(chat, "sticker_url_here")


# Connect to WhatsApp
client.connect()
