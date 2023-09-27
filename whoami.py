import os
from pyrogram import Client
import dotenv

dotenv.load_dotenv()

api_id = os.getenv('TOKEN')
api_hash = os.getenv('API_HASH')


with Client('dhivehishop', api_id, api_hash) as app:
    # Send a message to @fauzaanu
    app.send_message('me', 'Hello, me! I can use @jsondumpbot to get my channel id by forwarding a message to it.')
