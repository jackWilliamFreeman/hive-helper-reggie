import random 
import discord
from discord.ext import commands
import os

from numpy import true_divide
from bot_logic import format_dice_params, roll_dice, get_insult, get_scenario, get_treasure_result
import logging
import glob

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True)

@bot.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity = discord.Activity(
                          type = discord.ActivityType.watching, 
                          name = ' for some fucker to ask to me roll for them'))

global localstring
KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if KEY:
    localstring=''
else:
    localstring = 'assets/'

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
        return
    if params.addition_arg != 0:
        await ctx.reply(result)
        return
    await ctx.reply(f"sumfink aint right with that input, try and stick to the format you {get_insult('long form')}")
    

@bot.command(name="no", brief="a trash tier meme from ole Reggie, point it at a user", help="point this meme at a user, ie '!no @user' for best effect")
async def no(ctx, *arg):
    try: arg
    except: ctx.reply(f"put in a user to target as an argument you {get_insult('long form')}")
    user = arg[0]
    reply = f"NO NECROMUNDA FOR YOU {user}"
    logging.info("no meme out!")
    await ctx.send(reply, files = [discord.File(f'{localstring}no.jpg')])

@bot.command(name="praise", brief="reggie gonna give it to ya", help="point this meme at a user, ie '!praise @user' for best effect")
async def praise(ctx, *arg):
    try: arg
    except: ctx.reply(f"put in a user to target as an argument you {get_insult('long form')}")
    user = arg[0]
    reply = f'So it appears that {ctx.author.mention} wants someone to praise {user}\
    \r\n so congrats {user} you are a special snowflake and definately not a {get_insult("short form")}'
    logging.info("praise meme out!")
    await ctx.send(reply, files = [discord.File(f'{localstring}praise.gif')])

@bot.command(name = "gimme", help="ole Reggie will petition on your behalf")
async def gimme(ctx):
    await ctx.reply(f"here you go you {get_insult('long form')}", files = [discord.File(f'{localstring}gimme.jpg')])
    logging.info("gimme meme out!")


@bot.command(name="callout", brief="Reggie becomes your second in organising a duel", help="point this callout at a user, ie '!callout @user' for best effect")
async def callout(ctx, user):
    gifs = glob.glob(f"{localstring}*.gif")
    selected_gif = gifs[random.randint(0, len(gifs) -1)]
    text = f"Oh Shit! Hey {user}! I heard over by the facotorium sump that <@{ctx.message.author.id}> called you a {get_insult('long form')}, what you gonna do?!?"
    await ctx.send(text, files = [discord.File(selected_gif)])

@bot.command(name="battle", brief="get scenario and details for two users to battle", help="takes two users and whether to use the raider rules for this battle as arguments, ie. !battle @user1 @user2 raider or !battle @user1 @user2 settlement")
async def battle(ctx, *args):
    if len(args) < 3 or len(args) > 3:
        await ctx.reply(f"oi you {get_insult('long form')}, i need two users and either 'settlement' or 'raider' as inputs")
    user1 = args[0]
    user2 = args[1]
    raider_choice  = args[2]

    if raider_choice == "raider":
        raider_choice = True
    else: raider_choice = False

    text = get_scenario(user1, user2, raider_choice)

    await ctx.send(text)

@bot.command(name="loot", brief="reggie will reach into his magic loincloth for a special treat", help="takes an argument of a user who rolled and an optional 'smashed' to indicate smashing it. eg. !loot @jack smashed or !loot @jack")
async def loot(ctx, *args):
    is_smashed = False
    if not args:
        await ctx.reply(f"oi you {get_insult('long form')}, i need a user and optionally if they smashed it or not, if they smashed it write 'smashed' as well")
        return
    if len(args) == 2:
        if args[1] != 'smashed':
            await ctx.reply(f"oi you {get_insult('long form')}, i need a user and optionally if they smashed it or not, if they smashed it write 'smashed' as well")
            return
        else: is_smashed = True
            
    text = get_treasure_result(args[0], is_smashed)
    await ctx.reply(text)


bot.run(os.getenv('TOKEN'))

 
