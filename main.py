#https://xlsxwriter.readthedocs.io/getting_started.html#getting-started

import discord

import xlsxwriter

from discord.ext import commands

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

#Excel File Setup
workbook = xlsxwriter.Workbook('RegUsers.xlsx')

worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Registered Users')
worksheet.write('C1', 'Points')
worksheet.write('E1', 'Tasks Completed')

workbook.close()

#print online message when bot is running
@bot.event
async def on_ready():
    print("BOT ONLINE")





#Bot commands

#TEST
@bot.command()
async def hello(ctx):
    await ctx.send("Hi!")

#Register user class
def registration(name):
    
    workbook = xlsxwriter.Workbook('RegUsers.xlsx')

    #converts to char for excel writer
    user = ('' + name)
    nameCol = 'A2'
    worksheet.write(nameCol, user)

    workbook.close()

#register user
@bot.command()
async def register(ctx, name):
    users = registration(name)
    await ctx.send("registered " + name)








#print excel file
@bot.command()
async def print(ctx):
    await ctx.send(file = discord.File('RegUsers.xlsx'))






#bot token
bot.run("MTE4MTI2NTc0MDE2NzQwMTU4Mw.GY2-9k.cb4yL9-qtTLj9SHdhtkcT1JVQhSdQoKZAJpGqg")