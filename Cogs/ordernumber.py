import random
from main import commands
from main import requests
from main import json
from main import discord
from main import watermark
from main import discordbot
from main import MP_Error
from main import MRA_Error
from main import asyncio
from main import datetime
from main import colorama
from main import collection_name
from main import Log
from discord_slash import cog_ext

# Class related to Orders with 2 Commands including: buy, check
class order_activation_number(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Order a Temp-Number from the API and return it in an Embed-Message
    @cog_ext.cog_slash(name="buynumber", description="Order a phonenumber (useful to verify different types of Accounts)")
    async def buy_activation_number(self, ctx, service, country, operator):
        Log(ctx.author, 'buynumber')
        try:
            await ctx.defer(hidden=True)

            result = collection_name.find_one({"_id": ctx.author.id})
            getapi = result.get("API Key")

            headers = {
                "Authorization": "Bearer " + getapi,
                "Content-Type": "application/json",
            }

            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            response = requests.get(f"https://5sim.net/v1/user/buy/activation/{country}/{operator}/{service}", headers=headers)
            activation_id = response.json()["id"]
            activation_phone = response.json()["phone"]
            activation_operator = response.json()["operator"]
            activation_price = response.json()["price"]
            activation_status = response.json()["status"]
            activation_expires = response.json()["expires"]
            activation_sms = response.json()["sms"]
            activation_country = response.json()["country"]

            if response.status_code == 200:
                print(f"Buy Number: {response.json()}")
                embed = discord.Embed(title="Successfully", description="", colour=discord.Colour.green())
                embed.add_field(name="Order ID", value=activation_id)
                embed.add_field(name="Bought Number", value=activation_phone)
                embed.add_field(name="Operator", value=activation_operator)
                embed.add_field(name="Status", value=activation_status)
                embed.add_field(name="Expires", value=activation_expires)
                embed.add_field(name="Price", value=activation_price)
                embed.add_field(name="SMS", value=activation_sms)
                embed.add_field(name="Country", value=activation_country)
                embed.add_field(name="Timeout", value=f"You now can verify your Discordaccount using `{activation_phone}` and i will send updates within 60 Seconds.")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)


            if response.status_code == 401:
                embed.add_field(name="[401] Unauthorized", value="Invalid API Key detected => update your API Key please!")
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

            if response.status_code == 429:
                embed.add_field(name="[429] Unauthorized", value="You are being rate limited => wait minimum 5 seconds!")
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)


        except AttributeError:
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[401] Unauthorized", value="You cant use any command until you have set your API Key using /setapi")
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed, hidden=True)

        except Exception: raise Exception

    @buy_activation_number.error
    async def buynumber_error(self, ctx, error):
        if isinstance(error, MP_Error):
            pass

        elif isinstance(error, MRA_Error):
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[400] Missing Argument", value="`Country` is a required Argument that is Missing!")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed)

    # Check if the otp verification code is sent and if it is sent it returns the code
    @cog_ext.cog_slash(name="checkorder", description="checks a ordered number (useful to see the status of the orderd number & get the sms code)")
    async def check_activation_number(self, ctx, order_id):
        Log(ctx.author, 'checkorder')
        try:
            await ctx.defer(hidden=True)

            result = api_keys_collection.find_one({"_id": ctx.author.id})
            getapi = result.get("API Key")

            headers = {
                "Authorization": "Bearer " + getapi,
                "Content-Type": "application/json",
            }


            check_response = requests.get(f"https://5sim.net/v1/user/check/{order_id}", headers=headers)
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())

            if check_response.status_code == 200:
                check_phone = check_response.json()["phone"]
                check_operator = check_response.json()["operator"]
                check_product = check_response.json()["product"]
                check_status = check_response.json()["status"]
                check_country = check_response.json()["country"]

                if check_status == "PENDING":
                    embed = discord.Embed(title="[Pending] | Information", description="", colour=discord.Colour.yellow())
                    embed.add_field(name="Phone Number", value=check_phone)
                    embed.add_field(name="Network Operator", value=check_operator)
                    embed.add_field(name="Product", value=check_product)
                    embed.add_field(name="Status", value=check_status)
                    embed.add_field(name="Country", value=check_country)
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text=watermark)
                    await ctx.send(embed=embed, hidden=True)

                if check_status == "RECEIVED":
                    check_sms_sender = check_response.json()["sms"][0]["sender"]
                    check_sms_text = check_response.json()["sms"][0]["text"]
                    check_sms_code = check_response.json()["sms"][0]["code"]
                    embed = discord.Embed(title="Successfully", description="", colour=discord.Colour.green())
                    embed.add_field(name="Phone Number", value=check_phone)
                    embed.add_field(name="Network Operator", value=check_operator)
                    embed.add_field(name="Product", value=check_product)
                    embed.add_field(name="Status", value=check_status)
                    embed.add_field(name="Country", value=check_country)
                    embed.add_field(name="SMS Sender", value=check_sms_sender)
                    embed.add_field(name="SMS Text", value=check_sms_text)
                    embed.add_field(name="SMS Code", value=check_sms_code)
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text=watermark)
                    await ctx.send(embed=embed, hidden=True)

                if check_status == "FINISHED":
                    embed.add_field(name="Phone Number", value=check_phone)
                    embed.add_field(name="Network Operator", value=check_operator)
                    embed.add_field(name="Product", value=check_product)
                    embed.add_field(name="Status", value=check_status)
                    embed.add_field(name="Country", value=check_country)
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text=watermark)
                    await ctx.send(embed=embed, hidden=True)

                if check_status == "TIMEOUT":
                    embed = discord.Embed(title="[Timeout] | Information", description="", colour=discord.Colour.yellow())
                    embed.add_field(name="Phone Number", value=check_phone)
                    embed.add_field(name="Network Operator", value=check_operator)
                    embed.add_field(name="Product", value=check_product)
                    embed.add_field(name="Status", value=check_status)
                    embed.add_field(name="Country", value=check_country)
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text=watermark)
                    await ctx.send(embed=embed, hidden=True)

                if check_status == "CANCELED":
                    embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
                    embed.add_field(name="[404] Order Status", value="Order has been Canceled!")
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text=watermark)
                    await ctx.send(embed=embed, hidden=True)

                if check_status == "BANNED":
                    embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
                    embed.add_field(name="[404] Order Status", value="Order has been Banned!")
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text=watermark)
                    await ctx.send(embed=embed, hidden=True)


            if check_response.status_code == 401:
                embed.add_field(name="[401] Unauthorized", value="Invalid API Key detected => update your API Key please!")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

            if check_response.status_code == 429:
                embed.add_field(name="[429] Unauthorized", value="You are being rate limited => wait minimum 5 seconds!")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)


        except AttributeError:
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[401] Unauthorized", value="You cant use any command until you have set your API Key using /setapi")
            embed.set_footer(text=watermark)
            await ctx.send( embed=embed, hidden=True)

        except Exception:
            raise Exception

    @check_activation_number.error
    async def checknumber_error(self, ctx, error):
        if isinstance(error, MRA_Error):
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[400] Missing Argument", value="`Order ID` is a required Argument that is Missing!")
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed, hidden=True)

def setup(bot):
    bot.add_cog(order_activation_number(bot))