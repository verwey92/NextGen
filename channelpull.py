import datetime

import discord
from discord.ext import commands


class ChannelPull(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def channel_messages(self, ctx, channel_name: str):
        await ctx.send(
            f"Fetching message counts for #{channel_name}... This may take a while."
        )

        target_channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)

        # If the channel doesn't exist
        if not target_channel:
            await ctx.send(f"No channel named #{channel_name} found.")
            return

        thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)

        try:
            unique_users = set()
            message_count = 0

            async for message in target_channel.history(
                after=thirty_days_ago, limit=None
            ):
                message_count += 1
                unique_users.add(message.author.id)

            output = (
                f"Message and user counts for #{channel_name} in the last 30 days:\n"
            )
            output += f"{message_count} messages from {len(unique_users)} unique users."
            await ctx.send(output)

        except discord.Forbidden:
            await ctx.send(f"Permission denied for #{channel_name}.")
