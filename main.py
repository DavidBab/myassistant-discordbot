import discord
from discord.ext import commands
from credits import credit_system
from inventory import inventory_management
from commands import interactive_commands
from split import tabsplit
import json


TOKEN = "Add your token here"


# This is the prefix that the bot will respond to. It can be anything you want.
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


# This command removes the basic help menu.
client.remove_command('help')


# After the bot has logged in, this event will be called.
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_voice_state_update(member, before, after):
    '''
    The below function will check the on voice activity. If someone joins the channel with the id provided in 
    the channel_create_id, it will create a channel with the users username. If the created channel becomes
    empty the bot deletes the channel. It also require the category id where the channel shoud be added.
    '''

    guild = member.guild  # Get the guild from the member object

    # Find the desired voice channel to create and the category to move the channel into
    channel_create_name = "Channel Create"  # Replace with your desired channel name
    category_name = "Voice Channels"  # Replace with your desired category name

    channel_create = discord.utils.get(guild.voice_channels, name=channel_create_name)
    category = discord.utils.get(guild.categories, name=category_name)

    # If someone joins the channel with the desired name, it creates a voice channel.
    if after.channel and after.channel == channel_create:
        voice_channel = await guild.create_voice_channel(f"{member.name}'s Channel", category=category)
        # After creating it, moves the member inside the channel
        await member.move_to(voice_channel)

    # Checks if the channel that you disconnected from is not the channel_create voice channel
    if before.channel and before.channel != channel_create:
        # Gets the created voice channel that was created and where are the people located
        voice_channel = discord.utils.get(guild.voice_channels, id=before.channel.id)
        # If the voice channel is empty, it will delete the channel.
        if voice_channel and len(voice_channel.members) == 0:
            await voice_channel.delete()




@client.event
async def on_member_join(member):
    '''
    This event will occur when a member joins the server.
    '''

    # Get the guild
    guild = member.guild

    # This part opens the data.json file for reading and loads the content into the database variable.
    with open('data.json', 'r') as f:
        database = json.load(f)

    # This is the account variable that gets assigned to the database for the name.
    account = {
        "name": member.name,      # Get the member's name.
        "balance": 1500,          # Everyone starts with $1500.
        "inventory": [],          # Set to 0 by default.
            }

    # This line appends the database for the server.
    database[guild.name].append(account)

    # This part writes in the json file the rest changes.
    with open('data.json', 'w') as f:
        json.dump(database, f)




@client.event
async def on_guild_join(guild):
    '''
    If the bot joins a guild it will loop over every member in the members list. For every
    member it adds a new account tab with the members name which can be further customized after.
    '''

    # This part opens the data.json file for reading and loads the content into the config variable.
    with open('data.json', 'r') as f:
        database = json.load(f)
    # This will create a new database for the guild in the split json document.
    with open("split.json", "r") as d:
        split = json.load(d)

    # Create a key with the name of the guild and assign an empty list to it.
    database[guild.name] = []
    split[guild.name] = []

    # This creates a new section for the server in the database where you can add the account tabs.
    with open('data.json', 'w') as f:
        json.dump(database, f)

    # This loops over all the members inside the 
    for member in guild.members:
        # This flag checks if the member is already registered in the database with the bot.
        member_already_in = False
        # This loop loops over all the existing dictionaries in the database.
        for dict in database[guild.name]:
            # If the name is already in it won't add another account by setting the "member_already_in" flag to True.
            if dict.get('name') == member.name:
                member_already_in = True


        # This if statement only executes if the flag "member_already_in" is False. It creates an account and appends
        # the database for the discord server with the specific name.
        if not member_already_in:
            account = {
                "name": member.name,   # Get the member's name.
                "balance": 1500,       # Everyone starts with $1500.
                "inventory": [],       # Set empty by default.
            }

            # Appends the account to the correct discord server.
            database[guild.name].append(account)

    # This part writes in the json file the rest changes.
    with open('data.json', 'w') as f:
        json.dump(database, f)
    
    with open("split.json", "w") as d:
        json.dump(split, d)
        



credit_system(client)
inventory_management(client)
interactive_commands(client)
tabsplit(client)




client.run(TOKEN)
