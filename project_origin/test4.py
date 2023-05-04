import asyncio
import configparser
import pandas as pd
import datetime
import os

from helpers import cyrillic_to_latin, drop_channel_sign
from telethon import TelegramClient, events, sync, types

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

CHATS  = ["kunonline", "Daryo", "xushnudbek", "UzReport", "muslimuzportal"]
BEGIN = datetime.datetime(2023, 4, 27, 0, 0, 0)

# Create a new TelegramClient instance with your API credentials
client = TelegramClient('session_n43', api_id, api_hash)
session_name = 'session_n43.session'
print(os.path.exists(session_name))
# Connect to the Telegram API
client.connect()
loop = asyncio.get_event_loop()
# def main():
#     asyncio.run(send_code_request('+998997743910'))

# async def send_code_request(phone):
#     await client.send_code_request(phone)


async def sign_in(phone):
    code = input('code: ')
    await client.sign_in(phone, code)

async def send_code_request(phone):
    # Send the code request and wait for the response
    result = await client.send_code_request(phone)

def main():
    # Phone number to send code request to
    phone = '+998997743910'

    # Send the code request
    loop.run_until_complete(send_code_request(phone))
    loop.run_until_complete(sign_in(phone))

# Run the main coroutine
main()