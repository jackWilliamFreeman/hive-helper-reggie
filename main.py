import discord
from discord.ext import commands
import os
from bot_logic import format_dice_params, roll_dice, get_insult

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
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
        await ctx.reply(f"Ere's your bloody dice: \r\n \r\n{result}\r\n\r\nYou {get_insult('long form')}")
    else:
        await ctx.reply(result)

@bot.command(name="soup", brief="a trash tier meme from ole Reggie, point it at a user", help="point this meme at a user, ie '!soup @user' for best effect")
async def soup(ctx, arg):
    user = arg
    reply = f"NO NECROMUNDA FOR YOU {user}"
    await ctx.send(reply)

@bot.command(name = "gimme", help="ole Reggie will petition on your behalf")
async def gimme(ctx):
    await ctx.reply(f"here you go you {get_insult('long form')}", files = [discord.File('gimme.jpg')])


bot.run(os.getenv('TOKEN'))


