from pyrogram import Client
from pyrogram.raw.functions.contacts import ResolveUsername
from config_reader import config

BOT_TOKEN = config.bot_token.get_secret_value()

pyrogram_client = Client(
    "bot",
    api_id=25898752,
    api_hash="c59005f7b14ecd36300b71fdccc9b861",
    bot_token=BOT_TOKEN
)


def resolve_username_to_user_id(username: str):
    with pyrogram_client:
        r = pyrogram_client.invoke(ResolveUsername(username=username))
        if r.users:
            return r.users[0].id
        return None


print(resolve_username_to_user_id("Lime2mc"))