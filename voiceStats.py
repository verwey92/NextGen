import discord
import os
from discord.ext import commands
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN") # Replace this with your bot token

bot = commands.Bot(command_prefix='!', intents=intents)

# Voice state data will be stored in this dictionary
voice_data = {}  # Structure: {channel_id: {user_id: { 'join_time': datetime, 'total_time': timedelta}}}

@bot.event
async def on_voice_state_update(member, before, after):
    user_id = member.id
    now = datetime.now()

    # User joined a voice channel
    if before.channel is None and after.channel is not None:
        channel_id = after.channel.id
        if channel_id not in voice_data:
            voice_data[channel_id] = {}
        if user_id not in voice_data[channel_id]:
            voice_data[channel_id][user_id] = {'join_time': now, 'total_time': timedelta(0)}
        else:
            voice_data[channel_id][user_id]['join_time'] = now

    # User left a voice channel
    elif before.channel is not None and after.channel is None:
        channel_id = before.channel.id
        if channel_id not in voice_data or user_id not in voice_data[channel_id]:
            # Channel or user data is not available, skip further processing for this event
            return
        if 'join_time' in voice_data[channel_id][user_id]:
            join_time = voice_data[channel_id][user_id]['join_time']
            duration = now - join_time
            voice_data[channel_id][user_id]['total_time'] += duration
            del voice_data[channel_id][user_id]['join_time']

@bot.command()
async def hello(ctx):
    await ctx.send("Hello World")

@bot.command()
async def voice_stats(ctx):
    report = []

    for channel_id, users in voice_data.items():
        total_users = 0
        total_duration = timedelta(0)

        for user_data in users.values():
            if 'join_time' in user_data:
                duration = datetime.now() - user_data['join_time']
                user_data['total_time'] += duration
                del user_data['join_time']

            if user_data['total_time'] > timedelta(0):
                total_users += 1
                total_duration += user_data['total_time']

        if total_users == 0:
            average_duration = timedelta(0)
        if not report:
            await ctx.send("No voice activity data to report.")
        else:
            average_duration = total_duration // total_users

        hh, remainder = divmod(average_duration.seconds, 3600)
        mm, ss = divmod(remainder, 60)
        channel_name = bot.get_channel(channel_id).name
        report.append(f"Channel {channel_name} - Total users: {total_users}, Average duration: {hh:02}:{mm:02}:{ss:02}")

    await ctx.send("\n".join(report))

bot.run(TOKEN)
