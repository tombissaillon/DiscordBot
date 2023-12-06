#TO DO
    
#DONE
    #list of commands
    #Change bot commands to also accept / when inputted into chat, and to be seen when entering commands
    #Rename bot biography
    #Create event command?
    #Current Errors: why file will not update when information is added.
    #add points command
    #Greeting Message
    #change starting points to one when registered
    #TIME LOG OF WHEN TASKS ARE COMPLETED
    #Need to keep stamps and logs of what task and when completed.
    #create .txt file to send with commands
    #fix username when winner is selected
    #Excel logic for tasks


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
global points

#On bot start
@bot.event
async def on_ready():
    #print online message to terminal when bot is running
    print("BOT ONLINE")

    #Displays bot status
    await bot.change_presence(activity=discord.Game(name="Type /commands_help for help!"))

@bot.event
async def on_guild_join(guild):
    # This function will be called when the bot joins a new server
    general_channel = discord.utils.get(guild.text_channels, name = "general")
    
    if general_channel:
        # Send a welcome message to the general channel
        await general_channel.send("Hello, I'm your friendly bot! Type !commands_help to see a list of commands.")
    else:
        # If there is no 'general' channel, send a message to the first available text channel
        first_text_channel = guild.text_channels[0]
        await first_text_channel.send("Hello, I'm your friendly bot! Type !commands_help to see a list of commands.")

#Print commands to user
@bot.command()
async def commands_help(ctx):
    await ctx.send(file=discord.File('Commands_for_Discord_Reward_Bot.txt'))

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
    global user_id
    
    user_id = str(member.id)

    if user_id not in registered_users:
        registered_users[user_id] = {"points": 0, "tasks_completed": 0}
        await ctx.send(f"Registered {member.display_name}")
    else:
        await ctx.send(f"{member.display_name} is already registered.")

@bot.command()
async def points(ctx, member: discord.Member):
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
    user_id = str(user.id)
    if user_id in registered_users:
        # Add points to the user
        registered_users[user_id]['points'] += points

        # Send a message confirming the addition
        await ctx.send(f"Added {points} points to {user.display_name}. They now have {registered_users[user_id]['points']} points.")
    else:
        await ctx.send(f"{user.display_name} is not registered.")

@bot.command()
async def tasks(ctx, user: discord.Member, points: int = 1):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user_id = str(user.id)
    if user_id in registered_users:
        # Update user data
        registered_users[user_id]['points'] += points
        registered_users[user_id]['tasks_completed'] += 1

        # Store task with timestamp
        task_log = registered_users[user_id].get('task_log', [])
        task_log.append({"timestamp": current_time, "points": points, "completed_by": ctx.author.display_name})
        registered_users[user_id]['task_log'] = task_log

        # Send a message including the current timestamp
        await ctx.send(f"Task completed by {user.display_name}! Current time: {current_time}")

        # List all completed tasks with timestamps
        task_list = [f"{task['timestamp']} - {task['points']} points (Completed by: {task['completed_by']})" for task in task_log]
        await ctx.send(f"{user.display_name}'s completed tasks:\n" + '\n'.join(task_list))
    else:
        await ctx.send(f"{user.display_name} is not registered.")

@bot.command()
async def print(ctx):
    workbook = xlsxwriter.Workbook('RegUsers.xlsx')
    worksheet = workbook.add_worksheet()

    # Setting up workbook
    worksheet.write('A1', 'Registered Users')
    worksheet.write('C1', 'Points')
    worksheet.write('E1', 'Tasks Completed')
    worksheet.write('G1', 'Task Log')  # Add a column for Task Log

    # Start from row 2 to write user data
    row = 1
    for user_id, info in registered_users.items():
        # Fetch the discord.Member object using user ID
        user = await bot.fetch_user(int(user_id))

        # Write user name to column A
        worksheet.write(row, 0, user.display_name)
        # Write points to column C
        worksheet.write(row, 2, info['points'])
        # Write tasks completed to column E
        worksheet.write(row, 4, info['tasks_completed'])

        # Write task log to column G
        task_log = info.get('task_log', [])
        task_log_str = '\n'.join([f"{task['timestamp']} - {task['points']} points (Completed by: {task['completed_by']})" for task in task_log])
        worksheet.write(row, 6, task_log_str)

        row += 1

    workbook.close()
    await ctx.send(file=discord.File('RegUsers.xlsx'))

@bot.command()
async def select_winner(ctx):
    global registered_users

    if not registered_users:
        await ctx.send("No registered users.")
        return
    
    if not eventName:
        await ctx.send("No event name set. Use !createEvent to set an event name.")
        return

    # Calculate the probability based on points
    total_points = sum(info['points'] for info in registered_users.values())
    probabilities = [info['points'] / total_points for info in registered_users.values()]

    winner_id = random.choices(list(registered_users.keys()), weights=probabilities, k=1)[0]
    winner_member = await ctx.guild.fetch_member(int(winner_id))

    await ctx.send(f"@everyone, the winner of event {eventName} is: {winner_member.display_name}")

#bot token
bot.run("MTE4MTI2NTc0MDE2NzQwMTU4Mw.GugB0V.CJKGDNoT0XFitznlVDe2p7y0Ia3UIK-QBLxcwA")