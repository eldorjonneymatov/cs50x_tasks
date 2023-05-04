import asyncio
import configparser
import pandas as pd
import datetime

from helpers import cyrillic_to_latin, drop_channel_sign
from telethon import TelegramClient, events, sync, types
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import Chat
from telethon.errors.rpcerrorlist import SendCodeUnavailableError, PhoneCodeInvalidError, FloodWaitError, PhoneNumberInvalidError, AuthKeyUnregisteredError


# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
bot_token = config['Telegram']['bot_token']

api_hash = str(api_hash)

CHATS  = ["kunonline", "Daryo", "xushnudbek", "UzReport", "muslimuzportal"]
BEGIN = datetime.datetime(2023, 4, 27, 0, 0, 0)

# Create a new TelegramClient instance with your API credentials
client = TelegramClient('session_nam', api_id, api_hash)

# Connect to the Telegram API
client.start()



async def main():
    DATA = pd.DataFrame({"channel":[], "id":[], "date":[], "text":[], "ad":[]})

    # Iterate through channels
    for CHAT in CHATS:
        # Get the channel entity
        chat = await client.get_entity(CHAT)

        links, dates, texts, ad = [], [], [], []
        # Iterate through messages in the channel
        async for message in client.iter_messages(chat, reverse=True, offset_date=BEGIN):
            if message.text:
                links.append(f"{CHAT}/{message.id}")
                dates.append(message.date)
                texts.append(cyrillic_to_latin(message.text))
        if texts: texts, ad = drop_channel_sign(texts)
        chat_df = pd.DataFrame({'links': links, 'date': dates, 'text': texts, 'ad': ad})
        DATA = pd.concat([DATA, chat_df])
    DATA.to_csv("data.csv", index=False)

async def get_public_channels():
    public_channels = []
    async for dialog in client.iter_dialogs():
        if not dialog.is_group and dialog.is_channel:
            channel = await client.get_entity(dialog.id)
            if channel.username:
                public_channels.append((channel.username, dialog.name))
    return public_channels


async def channel_info(pc):
    await client.connect()
    CHANNELS = {}
    for chat in pc:
        # Get the full channel object using its username
        try:
            entity = await client.get_entity(chat)
            entity = entity[0]
            CHANNELS[chat[0]] = {}
            CHANNELS[chat[0]]["title"] = chat[1]
            CHANNELS[chat[0]]["description"] = entity.about if hasattr(entity, "about") else None
        except AuthKeyUnregisteredError:
            pass
    return CHANNELS


# pc = client.loop.run_until_complete(get_public_channels())
# cs = client.loop.run_until_complete(channel_info(pc))
# for i in cs:
#     print(cs[i]['title'], '\t', cs[i]['description'], '\t')

client.loop.run_until_complete(main())