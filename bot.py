import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from channelpull import ChannelPull
from pugquiz import PugQuiz
from userpull import UserPull
from voiceStats import VoiceStats

load_dotenv()

TOKEN = os.getenv("TOKEN")  # Replace this with your bot token

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(VoiceStats(bot))
    await bot.add_cog(UserPull(bot))
    await bot.add_cog(ChannelPull(bot))
    await bot.add_cog(PugQuiz(bot))
    print(f"We have logged in as {bot.user}")


bot.run(TOKEN)
