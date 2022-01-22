from main import commands
from main import requests
from main import discord
from main import watermark
from main import json
from main import Log
from main import colorama
from main import collection_name
from discord_slash import cog_ext


class userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="userinfo", description="Grab infrmations about your 5sim account (only visible to you to avoid leaking private informations)")
    async def userinformation(self, ctx):
        Log(ctx.author, 'userinfo')
        try:
            await ctx.defer(hidden=True)
            result = collection_name.find_one({"_id": ctx.author.id})
            getapi = result.get("API Key")

            headers = {
                "Authorization": "Bearer " + getapi,
                "Content-Type": "application/json",
            }

            response = requests.get("https://5sim.net/v1/user/profile", headers=headers)
            userid = response.json()["id"]
            email = response.json()["email"]
            founds = response.json()["balance"]
            rating = response.json()["rating"]
            default_country_name = response.json()["default_country"]["name"]
            default_country_iso = response.json()["default_country"]["iso"]
            default_country_phone = response.json()["default_country"]["prefix"]

            embed = discord.Embed(title="Userinfo", description="", colour=discord.Colour.green())
            embed.add_field(name="UserID", value=userid)
            embed.add_field(name="E-mail", value=email)
            embed.add_field(name="Founds", value=founds)
            embed.add_field(name="Rating", value=rating)
            embed.add_field(name="Default Country Name", value=default_country_name)
            embed.add_field(name="Default Country iso", value=default_country_iso)
            embed.add_field(name="Default Country Phone-Prefix", value=default_country_phone)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed, hidden=True)

        except AttributeError:
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[401] Unauthorized", value="You cant use any command until you have set your API Key using /setapi")
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed, hidden=True)


def setup(bot):
    bot.add_cog(userinfo(bot))