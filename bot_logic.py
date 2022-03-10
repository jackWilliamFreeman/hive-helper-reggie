from distutils.log import error
import random
import re
import pandas as pd
import os
from treasure import get_treasure_json


class dice_params:
    def __init__(self, addition_arg, is_distinct, dice_size, dice_no):
        self.addition_arg = addition_arg
        self.is_distinct = is_distinct
        self.dice_size = dice_size
        self.dice_no = dice_no

class scenario_results:
    def __init__(self, scenario_name, gang_size, comment):
        self.scenario_name = scenario_name
        self.gang_size = gang_size
        self.comment = comment
    
insult_predicate = ['moronic', 'obtuse', 'inane', 'rotund', 'fat', 'surly', 'ignorant', 'charged', 'addicted', 'overt', 'snobbish', 'irrepressible', 'hideous', 'blasphemous','spiteful','churlish','round-headed','purile', 'turgid', 'flappable', 'up-hive', 'impulsive', 'goat-faced', 'inbred']
insults = ['slattern', 'grox fucker', 'turkey', 'whoreson', 'fat cat', 'brigand', 'illiterate', 'cunt', 'whore','lummox','cad','heretic','simpleton','moron','catamite','fatso','virgin','nerd','grognard', 'swine', 'cockroach', 'mutton', 'plebian', 'fucker', 'shithead', 'imbecile']

global localstring
KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if KEY:
    localstring=''
else:
    localstring = 'assets/'


def get_insult(arg):
    if arg == "long form":
        insult = f"{insult_predicate[random.randint(0, len(insult_predicate)-1)]} {insults[random.randint(0, len(insults)-1)]}"
    else:
        insult = f"{insults[random.randint(0, len(insults)-1)]}"
    return insult

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

def get_scenario(user1, user2, is_raider):
    
    badlands_scenario = get_badlands_scenario()
    scenario = get_main_scenario_details(is_raider)
    gang_size_text = get_gang_size_text(user1, user2, scenario)
    equipment_text = ''

    if scenario.scenario_name == "Big Score":
        house_equip_text, standard_equip_text, settlement_defence_text = get_trap_text()
        equipment_text = f'You also get to deal with these babies: \r\n\
            **{house_equip_text}**\r\n\
            **{standard_equip_text}**\r\n\
            **{settlement_defence_text}**'

    return_text = f"YO LISTEN UP YOU MANGY DOGS: we got ourselves a battle now between {user1} and {user2}\r\n\r\n\
    Now i always thought {user1} was a {get_insult('short form')} and {user2} was a {get_insult('short form')} but we got to lay some ground rules \r\n\r\n\
    The scenario do be: **{scenario.scenario_name}**... {scenario.comment} \r\n\r\n\
    Now we be rolling in the badlands so make sure to beware of the event: **{badlands_scenario}**\r\n\r\n\
    The gang rules are: **{scenario.gang_size}**\r\n\r\n\
    {gang_size_text}\
    {equipment_text}"
    
    return return_text

def get_trap_text():
    items = pd.read_csv(f'{localstring}traps_gear.csv', header=0)
    house_equip_text = get_house_equipment(items)
    standard_equip_text = get_standard_equipment(items, 'Standard traps')
    settlement_defence_text = get_standard_equipment(items, 'Settlement defence')
    return house_equip_text,standard_equip_text,settlement_defence_text

def get_standard_equipment(items, arg):
    dice_roll = random.randint(1,6)
    house_gear_list = items.loc[(items['dice_roll']==dice_roll) & (items['theme']==arg)]
    text = f"{house_gear_list.description.values.tolist()[0]}"
    return text
    
def get_house_equipment(items):
    dice_roll = random.randint(1,8)
    house_gear_list = items.loc[(items['dice_roll']==dice_roll) & (items['theme']=='house trap')]
    if house_gear_list.roll_dice.values.tolist()[0] == 1:
        dice_size = house_gear_list.param.values.tolist()[0]
        roll = random.randint(1, dice_size)
        text = f"{int(roll)} x {house_gear_list.description.values.tolist()[0]}"
    else:
        text = f"{int(house_gear_list.param.values.tolist()[0])} x {house_gear_list.description.values.tolist()[0]}"
    return text

