#Invite link: https://discord.com/api/oauth2/authorize?client_id=1181265740167401583&permissions=8&scope=bot
#Token: MTE4MTI2NTc0MDE2NzQwMTU4Mw.GHsZaZ.qMRHobE4CFisQpsgklBue5tjdiYFHvZmFkqK0o


#https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst
#https://stackoverflow.com/questions/44951456/pip-error-microsoft-visual-c-14-0-is-required
#cmd command: pip install discord.py

import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.event
async def on_ready():
    print("BOT ONLINE")

@bot.command()
async def hello(ctx):
    await ctx.send("Hi!")

bot.run("MTE4MTI2NTc0MDE2NzQwMTU4Mw.GHsZaZ.qMRHobE4CFisQpsgklBue5tjdiYFHvZmFkqK0o")