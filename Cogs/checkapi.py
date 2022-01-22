from main import commands
from main import requests
from main import json
from main import discord
from main import discordbot
from main import watermark
from main import Log
from main import collection_name
from discord_slash import cog_ext

# This will check the uptime of the API and return the result
class checkapi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="checkapi", description="check if a request to 5sim is successful")
    async def check_api_status(self, ctx):
        Log(ctx.author, 'checkapi')
        await ctx.defer(hidden=True)

        try:
            result = collection_name.find_one({"_id": ctx.author.id})
            getapi = result.get("API Key")

            headers = {
                "Authorization": "Bearer " + getapi,
                "Content-Type": "application/json",
            }
            response = requests.get("https://5sim.net/v1/user/profile", headers=headers)
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())

            if response.status_code == 200:
                embed = discord.Embed(title="Successfully", description="", colour=discord.Colour.green())
                embed.add_field(name="[200] Request Successful", value="No issuers with requests to the API detected!")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

            if response.status_code == 401:
                embed.add_field(name="[404] Not found", value="Couldn't find a API Key bound to your Account. Please use /setapi fist!")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

            if response.status_code == 429:
                embed.add_field(name="[429] Unauthorized", value="You are being rate limited => wait minimum 5 seconds!")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

        except AttributeError:
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[401] Unauthorized", value="You cant use any command until you have set your API Key using /setapi")
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed, hidden=True)

        except Exception:
            raise Exception

def setup(bot):
    bot.add_cog(checkapi(bot))