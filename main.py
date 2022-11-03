import asyncio, os, discord
from twilio.rest import Client

import cogs.config as config
import cogs.strings as strings
import cogs.db as db
import cogs.methods as methods

db.initializeDB()

client = discord.Client()

text_client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)


@client.event
async def on_ready():
    print(strings.LOGGED_IN.format(client.user))


@client.event
async def on_message(message):
    discord_id = str(message.author.id)
    channel_id = str(message.channel.id)

    if message.content == ".sms unsub":
        if db.get_phone_count_for_user(discord_id):
            db.delete_phone(discord_id)
            await message.channel.send(strings.PHONE_REMOVED)
        else:
            await message.channel.send(strings.NO_PHONE_IN_DB)

    elif message.content.startswith(".sms "):
        try:
            phone = message.content.split()[1]
            try:
                int(phone)
            except:
                await message.channel.send(strings.WRONG_PHONE_FORMAT)
                return

            if len(phone) != 11:
                await message.channel.send(strings.WRONG_PHONE_FORMAT)
                return

            if db.get_phone_count_for_user(discord_id):
                await message.channel.send(strings.PHONE_PREVIOUSLY_ADDED)
            else:
                db.insert_phone(discord_id, phone)
                await message.channel.send(strings.PHONE_ADDED)

        except:
            await message.channel.send(strings.WRONG_COMMAND)

    elif db.is_channel_monitored(channel_id):
        role_name = db.get_channel_role(channel_id)
        guild = discord.utils.get(client.guilds, id=config.GUILD_ID)

        try:
            embed = message.embeds[0]
            content = methods.embed_to_text(embed)
        except:
            content = message.content

        content = f"{message.author.name}: \n{content}"
        for row in db.get_all_phone_records():
            discord_id = int(row[0])
            phone = row[1]

            try:
                member = await guild.fetch_member(discord_id)
                if discord.utils.get(member.roles, name=role_name) is not None:

                    message = text_client.messages.create(
                    to= "+" + phone,
                    from_=f"+{config.TWILIO_PHONE}",
                    body=f"{content}")
                    sent = message.sid

            except:
                continue

    try:
        if message.content == ".get_db":
            await message.channel.send(file=discord.File(config.DATABASE_NAME))
    except:
        pass

@client.event
async def on_message_edit(message_before, message_after):
    message = message_after
    discord_id = str(message.author.id)
    channel_id = str(message.channel.id)
    if db.is_channel_monitored(channel_id):
        role_name = db.get_channel_role(channel_id)
        guild = discord.utils.get(client.guilds, id=config.GUILD_ID)

        try:
            embed = message.embeds[0]
            content = methods.embed_to_text(embed)
        except:
            content = message.content

        content = f"{message.author.name}: \n{content}"
        for row in db.get_all_phone_records():
            discord_id = int(row[0])
            phone = row[1]

            try:
                member = await guild.fetch_member(discord_id)
                if discord.utils.get(member.roles, name=role_name) is not None:

                    message = text_client.messages.create(
                    to= "+" + phone,
                    from_=f"+{config.TWILIO_PHONE}",
                    body=f"{content}")
                    sent = message.sid

            except:
                continue


client.run(config.DISCORD_TOKEN)

