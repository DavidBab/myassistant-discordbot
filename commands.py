import discord
from discord.ext import commands
from discord.ext.commands import BucketType, CommandOnCooldown
import Paginator
import random
import json




def interactive_commands(client):
    @client.hybrid_command()
    @commands.cooldown(1, 30, BucketType.user)
    async def fish(ctx: commands.Context):
        # List of all possibilities to append your inventory with.
        possible_catch = [[":fish:", "Fish", random.randint(1,3)],[":duck:", "Duck", 1], [":shark:", "Shark", 1], [":crab:", "Crab", random.randint(1,2)], [":jellyfish:", "Jellyfish", random.randint(1,2)], [":tropical_fish:", "Tropical Fish", random.randint(1,2)],[":dolphin:", "Dolphin", 1],[":anchor:", "Anchor", 1]]

        # Open the json database and read out the information from it.
        with open("data.json", "r") as f:
            database = json.load(f)

        # Variables, to determine some logical statements.
        can_fish = False
        found = False
        # It chooses a random "catch" from the possible catches
        if random.random() <= 0.8:
            catch = random.choice([possible_catch[0], possible_catch[1]])
        else:
            catch = random.choice(possible_catch)

        # Looping trough users in the server.
        for user in database[ctx.guild.name]:
            # If we find the user who wrote a message we loop over his inventory.
            if user.get('name') == ctx.author.name:
                for item in user.get('inventory'):
                    # If an item in the users inventory is the fishing pole he will be able to fish.
                    if item[0] == ":fishing_pole_and_fish:":
                        can_fish = True
                        continue
                        
                    # If the item already exist it just adds the fished amount to the existing item, found is set to True.
                    if item[0] == catch[0] and can_fish:
                        item[2] += catch[2]
                        found = True
                        await ctx.send(f"You have caught {catch[2]} {catch[0]} {catch[1]}")
                        break
                break

        # If the item is not found and user is able to fish we append his inventory with the catch.
        if not found and can_fish:
            user['inventory'].append(catch)
            await ctx.send(f"You have caught {catch[2]} {catch[0]} {catch[1]}")

        # If he has no pole this will be activated
        if not can_fish:
            await ctx.send("You first need to obtain a fishing pole.")
        
        # Open the json file and dump in the new data.
        with open("data.json", "w") as f:
            json.dump(database, f)

    # Fishing set for 30 second cooldown with feedback message.
    @fish.error
    async def fish_error(ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send("This command can be used every 30 seconds.")
        else:
            raise error





    @client.hybrid_command()
    async def shop(ctx: commands.Context):

        with open("shop.json", "r") as f:
            store = json.load(f)

        embeds = []
        count= 0

        for item_list in store["Shop"]:
            # This is to create a new embed after every 8 items.
            if count == 0:
                # Creating a new embed.
                embed = discord.Embed(
                    title = "MyAssistant Shop",
                    description = "",
                    color = discord.Color.random())
            # Adding +1 to the count for every item.
            count += 1
            embed.add_field(name=f"{item_list[0]} {item_list[1]}", value=f"Price: ${item_list[2]}", inline=False)

            # When count reaches 8 it sets the count to 0 to create a new embed and append the existing one into the embeds list.
            if count == 6:
                count = 0
                embeds.append(embed)
                embed.set_footer(text="This message won't work after some time.")
        
        # When the loop is over and there is still one embed remaining it appends it to the embeds. 
        if count != 0:
            embeds.append(embed)
            embed.set_footer(text="This message won't work after some time.")

        # At the end we return the embeds using Paginator as a text message.
        await Paginator.Simple().start(ctx, pages=embeds)




    @client.hybrid_command()
    async def buy(ctx: commands.Context, item):
        item = item.lower()

        # We open both json files to read from them.
        with open("data.json", "r") as f:
            data = json.load(f)
        with open("shop.json", "r") as d:
            store = json.load(d)

        # Found variable for finding the item in your inventory
        found = False

        # Searching the Shop for the given item.
        for goods in store["Shop"]:
            if goods[1].lower() == item:
                # Create a variable for the price to store it for later
                price = goods[2]
                # Looping trough users and finding the author.
                for user in data[ctx.guild.name]:
                    if user.get('name') == ctx.author.name:
                        user['balance'] -= price
                        # Setting the "price" to the new "amount" of the bought item if it would be appended to the inventory.
                        goods[2] = 1
        
                        # Loop over items in your inventory.
                        for inv_item in user.get('inventory'):
                            # Adding +1 to the amount if there is already a item that matches the buy request.
                            if inv_item[1].lower() == item:
                                inv_item[2] += 1
                                found = True       
                                await ctx.send(f"{ctx.author.display_name}, you bought {goods[2]} {goods[1]} {goods[0]} for ${price}")
                                break
                        break         
                break

        # If there was no item that mached the item bought we append the inventory with the bought item.
        if not found:
            user['inventory'].append(goods)
            await ctx.send(f"{ctx.author.display_name}, you bought {goods[2]} {goods[1]} {goods[0]} for ${price}")
            

        # Writing the data into the inventory, we are not writing it to the store so that the price doesn't gets changed.
        with open("data.json", "w") as f:
            json.dump(data, f)





    @client.hybrid_command()
    async def sell(ctx: commands.Context, item, amount = None):
        # Put the item into lowercase so that whatever input it gets it can find a match.
        item = item.lower()
        # Prices of the fishes.
        collectibles = [[":fish:", "Fish", random.randint(5,12)],[":rock:", "Rock", 10], [":gem:", "Diamond", 500],[":duck:", "Duck", random.randint(8,15)], [":shark:", "Shark", random.randint(80,150)], [":crab:", "Crab", random.randint(13,18)], [":jellyfish:", "Jellyfish", random.randint(19,34)], [":tropical_fish:", "Tropical Fish", random.randint(21,30)],[":dolphin:", "Dolphin", random.randint(14,45)],[":anchor:", "Anchor", 160]]

        # Opening the database of the shop and the user inventory.
        with open("data.json", "r") as f:
            data = json.load(f)
        with open("shop.json", "r") as d:
            store = json.load(d)

        # Item owned flag that is set to True when the program finds the item.
        item_owned = False

        # Prices if you sell a fish. You get a random number for every piece.
        for fishes in collectibles:
            if fishes[1].lower() == item:
                price = fishes[2]

        # Prices if you sell an item from the store. You get the half back
        for goods in store["Shop"]:
            if goods[1].lower() == item:
                price = goods[2] // 2

        # Looping over the users.
        for user in data[ctx.guild.name]:
            # If ctx.author name matches we continue.
            if user.get('name') == ctx.author.name:
                # Looping trough every item in the users inventory.
                for inv_item in user.get('inventory'):
                    # In case we find the item we the item_owned is set to True and we continue with other parts.
                    if inv_item[1].lower() == item:
                        item_owned = True

                        # These are here to store the emoji and name if it gets deleted.
                        emoji = inv_item[0]
                        name = inv_item[1]

                        # When the amount argument is not set this line of code triggers.
                        if amount == None:
                            inv_item[2] -= 1
                            user['balance'] += price
                            # When the amount is 0 in the user inventory from the sold item, it automatically removes the item in his/her inventory
                            if inv_item[2] == 0:
                                user['inventory'].remove(inv_item)
                            await ctx.send(f"{ctx.author.display_name}, you sold 1 {emoji} {name} for ${price}")
                        
                        # If there is an amount argument set this line of code triggers.
                        if amount != None:
                            # Variables for counting in the for loop.
                            final_price = 0
                            pieces_sold = 0
                            # Loops over each time until the amount the user gave matches the amount that he has in his inventory.
                            for _ in range(int(amount)):
                                inv_item[2] -= 1
                                pieces_sold += 1
                                final_price += price
                                # When the amount is = 0, it removes the whole item, breakes the loop and sends an informative message to the user about how many pieces it sold and for how much of the item.
                                if inv_item[2] == 0:
                                    user['balance'] += final_price
                                    user['inventory'].remove(inv_item)
                                    await ctx.send(f"{ctx.author.display_name}, you sold {pieces_sold} {emoji} {name} for ${final_price}")
                                    break
        
        # If the item was not found in his inventory, this gets triggered
        if not item_owned:
            await ctx.send("Sorry, but you don't own that item.")
                           
        # We write the new information to the file.
        with open("data.json", "w") as f:
            json.dump(data, f)
        

        
        
    @client.hybrid_command()
    async def howgay(ctx: commands.Context, member: discord.Member = None):
        # Generates a randum number between 0-120
        number = random.randint(0,120)
        
        # If there is no member in the command this gets triggered.
        if member == None:
            if ctx.author.name == "dawe5956":
                await ctx.send(f"{ctx.author.mention}, you are the most heterosexual man that I know!")
            else:
                await ctx.send(f"{ctx.author.mention}, you are :rainbow_flag: {number}% gay!")

        # If there is a member argument this gets triggered.
        else:
            if member.name == "dawe5956":
                await ctx.send(f"{member.mention} is the most heterosexual man I know!")
            else:
                await ctx.send(f"{member.mention}, you are :rainbow_flag: {number}% gay!")


    
    @client.hybrid_command()
    async def rob(ctx: commands.Context, member: discord.Member = None):
        pass



    @client.hybrid_command()
    async def slots(ctx: commands.Context):
        # Open the data.json file to read out data.
        with open("data.json", "r") as f:
            data = json.load(f)

        # Options that can be spinned out.
        options = [":gem:", ":trophy:", ":fire:", ":moneybag:", ":bomb:"]

        # The combination of the above options.
        combination = [options[random.randint(0,4)], options[random.randint(0,4)], options[random.randint(0,4)]]

        # Price that you win, default is zero + won flag set to False.
        price = 0
        won = False

        # If the three signs match the price changes based on what signs you got.
        if combination[0] == combination[1] == combination[2]:
            # Won is set to True, and you get price based on what you roll. 
            won = True
            # Gems.
            if combination[0] == options[0]:
                price = 100000
            # Moneybag.
            elif combination[0] == options[1]:
                price = 50000
            # Bomb.
            elif combination[0] == options[4]:
                price = -500
            # Everything else.
            else:
                price = 500

        # Loops over the users until it finds the user with the authors name.
        for user in data[ctx.guild.name]:
            if user.get('name') == ctx.author.name:
                # If the user has more money than 100 he can play.
                if user.get('balance') >= 100:
                    # The money for the game is taken from the user and a price is added if he won anything.
                    user['balance'] = user['balance'] - 100 + price
                    # Bot outputs based on win or lose.
                    if not won:
                        await ctx.send(f"{ctx.author.display_name}, you spinned the slot machine and got: | {combination[0]} | {combination[1]} | {combination[2]} |")
                        break
                    else:
                        await ctx.send(f"{ctx.author.display_name}, you spinned | {combination[0]} | {combination[1]} | {combination[2]} | and won ${price}")
                        break
                
                # If the user doesn't have enough money this gets triggered.
                else:
                    await ctx.send(f"{ctx.author.display_name}, you need ${100 - user['balance']} more to play slots.")
                    break

        # We write in the data into the data.json document.
        with open("data.json", "w") as f:
            json.dump(data, f)
       


    @client.hybrid_command()
    @commands.cooldown(1, 30, BucketType.user)
    async def mine(ctx: commands.Context):
        options = [[":rock:", "Rock", random.randint(1,2)], [":gem:", "Diamond", 1]]
        
        # Choose the first item most of the time
        if random.random() <= 0.8:
            choice = options[0]
        else:
            choice = random.choice(options)
        
        # Open the json database and read out the information from it.
        with open("data.json", "r+") as f:
            database = json.load(f)

        # Variables, to determine some logical statements.
        can_mine = False
        found = False

        # Looping trough users in the server.
        for user in database[ctx.guild.name]:
            # If we find the user who wrote a message we loop over his inventory.
            if user.get('name') == ctx.author.name:
                for item in user.get('inventory'):
                    # If an item in the users inventory is the fishing pole he will be able to fish.
                    if item[0] == ":pick:":
                        can_mine = True
                        continue
                        
                    # If the item already exist it just adds the fished amount to the existing item, found is set to True.
                    if item[0] == choice[0] and can_mine:
                        item[2] += choice[2]
                        found = True
                        await ctx.send(f"You have caught {choice[2]} {choice[0]} {choice[1]}")
                        break
                break

        # If the item is not found and user is able to fish we append his inventory with the catch.
        if not found and can_mine:
            user['inventory'].append(choice)
            await ctx.send(f"You have caught {choice[2]} {choice[0]} {choice[1]}")

        # If he has no pole this will be activated
        if not can_mine:
            await ctx.send("You first need to obtain a Pickaxe.")
        
        # Open the json file and dump in the new data.
        with open("data.json", "w") as f:
            json.dump(database, f)

    # Fishing set for 30 second cooldown with feedback message.
    @mine.error
    async def mine_error(ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send("This command can be used every 30 seconds.")
        else:
            raise error
        
    
    @client.hybrid_command()
    async def help(ctx: commands.Context):
        embeds = []

        embed = discord.Embed(title="Help Menu", description="The prefix of the commands is !", color=discord.Color.random())

        embed.add_field(name="**Entertainment Commands**", value="", inline=False)
        embed.add_field(name="-`fish` Catch fish", value="", inline=False)
        embed.add_field(name="-`mine` Mine for resources", value="", inline=False)
        embed.add_field(name="-`inventory` Shows your inventory", value="", inline=False)
        embed.add_field(name="-`shop` View items in the shop", value="", inline=False)
        embed.add_field(name="-`buy [item]` Buy an item from the shop", value="", inline=False)
        embed.add_field(name="-`sell [item] [amount]` Sell an item from your inventory", value="", inline=False)
        embed.add_field(name="-`howgay [member]` Check how gay someone is", value="", inline=False)
        embed.add_field(name="-`balance` Shows your or someones balance", value="", inline=False)
        embed.add_field(name="-`donate [money] [member]` Donates money to given member.", value="", inline=False)
        embed.add_field(name="-`slots` Play slots", value="", inline=False)

        embeds.append(embed)

        embed = discord.Embed(title="Help Menu", description="The prefix of the commands is !", color=discord.Color.random())

        embed.add_field(name="**Tabslpit Commands**", value="", inline=False)
        embed.add_field(name="-`create [id] [money] [members]` Creates a tab", value="", inline=False)
        embed.add_field(name="-`accept [id]` Accepts the money form the tab", value="", inline=False)
        embed.add_field(name="-`remove [id]` Removes a tab based on id", value="", inline=False)
        embed.add_field(name="-`show [id]` Shows information about a tab", value="", inline=False)
        embed.add_field(name="-`tabs` Shows all the tabs avilable.", value="", inline=False)
        
        embeds.append(embed)

        await Paginator.Simple().start(ctx, pages=embeds)
        