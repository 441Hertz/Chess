import discord, os, logging
from dotenv import load_dotenv
from discord.ext import commands


def logs():
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename = 'p1\discord.log', encoding = 'utf-8', mode = 'w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

logs()