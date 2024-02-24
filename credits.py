import discord
from discord.ext import commands
import json
import Paginator



def credit_system(client):
    # Give Money to a desired member.
    @client.command()
    async def donate(ctx, amount, name: discord.Member):
        # We open the "data.json" for reading.
        with open('data.json', 'r') as f:
            database = json.load(f)

        have_money = False

        # Loops over the dictionaries.
        for dict in database[ctx.guild.name]:
            if dict.get('name') == ctx.author.name:
                if dict.get('balance') >= int(amount):
                    dict['balance'] -= int(amount)
                    have_money = True
                else:
                    break


            if dict.get('name') == name.name and have_money:
                # Convert the 'amount' to an integer and add it to the value for the 'balance' key.
                dict['balance'] += int(amount)
                break

        if not have_money:
            await ctx.send(f"{ctx.author.display_name}, you don't have ${amount} in your wallet.")

        if have_money:
            await ctx.send(f"{ctx.author.display_name}, you sent ${amount} to {name.display_name}")

        

        # Save the updated dictionary back to the file
        with open('data.json', 'w') as f:
            json.dump(database, f)  
        


    # Reseting someones balance
    @client.command()
    @commands.is_owner()  # Add this line to restrict usage to server owner
    async def reset(ctx, member: discord.Member):

        # We open the "data.json" for reading.
        with open('data.json', 'r') as f:
            database = json.load(f)

        # Flag if you find the member.
        found = False

        # We loop over all dictionaries in the database at the index of the guilds server.
        for dict in database[ctx.guild.name]:
            if dict.get('name') == member.name:
                # Reset the balance to 0.
                dict['balance'] = 0
                # The found flag turn to True.
                found = True

        # Checks if we found the user, if we did and reseted the account it will display that it got reseted.
        if found:       
            await ctx.send(f"{ctx.author}, you successfully reset {member.display_name}'s balance.")
        # If the name was not found it returns an error message.
        else:  
            await ctx.send(f"User with name '{member.display_name}' not found.")

        # Save the updated dictionary back to the file.
        with open('data.json', 'w') as f:
            json.dump(database, f)




    # Balance checking command 
    @client.command()
    async def balance(ctx, member: discord.Member = None):
        
        # We open the "data.json" for reading.
        with open('data.json', 'r') as f:
            database = json.load(f)
       
        # We loop over the users in the server.
        for user in database[ctx.guild.name]:
            # If there was no member specified, it displays the authors wallet.
            if member is None:
                if user.get('name') == ctx.author.name:
                    await ctx.send(f"{ctx.author.display_name}, you have ${user.get('balance')} in your wallet.")
                    break
            
            # If there was a member specified, it displays the members wallet.
            else:
                if user.get('name') == member.name:
                    await ctx.send(f"{member.display_name}'s wallet contains ${user.get('balance')}")
                    break

            
        


          
    