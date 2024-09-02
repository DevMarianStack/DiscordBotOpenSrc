import discord
from discord.ext import commands
from utils import permissions, default
from utils.data import DiscordBot

class HelpFormat(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
    
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", description="Here are all the available commands categorized.", color=discord.Color.blue())

        for cog, commands in mapping.items():
            if cog is None:
                continue

            cog_name = cog.qualified_name if cog else "No Category"
            command_list = [f"`{command.name}`: {command.short_doc or 'No description'}" for command in commands]

            if command_list:
                embed.add_field(name=cog_name, value="\n".join(command_list), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Help for `{command.name}`", description=command.help or "No description", color=discord.Color.green())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        commands = [f"`{command.name}`: {command.short_doc or 'No description'}" for command in cog.get_commands()]
        embed = discord.Embed(title=f"Help for `{cog.qualified_name}`", description="\n".join(commands), color=discord.Color.orange())
        await self.get_destination().send(embed=embed)

async def setup(bot: DiscordBot):
    bot.help_command = HelpFormat()
    await bot.add_cog(Events(bot))  # Ensure `Events` cog is defined and imported correctly