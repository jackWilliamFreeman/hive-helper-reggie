import random
from treasure import get_treasure_json
from insult_logic import get_insult

def get_treasure_result(user, is_smashed):
    treasures = get_treasure_json()
    moderator = 0
    single_roll = 0
    if is_smashed:
        single_roll = random.randint(1,3) - moderator
    else:
        single_roll = random.randint(1,6)
    ten_roll = random.randint(1,6) * 10
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