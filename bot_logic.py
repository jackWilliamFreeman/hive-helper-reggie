from distutils.log import error
import random
import re
from sqlite3 import paramstyle

class dice_params:
    def __init__(self, addition_arg, is_distinct, dice_size, dice_no):
        self.addition_arg = addition_arg
        self.is_distinct = is_distinct
        self.dice_size = dice_size
        self.dice_no = dice_no
    

pre_insults = ['moronic', 'obtuse', 'inane', 'rotund', 'fat', 'surly', 'ignorant', 'charged', 'addicted', 'overt', 'snobbish', 'irrepressible']
post_insults = ['slattern', 'grox fucker', 'turkey', 'whoreson', 'fat cat', 'brigand', 'illiterate', 'cunt', 'whore']

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
            return f"oi {get_insult('short form')}, too many dice rolled versus dice options"
    #roll dice, handle discrete and addition case as well
    while i <= params.dice_no:
        roll = random.randint(1, params.dice_size) 
        if params.is_distinct and (roll + params.addition_arg) not in rolls:  
            rolls.append(roll + params.addition_arg)
            i += 1
        if not params.is_distinct:
            i += 1
            rolls.append(roll + params.addition_arg)   
    rolls.sort()
    return rolls
                    
async def format_dice_args(ctx, args):  
    global addition_arg
    global is_distinct
    global dice_size
    global dice_no

    is_distinct = False
    addition_arg = 0
    dice_no = 1
    dice_size = 1
    match = re.search('^\d{0,2}d\d{1,2}$', args[0])
    dice_args = args[0].split("d")
    if match:
        dice_no = int(dice_args[0] or 1)
        dice_size = int(dice_args[1])     
    else: 
        await ctx.reply(f"give me a good format you {get_insult('long form')}, something like !roll 1d6 or !roll d6")
        raise error("wrong dice format used")

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

def get_insult(arg):
    if arg == "long form":
        insult = f"{pre_insults[random.randint(0, len(pre_insults)-1)]} {post_insults[random.randint(0, len(post_insults)-1)]}"
    else:
        insult = f"{post_insults[random.randint(0, len(post_insults)-1)]}"
    return insult

