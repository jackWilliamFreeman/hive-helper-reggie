import discord
from discord.ext import commands
import os
from bot_logic import format_dice_params, roll_dice, get_insult, get_scenario
import logging

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True)

@bot.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity = discord.Activity(
                          type = discord.ActivityType.watching, 
                          name = ' for some fucker to ask to me roll for them'))


@bot.command(name="roll", brief="Unable to do basic mafs? ole Reggie knows his letters", help="ole Reggie will roll some dice, accepted formats: XXdXX ie 1d4 or 10d20, also accepts parameters after like 'distinct' to keep rolls distinct. eg. !roll 10d4 distinct",usage="[0-2]<number> d [1-2]<number> eg. 10d20 or d4, optional parameters: '+number' to add to rolls and 'distinct' to keep only unique rolls")
async def roll(ctx, *args):
    try: args
    except: 
        await ctx.send(f"you gotta specify some dice arguments you {get_insult('long form')}, try 1d6 or something")
        return
    params = await format_dice_params(ctx, args)
    result = roll_dice(params)
    if isinstance(result, list):
        logging.info("rolling some dice for mates")
        await ctx.reply(f"Ere's your bloody dice: \r\n \r\n{result}\r\n\r\nYou {get_insult('long form')}")
    else:
        await ctx.reply(result)

@bot.command(name="no", brief="a trash tier meme from ole Reggie, point it at a user", help="point this meme at a user, ie '!no @user' for best effect")
async def no(ctx, arg):
    user = arg
    reply = f"NO NECROMUNDA FOR YOU {user}"
    logging.info("no meme out!")
    await ctx.send(reply)

@bot.command(name = "gimme", help="ole Reggie will petition on your behalf")
async def gimme(ctx):
    await ctx.reply(f"here you go you {get_insult('long form')}", files = [discord.File('gimme.jpg')])
    logging.info("gimme meme out!")

@bot.command(name = "strain", help="ole Reggie will display the insignia of the biker strain")
async def strain(ctx):
    await ctx.reply(f"here you go you {get_insult('long form')}", files = [discord.File('strain.png')])
    logging.info("gimme meme out!")

@bot.command(name="callout", brief="Reggie becomes your second in organising a duel", help="point this callout at a user, ie '!callout @user' for best effect")
async def callout(ctx, arg):
    user = arg
    reply = f"Oh Shit he done called you out {user}, What are you gonna do you {get_insult('long form')}?"
    await ctx.send(reply, files = [discord.File('ohshit.gif')])

@bot.command(name="battle", brief="get scenario and details for two users to battle", help="takes two users and whether to use the raider rules for this battle as arguments, ie. !battle @user1 @user2 raider or !battle @user1 @user2 settlement")
async def battle(ctx, *args):
    user1 = args[0]
    user2 = args[1]
    raider_choice  = args[2]

    if raider_choice == "raider":
        raider_choice = True
    else: raider_choice = False

    text = get_scenario(user1, user2, raider_choice)

    await ctx.send(text)


bot.run(os.getenv('TOKEN'))

 
