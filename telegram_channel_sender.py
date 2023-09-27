import os
import random
from pyrogram import Client
import dotenv

dotenv.load_dotenv()

api_id = os.getenv('TOKEN')
api_hash = os.getenv('API_HASH')
client = Client('dhivehishop', api_id, api_hash)
channel_id = -1001694454904  # dhivehishop
staging = -1001948761631  # staging
messages_que = []

async def main(formatted_msg):
    """
    Sends the formatted message to the channel
    """

    # Comment on Production
    channel_id = staging

    random_pic_id = random.randint(1, 5)
    await client.send_photo(channel_id,
                            photo=f"Images/{random_pic_id}.png",
                            caption=f"{formatted_msg}\n@gedhoru - Share / [Boost](https://t.me/gedhoru?boost)"
                            )


def send_update(formatted_msg, end=False, no_que=False):
    """
    The loop in pyrogram
    """
    with client:
        client.run(main(formatted_msg, end=end, no_que=no_que))
