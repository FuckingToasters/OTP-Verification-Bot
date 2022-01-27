import pymongo
import json
import discord
import os
import sys
import traceback
import asyncio
import datetime
import colorama
import requests
from discord.ext import commands
from discord.ext.commands import MissingPermissions as MP_Error
from discord.ext.commands import MissingRequiredArgument as MRA_Error
from discord_slash import SlashCommand, SlashContext


# setup default config
with open("app.json") as a:
    app = json.load(a)
    url = app["env"]["DATABASE_URL"]["description"]
    token = app["env"]["DISCORDBOT_TOKEN"]["description"]
    database_name = app["env"]["COLLECTION_NAME"]["description"]
    # myclient = pymongo.MongoClient(url, ssl=True, ssl_ca_certs="cacert.pem")
    myclient = pymongo.MongoClient(url, ssl=True)
    mydb = myclient[database_name]
    collection_name = mydb["API Keys"]
    dblist = myclient.list_database_names()
    discordbot = commands.Bot(command_prefix="dont_put_ur_prefix_here", case_insensitive=True, self_bot=False, intents=discord.Intents.all())
    discordbot.remove_command("help")
    slash = SlashCommand(discordbot, sync_commands=True, sync_on_cog_reload=True, debug_guild=903339334017642516)
    watermark = "created by Infinimonster#1312"


# with open("config.json") as conf:
#     config = json.load(conf)
#     requests = cloudscraper.create_scraper()
#     prefix = config.get("Discordbot Prefix")
#     token = config.get("Discordbot Token")
#     watermark = "created by ★MoneyDrop★#2921"
#     discordbot = commands.Bot(command_prefix=prefix, case_insensitive=True, self_bot=False, intents=discord.Intents.all())
#     discordbot.remove_command("help")
#     slash = SlashCommand(discordbot, sync_commands=True, sync_on_cog_reload=True, debug_guild=123456789012345678)

    # logging activities from a Member
    def Log(user, command):
        timestamp = str(datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S'))
        print(f"{colorama.Fore.RESET}"
              f"[{colorama.Fore.GREEN}{timestamp}{colorama.Fore.RESET}] "
              f"USER {colorama.Fore.YELLOW}{str(user)} {colorama.Fore.RESET}USED THE COMMAND {colorama.Fore.YELLOW}{command}")
        with open('[Data]/logs.txt', 'a', encoding='utf-8') as f: f.write(f'[{timestamp}] USER {str(user)} USED THE COMMAND {command}\n')


    # load all cogs in the cogs folder
    if __name__ == '__main__':
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                try:
                    discordbot.load_extension(f"Cogs.{filename[:-3]}")
                    print(f"{colorama.Fore.RED}[>] {colorama.Fore.GREEN}Cogs.{filename[:-3]} loaded")
                except Exception as e:
                    print(f'Failed to load extension {filename}', file=sys.stderr)
                    traceback.print_exc()

        print(f"{colorama.Fore.YELLOW}[>] {colorama.Fore.LIGHTCYAN_EX}Discordbot is ready!")
        discordbot.run(token)
