from datetime import datetime, timedelta

import discord
from discord.ext import commands


class UserPull(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def user_messages(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Please specify a user!")
            return

        # Inform the user that the command is processing
        await ctx.send(
            "Retreiving user message count within the server for the last 30 days."
        )

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=30)
        counter = 0

        # Iterate over the channels to count messages
        for channel in ctx.guild.text_channels:
            try:
                # Filter messages by the user and the date range
                async for message in channel.history(
                    limit=None, after=start_time, before=end_time
                ):
                    if message.author == member:
                        counter += 1
            except discord.Forbidden:
                continue  # Ignore channels the bot doesn't have access to

        await ctx.send(
            f"{member.mention} has sent {counter} messages in the last 30 days!"
        )
