#TO DO
    #EXCEL FILE LOGIC FOR POINTS
    #TIME LOG OF WHEN TASKS ARE COMPLETED
    #Need to work on command to add points to users when task completed.
    #Need to keep stamps and logs of what task and when completed.
    #Greeting Message?
    #change starting points to one when registered
    #create .txt file to send with commands

#DONE
    #list of commands
    #Change bot commands to also accept / when inputted into chat, and to be seen when entering commands
    #Rename bot biography
    #Create event command?
    #Current Errors: why file will not update when information is added.
    #add points command


#LIBRARY IMPORTS **IMPORTANT INFORMATION TO COMMITING TO CODE**
    #https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst
    #https://stackoverflow.com/questions/44951456/pip-error-microsoft-visual-c-14-0-is-required
    #cmd command: pip install discord.py

    #https://xlsxwriter.readthedocs.io/getting_started.html#getting-started

import discord
import xlsxwriter
import datetime
import random

from discord.ext import commands

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix= ["!","/"], intents = intents)

currentTime = datetime.datetime.now()
registered_users = {}
eventName = ""

#On bot start
@bot.event
async def on_ready():
    #print online message to terminal when bot is running
    print("BOT ONLINE")

    #Displays bot status
    await bot.change_presence(activity=discord.Game(name="Type /commands_help for help!"))

#Print commands to user
@bot.command()
async def commands_help(ctx):
    await ctx.send("!commands_help")
    await ctx.send("uploads list of commands to server chat")
    await ctx.send("!register (user name)")
    await ctx.send("registers user name to excel file to keep track of points")
    await ctx.send("!print")
    await ctx.send("prints excel file to view users, points, tasks with timestamps")

@bot.command()
async def createEvent(ctx, name):
    global eventName
    eventName = name
    await ctx.send("Event " + eventName + " created.")

@bot.command()
async def event(ctx):
    await ctx.send(eventName + " event.")

@bot.command()
async def register(ctx, member: discord.Member):
    user_id = str(member.id)
    if user_id not in registered_users:
        registered_users[user_id] = {"points": 0, "tasks_completed": 0}
        await ctx.send(f"Registered {member.display_name}")
    else:
        await ctx.send(f"{member.display_name} is already registered.")

@bot.command()
async def user_info(ctx, member: discord.Member):
    user_id = str(member.id)
    if user_id in registered_users:
        info = registered_users[user_id]
        await ctx.send(f"{member.display_name} has {info['points']} points and has completed {info['tasks_completed']} tasks.")
    else:
        await ctx.send(f"{member.display_name} is not registered.")

@bot.command()
async def add_points(ctx, user: discord.Member, points: int):
    global registered_users

    # Check if the user is registered
    if str(user.id) not in registered_users:
        await ctx.send(f"{user.display_name} is not registered.")
        return

    # Add points to the user
    registered_users[str(user.id)]['points'] += points

    await ctx.send(f"Added {points} points to {user.display_name}. They now have {registered_users[str(user.id)]['points']} points.")









#print excel file
@bot.command()
async def print(ctx):
    workbook = xlsxwriter.Workbook('RegUsers.xlsx')
    worksheet = workbook.add_worksheet()

    #Setting up workbook
    worksheet.write('A1', 'Registered Users')
    worksheet.write('C1', 'Points')
    worksheet.write('E1', 'Tasks Completed')

    #Start from row 2 to write user data
    row = 1
    for user, info in registered_users.items():
        #Write user name to column A
        worksheet.write(row, 0, user)
        #Write points to column C
        worksheet.write(row, 2, info['points'])
        #Write tasks completed to column E
        worksheet.write(row, 4, info['tasks_completed'])
        row += 1

    workbook.close()
    await ctx.send(file=discord.File('RegUsers.xlsx'))

@bot.command()
async def select_winner(ctx):
    global registered_users

    # Check if there are registered users
    if not registered_users:
        await ctx.send("No registered users.")
        return

    # Calculate the probability based on points
    total_points = sum(info['points'] for info in registered_users.values())
    probabilities = [info['points'] / total_points for info in registered_users.values()]

    # Select a winner based on probabilities
    winner_id = random.choices(list(registered_users.keys()), weights=probabilities, k=1)[0]
    winner_member = await ctx.guild.fetch_member(int(winner_id))

    await ctx.send(f"@everyone, the winner of event " + eventName + " is: {winner_member.display_name}")

#bot token
bot.run("MTE4MTI2NTc0MDE2NzQwMTU4Mw.GYptH9.V9UEPdWiM6AVb91hd-9tqw-LFLPGexrxO4iqE0")