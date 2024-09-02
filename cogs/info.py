import time
import discord
import psutil
import os

from utils.default import CustomContext
from discord.ext import commands
from utils import default, http
from utils.data import DiscordBot


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx: CustomContext):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        msg = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await msg.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command(aliases=["joinme", "join", "botinvite"])
    async def invite(self, ctx: CustomContext):
        """ Invite me to your server """
        await ctx.send("\n".join([
            f"**{ctx.author.name}**, use this URL to invite me",
            f"<{discord.utils.oauth_url(self.bot.user.id)}>"
        ]))

    @commands.command()
    async def source(self, ctx: CustomContext):
        """ Check out my source code <3 """
        # Do not remove this command, this has to stay due to the GitHub LICENSE.
        # TL:DR, you have to disclose source according to MIT, don't change output either.
        # Reference: https://github.com/DevMarianStack/DiscordBotOpenSrc
        await ctx.send("\n".join([
            f"**{ctx.bot.user}** is powered by this source code:",
            "https://github.com/DevMarianStack/DiscordBotOpenSrc"
        ]))

    @commands.command(aliases=["supportserver", "feedbackserver"])
    async def botserver(self, ctx: CustomContext):
        """ Get an invite to our support server! """
        if isinstance(ctx.channel, discord.DMChannel) or ctx.guild.id != 1279924650125819995:
            return await ctx.send(f"**Here you go {ctx.author.name} 🍻**\nhttps://discord.gg/FdNkRqXWjD")
        await ctx.send(f"**{ctx.author.name}** this is my home you know :3")

    @commands.command()
    async def covid(self, ctx: CustomContext, *, country: str):
        """Covid-19 Statistics for any countries"""
        async with ctx.channel.typing():
            r = await http.get(f"https://disease.sh/v3/covid-19/countries/{country.lower()}", res_method="json")

            if "message" in r.response:
                return await ctx.send(f"The API returned an error:\n{r['message']}")

            r = r.response

            json_data = [
                ("Total Cases", r["cases"]), ("Total Deaths", r["deaths"]),
                ("Total Recover", r["recovered"]), ("Total Active Cases", r["active"]),
                ("Total Critical Condition", r["critical"]), ("New Cases Today", r["todayCases"]),
                ("New Deaths Today", r["todayDeaths"]), ("New Recovery Today", r["todayRecovered"])
            ]

            embed = discord.Embed(
                description=(
                    "The information provided was last "
                    f"updated <t:{int(r['updated'] / 1000)}:R>"
                )
            )

            for name, value in json_data:
                embed.add_field(
                    name=name,
                    value=f"{value:,}" if isinstance(value, int) else value
                )

            await ctx.send(
                f"**COVID-19** statistics in :flag_{r['countryInfo']['iso2'].lower()}: "
                f"**{country.capitalize()}** *({r['countryInfo']['iso3']})*",
                embed=embed
            )

    @commands.command(aliases=["info", "stats", "status"])
    async def about(self, ctx: CustomContext):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embedColour = None
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=ctx.bot.user.avatar)
        embed.add_field(
            name="Last boot",
            value=default.date(self.bot.uptime, ago=True)
        )
        embed.add_field(
            name="Developer",
            value=str(self.bot.get_user(
                self.bot.config.discord_owner_id
            ))
        )
        embed.add_field(name="Library", value="discord.py")
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )")
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]))
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB")

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)


async def setup(bot):
    await bot.add_cog(Information(bot))