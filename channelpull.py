import discord 
import os
from discord.ext import commands, tasks
import datetime

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN") # Replace this with your bot token
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='channel_messages')
async def fetch_messages(ctx, channel_name: str):
    await ctx.send(f"Fetching message counts for #{channel_name}... This may take a while.")
    
    target_channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)

    # If the channel doesn't exist
    if not target_channel:
        await ctx.send(f"No channel named #{channel_name} found.")
        return

    thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    
    try:
        unique_users = set()
        message_count = 0

        async for message in target_channel.history(after=thirty_days_ago, limit=None):
            message_count += 1
            unique_users.add(message.author.id)


        output = f"Message and user counts for #{channel_name} in the last 30 days:\n"
        output += f"{message_count} messages from {len(unique_users)} unique users."
        await ctx.send(output)

    except discord.Forbidden:
        await ctx.send(f"Permission denied for #{channel_name}.")

bot.run(TOKEN)