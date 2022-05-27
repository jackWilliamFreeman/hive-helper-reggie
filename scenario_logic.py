import os
import random
from tracemalloc import is_tracing
from insult_logic import get_insult
import pandas as pd

class scenario_results:
    def __init__(self, scenario_name, gang_size, comment):
        self.scenario_name = scenario_name
        self.gang_size = gang_size
        self.comment = comment

global localstring
KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if KEY:
    localstring=''
else:
    localstring = 'assets/'

def get_scenario(args):

    user1 = args[0]
    user2 = args[1]
    raider_choice  = args[2]

    if raider_choice == "raider":
        raider_choice = True
    else: raider_choice = False
    
    badlands_scenario = get_badlands_scenario()
    scenario = get_main_scenario_details(raider_choice)
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


async def get_new_scenario(args, ctx):
    user1 = args[0]
    user2 = args[1]

    user1_dice_roll = random.randint(1,40000)
    user2_dice_roll = random.randint(1,40000)
    if user1_dice_roll > user2_dice_roll:
        attacker = user1  
    else: 
        attacker = user2
    await ctx.reply(f"Lets roll some D 40,000's to determine attacker etc\r\nSo it it turns out **{user1}** rolled **{user1_dice_roll}** and **{user2}** rolled **{user2_dice_roll}**, ergo **{attacker}** is the **attacker** this time")

    badlands_scenario = get_badlands_scenario()
    scenario = get_new_scenario_details()
    gang_sizes = get_gang_sizes(scenario)

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
    {gang_sizes}\r\n\
    {equipment_text}"

    return return_text

def get_gang_sizes(scenario):
    gang_sizes = scenario.gang_size
    gang_size_text = ''

    if gang_sizes == 'Random 7':
        gang_size_text = "You both get randomn 7 gangers"
    if gang_sizes == 'Custom d3+6':
        attacker =  random.randint(1,3) + 6
        defender =  random.randint(1,3) + 6
        gang_size_text = f"**Attacker** gets **{attacker} Gangers** for this matchup, **Defender** gets **{defender} Gangers**. Emperor be with ye!"
    if gang_sizes == 'Attacker: custom D3+6, Defender: Random 5 (sentries) + reinforcements':
        attacker =  random.randint(1,3) + 6
        defender =  '5 randomn'
        gang_size_text = f"**Attacker** gets **{attacker} Gangers** for this matchup, **Defender** gets **{defender} Gangers and some reinforcements or whatever**. Emperor be with ye!"
    if gang_sizes == 'Attacker: custom D3+6, Defender: Random 5 (sentries) + reinforcements':
        attacker =  random.randint(1,3) + 6
        defender =  '5 randomn'
        gang_size_text = f"**Attacker** gets **{attacker} Gangers** for this matchup, **Defender** gets **{defender} Sentries and some reinforcements or whatever**. Emperor be with ye!"
    if gang_sizes == 'Attacker: custom D3+6, Defender: Random D3+6 ':
        attacker =  random.randint(1,3) + 6
        defender =  random.randint(1,3) + 6
        gang_size_text = f"**Attacker** gets **{attacker} Gangers** for this matchup, **Defender** gets **{defender} Gangers**. Emperor be with ye!"
    if gang_sizes == 'Attacker: custom D3+6, Defender: Random 6 (plus reinforcers)':
        attacker =  random.randint(1,3) + 6
        defender =  random.randint(1,3) + 6
        gang_size_text = f"**Attacker** gets **{attacker} Gangers** for this matchup, **Defender** gets **{defender} Gangers** plus some reinforcements or some BS. Emperor be with ye!"
    if not gang_sizes:
        gang_size_text = f"Depends on the scenario chosen boyo"
        scenario.gang_size = 'Depends on the scenario'
    return gang_size_text
    #gang_size_text = f"congrats {user1} you get: **{user1_calc_gang_size} gangers**, congrats {user2} you get **{user2_calc_gang_size} gangers**\r\n\r\n"

def get_new_scenario_details():
    scenario_dice_roll = random.randint(2,12)
    global scenarios
    scenarios = pd.read_csv(f'{localstring}new_scenarios.csv', header=0)
    scenario_randomn = random.randint(1,6)
    scenario_subchoice = ''
    if scenario_randomn >= 4:
        scenario_subchoice = 'secondary'
    else:
        scenario_subchoice = 'primary'
    
    rolled_scenario = scenarios[scenarios.roll.eq(scenario_dice_roll)]
    if rolled_scenario.has_multi.iloc[0] == 0:
        scenario_subchoice = 'none'
    
    if scenario_subchoice == 'primary':
        scenario_name= rolled_scenario.primary.iloc[0]
        gang_size_text = rolled_scenario.selectionprimary.iloc[0]
        comment = rolled_scenario.dialogueprimary.iloc[0]
    if scenario_subchoice == 'secondary':
        scenario_name= rolled_scenario.secondary.iloc[0]
        gang_size_text = rolled_scenario.selectionsecondary.iloc[0]
        comment = rolled_scenario.dialoguesecondary.iloc[0]
    if scenario_subchoice == 'none':
        scenario_name= rolled_scenario.primary.iloc[0]        
        gang_size_text = 'Depends on Scenario'
        comment = rolled_scenario.dialogueprimary.iloc[0]

    scenario_details = scenario_results(scenario_name, gang_size_text, comment)
    return scenario_details