def get_gang_size_text(user1, user2, scenario):
    gang_size_text = ""
    if scenario.gang_size == "Choose d3+6 Gangers":
        user1_calc_gang_size = random.randint(1,3)+6
        user2_calc_gang_size = random.randint(1,3)+6
        gang_size_text = f"congrats {user1} you get: **{user1_calc_gang_size} gangers**, congrats {user2} you get **{user2_calc_gang_size} gangers**\r\n\r\n"
    return gang_size_text


def get_main_scenario_details(is_raider):
    scenario_dice_roll = random.randint(2,12)
    global scenarios
    if is_raider:
        scenarios = pd.read_csv(f'{localstring}raider_scenarios.csv', header=0)
    else: scenarios = pd.read_csv(f'{localstring}settlement_scenarios.csv', header=0)
   
    rolled_scenario = scenarios[scenarios.roll.eq(scenario_dice_roll)]
    scenario_name= rolled_scenario.scenario.iloc[0]
    gang_size_text = rolled_scenario.gang_size.iloc[0]
    comment = rolled_scenario.comment.iloc[0]

    scenario_details = scenario_results(scenario_name, gang_size_text, comment)
    return scenario_details


def get_badlands_scenario():
    badlands_dice_roll = (random.randint(1,6)*10)+random.randint(1,6)
    badlands_scenarios = pd.read_csv(f'{localstring}badland_events.csv', header=0, index_col=0,squeeze=True).to_dict()
    rolled_badlands_scenario = badlands_scenarios[badlands_dice_roll]
    return rolled_badlands_scenario

                    
async def format_dice_params(ctx, args):  
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
        await ctx.reply(f"give me a good format you {get_insult('long form')}, something like !roll 1d6 or !roll d6, max 2 digits so 1-99")
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

def get_treasure_result(user, is_smashed):
    treasures = get_treasure_json()
    moderator = 0
    if is_smashed:
        moderator = 3
    ten_roll = random.randint(1,6) * 10
    single_roll = random.randint(1,6) - moderator
    if single_roll <= 0 :
        single_roll = 1
    d66 = ten_roll + single_roll
    text = ''    
    description = ''
    short_description = False
    dice_text = ''
    result = ''
    for treasure in treasures:
        if treasure['primary'] == d66 and treasure['inner_treasure_roll'] == True:
            description = treasure['description']
            dice_size = treasure['dice_size']
            inner_d6 = random.randint(1,dice_size) 
            inner_inner_d6 = random.randint(1,dice_size) 
            results = treasure['treasure']
            rolled_result = results[(inner_d6 - 1)]
            final_result = rolled_result[str(inner_d6)][(inner_inner_d6 - 1)]
            result = final_result
            dice_text = f'your rolled a **{inner_d6}** followed by a **{inner_inner_d6}**'

        if treasure['primary'] == d66 and treasure['inner_treasure_roll'] == False:
            description = treasure['description']
            if treasure['tertiary_roll']:
                dice_size = treasure['dice_size']
                inner_d6 = random.randint(1,dice_size)
                results = treasure['treasure']
                rolled_result = results[(inner_d6 - 1)]
                rolled_description = rolled_result[str(inner_d6)]             
                if "d3" in description.lower():
                    d3 = random.randint(1,3)
                    rolled_description = f'{rolled_description} X {d3}'
                result = rolled_description 
                dice_text = f'you rolled a **{inner_d6}**'

            else:
                result = treasure['description']
                short_description = True
    
    if short_description:
        text = f"Lets roll some dice before i reach into my magic loincloth of mystery!\r\n\
        \r\nWell you first up rolled a **{d66}**...interesting, that means you win: **{description}**\r\n\
        \r\nEnjoy it {user} you {get_insult('long form')}!"
    else:
        text = f"Lets roll some dice before i reach into my magic loincloth of mystery!\r\n\
        \r\nWell you first up rolled a **{d66}**...interesting, that means you win: **{description}**\r\n\
        \r\nYou then rolled a {dice_text}\r\n\
        \r\nFor that roll you get: **{result}**\r\n\
        \r\nDo you like that {user}, you {get_insult('long form')}!? Well do ya?"

    return text

