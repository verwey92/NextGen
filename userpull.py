import discord
import os
from discord.ext import commands
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN") # Replace this with your bot token
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def usermessages(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Please specify a user!")
        return
    
    #Inform the user that the command is processing
    await ctx.send("Retreiving user message count within the server for the last 30 days.")

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=30)
    counter = 0

    # Iterate over the channels to count messages
    for channel in ctx.guild.text_channels:
        try:
            # Filter messages by the user and the date range
            async for message in channel.history(limit=None, after=start_time, before=end_time):
                if message.author == member:
                    counter += 1
        except discord.Forbidden:
            continue  # Ignore channels the bot doesn't have access to

    await ctx.send(f"{member.mention} has sent {counter} messages in the last 30 days!")

bot.run(TOKEN)
