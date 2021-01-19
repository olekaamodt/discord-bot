import discord
import os
from just_eat_scraper import FoodDelivery
import re
import asyncio

fastFood = FoodDelivery()

bot_token, guild_name = fastFood.get_bot_tokens("token.json")

client = discord.Client()





emojiArr = []

with open("emojis.txt", encoding = 'utf-8') as emojis:
    content = emojis.read()
    emojiArr = list(content.split(" "))



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


    if message.content.startswith('$food'):
        
        postalCode = message.content[6:10]
        restaurants = fastFood.get_all_restaurants(postalCode)
        usedEmojis = []
        restaurantChoice = {}

        embedVar = discord.Embed(title="Restaurants near " + postalCode, description="Restauranger", color=0x00ff00)
        for i in range(len(restaurants)):
            
            if restaurants[i]["IsOpenNow"]:
                usedEmojis.append(emojiArr[i])

                #makes embed for all open restaurants in the area
                restaurantChoice[emojiArr[i]] = {"Name": restaurants[i]["Name"], "Id":restaurants[i]["Id"], "MenuId":restaurants[i]["CollectionMenuId"]}

                embedVar.add_field(name=restaurants[i]["Name"] + " " + emojiArr[i], value="Åpent", inline=False)

            else:
                usedEmojis.append(emojiArr[i])
                restaurantChoice[emojiArr[i]] = {"Name": restaurants[i]["Name"], "Id":restaurants[i]["Id"], "MenuId":restaurants[i]["CollectionMenuId"]}
                embedVar.add_field(name=restaurants[i]["Name"] + " " + emojiArr[i], value="Stengt", inline=False)
           

        msg = await message.channel.send("Velg Restaurant", embed = embedVar)
        for emoji in usedEmojis:
            await msg.add_reaction(emoji)

        await asyncio.sleep(10)

        msg = await msg.channel.fetch_message(msg.id)
        
        for reaction in msg.reactions:
            if reaction.count == 2:
                restaurant_name = restaurantChoice[reaction.emoji]["Name"]

                #fetches the menu from the just eat rest API
                menu = fastFood.get_menu(restaurantChoice[reaction.emoji]["MenuId"])

                await message.channel.send("du har valgt " + restaurant_name)
                await message.channel.send("henter meny fra " + restaurant_name)

                # makes the menu from the menu dictionary from the api
                pages, contents, food_emojis = create_menu_pages(discord, menu, restaurant_name, emojiArr)
        
        # amount of pages it changes when emoji is clicked
        cur_page = 1

        message_menu = await message.channel.send(f"Page {cur_page}/{pages}", embed = contents[cur_page-1])
        # getting the message object for editing and reacting

        # adding emojis the menu embed message
        await message_menu.add_reaction("◀️")
        await message_menu.add_reaction("▶️")
        await message_menu.add_reaction("👍")
        for emoji in food_emojis["0"].keys():
            await message_menu.add_reaction(emoji)

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ["◀️", "▶️", "👍"] + emojiArr
            # This makes sure nobody except the command sender can interact with the "menu"

        chosen_menu_items = []

        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message_menu.edit(content=f"Page {cur_page}/{pages}:", embed = contents[cur_page-1])
                    await message_menu.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message_menu.edit(content=f"Page {cur_page}/{pages}:", embed = contents[cur_page-1])
                    await message_menu.remove_reaction(reaction, user)
                    
                # finished choosing the items
                elif str(reaction.emoji) == "👍" and cur_page:
                    await message.channel.send("Du har valgt følgende")
                    for item in chosen_menu_items:
                        await message.channel.send(item)

                elif str(reaction.emoji) in food_emojis[str(cur_page - 1)].keys():
                    name = "Name"
                    id_name = "Id"
                    # adds the menu items chosen from the discord chat
                    item_name = food_emojis[str(cur_page - 1)][str(reaction.emoji)][name]
                    food_id = food_emojis[str(cur_page - 1)][str(reaction.emoji)][id_name]
                    await message.channel.send(f"{item_name} har blitt lagt til ")
                    chosen_menu_items.append((item_name, food_id[0]))
                    

                else:
                    await message_menu.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page

            except asyncio.TimeoutError:
                await message_menu.delete()
                break
                # ending the loop if user doesn't react after x seconds

        #menuEmbed = create_menu_embed(menuEmbed, menu)
        #menu_msg = await message.channel.send("Velg produkt", embed = menuEmbed)
        
        



def create_menu_pages(discord, menu_dict, restaurant_name, emoji_arr):
    contents = []
    pages = 0
    max_items = 17
    emoji_index = 0
    embed_menu = discord.Embed(title="meny for " + restaurant_name, description="Meny", color=0x00ff00)
    used_emojis_food = {}

    # loops thorugh the menu dictionary to make the emnu embed for the selected restaurant
    for i in range(len(menu_dict)):
        # for each 23rd item a new embed will be made which will be one page
        if i == max_items:
            emoji_index = 0
            embed_menu = discord.Embed(title="meny for " + restaurant_name, description="Meny", color=0x00ff00)
            max_items += max_items
            pages += 1

        if str(pages) not in used_emojis_food.keys():
            used_emojis_food[str(pages)] = {}
            
        if not menu_dict[i]["Desc"]:
            embed_menu.add_field(name=menu_dict[i]["Name"] + " " +  emoji_arr[emoji_index], value=i, inline=True)
            used_emojis_food[str(pages)][emoji_arr[emoji_index]] = {"Name":menu_dict[i]["Name"], "Id":[menu_dict[i]["Id"]]}

        if menu_dict[i]["Desc"]:
            # adds each item as a field in the embed
            embed_menu.add_field(name=menu_dict[i]["Name"] + "(" + menu_dict[i]["Syn"] +  ") " + emoji_arr[emoji_index], value=menu_dict[i]["Desc"], inline=True)
            used_emojis_food[str(pages)][emoji_arr[emoji_index]] = {"Name":menu_dict[i]["Name"] + " " + menu_dict[i]["Syn"], "Id":[menu_dict[i]["Id"]]}
                    

        if i == (max_items - 1):
            contents.append(embed_menu)

        emoji_index += 1

    return pages, contents, used_emojis_food


    # def check_emoji(emoji, used_emojis):






        







            


client.run(bot_token)