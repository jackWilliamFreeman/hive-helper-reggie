import random
from insult_logic import get_insult
import re

class dice_params:
    def __init__(self, addition_arg, is_distinct, dice_size, dice_no):
        self.addition_arg = addition_arg
        self.is_distinct = is_distinct
        self.dice_size = dice_size
        self.dice_no = dice_no

async def format_dice_params(ctx, args):  
    is_distinct = False
    addition_arg = 0
    dice_no = 1
    dice_size = 1
    match = re.search('^\d{0,2}d\d{1,2}$', args[0].lower())
    dice_args = args[0].lower().split("d")
    if match:
        dice_no = int(dice_args[0] or 1)
        dice_size = int(dice_args[1])     
    else: 
        await ctx.reply(f"give me a good format you {get_insult('long form')}, something like !roll 1d6 or !roll d6, max 2 digits so 1-99")
        raise Exception("the fuck...")
 

    if len(args) > 1:
        i = 1
        while(i <= (len(args) - 1)):
            current_arg = args[i]
            if current_arg.startswith('+'):
                addition_arg = int(args[1].split('+')[1])
            if current_arg.startswith('distinct'):
                is_distinct = True
            i += 1
    params = dice_params(addition_arg, is_distinct, dice_size, dice_no)
    return params

def roll_dice(params):
    i = 1
    rolls = []
    try: params.addition_arg
    except: params.addition_arg = 0
    try: params.is_distinct
    except: params.is_distinct = False
    #handle case of too many rolls for discrete
    if params.is_distinct:
        if(params.dice_no > params.dice_size):
            return f"oi {get_insult('short form')}, too many dice rolled for the amount of possible distinct options"
    #roll dice, handle discrete and addition case as well
    while i <= params.dice_no:
        roll = random.randint(1, params.dice_size) 
        if params.is_distinct and (roll) not in rolls:  
            rolls.append(roll)
            i += 1
        if not params.is_distinct:
            i += 1
            rolls.append(roll) 
    if params.addition_arg > 0:
        total = 0
        for roll in rolls:
            total += roll
        total += params.addition_arg
        return f"Getting me to do quick mafs eh? well Reggie learned his letters so 'ere we go:\
                \r\nyou rolled **{rolls}** + **{params.addition_arg}**, when I add them all together I get: **{total}**\
                \r\nHow is that for quick mafs you {get_insult('short form')}"
    rolls.sort()
    return rolls