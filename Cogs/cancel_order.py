import discord
from main import commands
from main import MP_Error
from main import MRA_Error
from main import watermark
from main import requests
from main import Log
from main import colorama
from main import collection_name
from discord_slash import cog_ext

# This is useful, if you want to cancel an order that you have placed
class cancel_activation_number(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="cancelorder", description="cancel a ordered number (useful if no sms is being sent & refound your founds)")
    async def cancel_order(self, ctx, order_id):
        Log(ctx.author, 'cancelorder')
        try:
            await ctx.defer(hidden=True)
            result = collection_name.find_one({"_id": ctx.author.id})
            getapi = result.get("API Key")

            headers = {
                "Authorization": "Bearer " + getapi,
                "Content-Type": "application/json",
            }

            cancel_response = requests.get(f"https://5sim.net/v1/user/cancel/{order_id}", headers=headers)
            if cancel_response.status_code == 200:
                embed = discord.Embed(title="Successfully", description="", colour=discord.Colour.green())
                embed.add_field(name="[200] Order Status", value="The Order has been **canceled** successfully!")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

            elif cancel_response.status_code == 400:
                embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
                embed.add_field(name="[400] Invalid Argument", value="The Argument `Order ID` is not correct.\n Please check your Order ID and try it again!")
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

    @cancel_order.error
    async def cancel_error(self, ctx, error):
        if isinstance(error, MP_Error):
            pass

        elif isinstance(error, MRA_Error):
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[400] Missing Argument", value="`Order ID` is a required Argument that is Missing!")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed, hidden=True)


def setup(bot):
    bot.add_cog(cancel_activation_number(bot))