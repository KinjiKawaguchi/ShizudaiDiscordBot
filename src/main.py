import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
client = discord.Bot()

bot = commands.Bot(command_prefix="/",intents=intents,client=client)

TOKEN = os.environ.get('TOKEN')