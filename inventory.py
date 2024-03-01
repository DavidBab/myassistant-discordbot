import discord
from discord.ext import commands
import json
import Paginator



def inventory_management(client):
    @client.hybrid_command()
    async def inventory(ctx: commands.Context, member: discord.Member = None):
        '''
        This command displays an inventory of yours or an inventory of the chosen person. Every item
        in your inventory is a list. The first item in the list is an emoji, the second is the name
        of the item, and the third is the amount of the item.
        '''

        # Open the data.json file with open
        with open('data.json', 'r') as f:
            database = json.load(f)

        # Set an embeds list for the embeds and a count to count elements in one embed
        embeds = []
        count = 0

        # Try is for errors, like empty Inventory etc...
        try:
            # If there is no member it loops over the autors inventory.
            if member is None:
                # Looping over the database which contains the Server name, until we find matching username.
                for user in database[ctx.guild.name]:
                    if user.get('name') == ctx.author.name:
                        # Loops over every item in the inventory (item is a list).
                        for item_list in user.get('inventory'):
                            # This is to create a new embed after every 8 items.
                            if count == 0:
                                # Creating a new embed.
                                embed = discord.Embed(
                                    title = f"{ctx.author.display_name}'s Inventory",
                                    description = "",
                                    color = discord.Color.random())
                            # Adding +1 to the count for every item.
                            count += 1
                            embed.add_field(name=f"{item_list[0]} {item_list[1]}", value=f"Amount: {item_list[2]}", inline=False)

                            # When count reaches 6 it sets the count to 0 to create a new embed and append the existing one into the embeds list.
                            if count == 6:
                                count = 0
                                embeds.append(embed)
                                embed.set_footer(text="This message won't work after some time.")
                        
                        # When the loop is over and there is still one embed remaining it appends it to the embeds. 
                        if count != 0:
                            embeds.append(embed)
                            embed.set_footer(text="This message won't work after some time.")


            # If it finds a member parameter it will search for that member.
            else:
                # Here happens the same, but the member is the member mentioned in the !inventory command.
                for user in database[ctx.guild.name]:
                    if user.get('name') == member.name:
                        for item_list in user.get('inventory'):
                            if count == 0:
                                embed = discord.Embed(
                                    title = f"{member.display_name}'s Inventory",
                                    description = "",
                                    color = discord.Color.random())
                            count += 1
                            embed.add_field(name=f"{item_list[0]} {item_list[1]}", value=f"Amount: {item_list[2]}", inline=False)

                            if count == 6:
                                count = 0
                                embeds.append(embed)
                                embed.set_footer(text="This message won't work after some time.")

                        if count != 0:
                            embeds.append(embed)
                            embed.set_footer(text="This message won't work after some time.")
            
            # At the end we return the embeds using Paginator as a text message.
            await Paginator.Simple().start(ctx, pages=embeds)

            

        
        # If something goes wrong.
        except:
            await ctx.send('Sorry something went wrong, or inventory of the user could be empty.')
