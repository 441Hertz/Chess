import discord, os, logging
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def logs():
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

# logs()

bot = commands.Bot(command_prefix = '!')

extensions = ['cogs.CommandEvents']
for ext in extensions:
    bot.load_extension(ext)
        
bot.run(TOKEN)

