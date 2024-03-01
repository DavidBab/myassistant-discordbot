import discord
import json
from discord.ext import commands



def tabsplit(client):
    @client.hybrid_command()
    async def create(ctx: commands.Context, id, money, members):
        
       # This part calculates the split from the money based on the members.
        split = int(money) // len(members)

        # This command adds the properties to a dictionary.
        money_split = {
            "money": money,
            "members": members,
            "split": split,
            "id": id,
        }

        # This command just shows what you added to the 
        await ctx.send(f"{ctx.author.display_name}, you have added new tab with the ID: {id}")

        # The below commands open a json file called data.json as reading than saves it into a variable called data. 
        with open('split.json', 'r') as f:
            data = json.load(f)

        # We append the data with our money_split dictionary.
        data[ctx.guild.name].append(money_split)

        # As the last step we write it into the json file.
        with open('split.json','w') as f:
            json.dump(data, f)



    @client.hybrid_command()
    async def accept(ctx: commands.Context, id = None):
        # First, open the data.json file for reading and load it as the config variable.
        if id == None:
            await ctx.send("Provide an ID please.")
            return

        with open('split.json', 'r') as f:
            data = json.load(f)

        for dict in data[ctx.guild.name]:
            if dict.get('id') == id:
                if ctx.author.mention in dict.get('members'):
                    dict.get('members').remove(ctx.author.mention)
                    await ctx.send(f"{ctx.author.display_name}, you have been removed from tab ID: {id}")
                    break
                else:
                    await ctx.send(f"{ctx.author.display_name}, you are not a member of tab ID: {id}")
                    break

        # Finally, rewrite the data.json file with the updated config file.
        with open('split.json', 'w') as f: 
            json.dump(data, f)



    @client.hybrid_command()
    async def remove(ctx: commands.Context, id):
        # This part opens the data.json file for reading and loads the content into the config variable.
        with open('split.json', 'r') as f:
            data = json.load(f)

        # This loop loops over all the data and searches for the ID that you gave it as an argument.
        for dict in data[ctx.guild.name]:
            if dict.get("id") == id:
                # If it finds the ID it removes the whole dictionary that contains the item.
                data[ctx.guild.name].remove(dict)

                # Finally we send a message that the dictionary was successfully removed.
                await ctx.send(f"{ctx.author}, you removed tab ID: {id}")

                break
            # This statement occurs when there is no such id that the user gave.
            if dict.get("id") == None:
                await ctx.send(f"There is no tab with the id of: {id}")


        # Finally this line rewrites the data.json file with the new config file without the dictionary.
        with open('split.json','w') as f:
            json.dump(data, f)




    @client.hybrid_command()
    async def tabs(ctx: commands.Context):
        # This opens the data.json file for reading and loads it as data variable.
        with open('split.json', 'r') as f:
            data = json.load(f)

        # This creates the "header" of the message.
        message = "**Here are the tabs you can use:**\n"

        # For every 'id' it appends the "message" with a new line represented with "\n" that contains an ID.
        for dict in data[ctx.guild.name]:
            message += "* " + str(dict.get("id")) + "\n"

        # Finally it sends the whole message to the channel.
        await ctx.send(message)

                        



    @client.hybrid_command()
    async def show(ctx: commands.Context, id):
        # First it opens the data.json file for reading and loads it as config variable.
        with open('split.json', 'r') as f:
            data = json.load(f)

        # Flag variable to track if the loot with the specified ID is found
        found = False

        embed = discord.Embed(color= discord.Color.random())
        embed.set_author(name=f"ID: {id}", icon_url=client.user.avatar.url)

        # We iterate over the the files that is owned by the guild name.
        for dict in data[ctx.guild.name]:
            # If we find the ID, the bot sends a message with the values of the keys we provide it.
            if dict.get('id') == id:
                embed.add_field(name=f"Total: {dict.get('money')} | Split: {dict.get('split')}", value=dict.get('members'), inline=True)
                found = True
                await ctx.send(embed=embed)
                break

        # If there is no ID that we specified, it will send an error message to the channel.
        if not found:
            await ctx.send(f"There is no tab with the id of: {id}")

    