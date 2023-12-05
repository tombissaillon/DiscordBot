#TO DO
    #Current Errors: why file will not update when information is added.
    #Need to work on command to add points to users when task completed.
    #Need to keep stamps and logs of what task and when completed.
    #Greeting Message?

#DONE
    #list of commands
    #Change bot commands to also accept / when inputted into chat, and to be seen when entering commands
    #Rename bot biography


#LIBRARY IMPORTS **IMPORTANT INFORMATION TO COMMITING TO CODE**
    #https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst
    #https://stackoverflow.com/questions/44951456/pip-error-microsoft-visual-c-14-0-is-required
    #cmd command: pip install discord.py

    #https://xlsxwriter.readthedocs.io/getting_started.html#getting-started

import discord

import xlsxwriter

from discord.ext import commands

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix= ["!","/"], intents=intents)

#On bot start
@bot.event
async def on_ready():
    #print online message to terminal when bot is running
    print("BOT ONLINE")

    #Displays bot status
    await bot.change_presence(activity=discord.Game(name="Type /commands_help for help"))

    global workbook
    workbook = xlsxwriter.Workbook('RegUsers.xlsx')
    global worksheet 
    worksheet = workbook.add_worksheet()
    
    #Setting up workbook
    worksheet.write('A1', 'Registered Users')
    worksheet.write('C1', 'Points')
    worksheet.write('E1', 'Tasks Completed')

#On bot end
#@bot.event
#async def on_close():
    #workbook.close()


#BOT COMMAND LIST
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









#Print commands to user
@bot.command()
async def commands_help(ctx):
    await ctx.send("!commands_help")
    await ctx.send("uploads list of commands to server chat")
    await ctx.send("!register (user name)")
    await ctx.send("registers user name to excel file to keep track of points")
    await ctx.send("!print")
    await ctx.send("prints excel file to view users, points, tasks with timestamps")

#print excel file
@bot.command()
async def print(ctx):
    await ctx.send(file = discord.File('RegUsers.xlsx'))

#bot token
bot.run("MTE4MTI2NTc0MDE2NzQwMTU4Mw.GHos_s.xCNY821leZNf_shp-AMeCs6UTEYD18aFdg1ETg")