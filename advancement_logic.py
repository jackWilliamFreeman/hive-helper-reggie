from asyncio.windows_events import NULL


class advancement_details:
    def __init__(self, details, roll_required = None, low_text= None, high_text= None):
        self.details = details
        self.roll_required = roll_required or False
        self.low_text = low_text or False
        self.high_text = high_text or False

def get_advancement_other(roll):
    advancements = {
        2:advancement_details('Random Secondary Skill!'),
        3:advancement_details('Random Primary Skill!'),
        4:advancement_details('Characteristic Increase', True, '+1 Wound', '+1 Attack'),
        5:advancement_details('Characteristic Increase', True, '+1 Strength', '+1 Toughness'),
        6:advancement_details('Characteristic Increase', True, '+1 Leadership', '+1 Cool'),
        7:advancement_details('Characteristic Increase', True, '+1 Weapon Skill', '+1 Ballistic Skill'),
        8:advancement_details('Characteristic Increase', True, '+1 Willpower', '+1 Intelligence'),
        9:advancement_details('Characteristic Increase', True, '+1 Movement', '+1 Initiative'),
        10:advancement_details('Custom Primary Skill'),
        11:advancement_details('Random Primary Skill'),
        12:advancement_details('Promotion')
    }
    return advancements[roll]

def get_advancement_ganger(roll):
    advancements = {
        2:advancement_details('Become a Specialist!'),
        3:advancement_details('Characteristic Increase', True, '+1 Weapon Skill', '+1 Ballistic Skill'),
        4:advancement_details('Characteristic Increase', True, '+1 Weapon Skill', '+1 Ballistic Skill'),
        5:advancement_details('Characteristic Increase', True, '+1 Strength', '+1 Toughness'),
        6:advancement_details('Characteristic Increase', True, '+1 Strength', '+1 Toughness'),
        7:advancement_details('Characteristic Increase', True, '+1 Movement', '+1 Initiative'),
        8:advancement_details('Characteristic Increase', True, '+1 Willpower', '+1 Intelligence'),
        9:advancement_details('Characteristic Increase', True, '+1 Willpower', '+1 Intelligence'),
        10:advancement_details('Characteristic Increase', True, '+1 Leadership', '+1 Cool'),
        11:advancement_details('Characteristic Increase', True, '+1 Leadership', '+1 Cool'),
        12:advancement_details('Become a Specialist!')
    }
    return advancements[roll]

def get_advancement_text(roll, is_ganger):
    if is_ganger:
        advancement = get_advancement_ganger(roll)
    else:
        advancement = get_advancement_other(roll)
    if advancement.roll_required:
        text = f'Congrats you rolled {roll}, your ganger got a {advancement.details}, roll a dice and on 1-3 you get {advancement.low_text} and one a 4-6 you get {advancement.high_text}\
            \r\nHowever you can spend XP to change this result if needs be. Consult me handy table above to see whats possible.'
    else:
        text = f'Congrats you rolled {roll}, your ganger got a {advancement.details}\
            \r\nHowever you can spend XP to change this result if needs be. Consult me handy table above to see whats possible.'
    return text

def get_advancement_table_text(is_ganger):
    if is_ganger:
        return f"`+-------+-------------------------------------------+\
    \r\n| Roll  | Advancement                               |\
    \r\n+-------+-------------------------------------------+\
    \r\n| 2     | Ganger Becomes a Specialist               |\
    \r\n+-------+-------------------------------------------+\
    \r\n| 3 - 4 | Characteristic: WS or BS                  |\
    \r\n+-------+-------------------------------------------+\
    \r\n| 5 - 6 | Characteristic: Strength or toughness     |\
    \r\n+-------+-------------------------------------------+\
    \r\n| 7     | Characteristic: Movement or Initiative    |\
    \r\n+-------+-------------------------------------------+\
    \r\n| 8 - 9 | Characteristic: Willpower or Intelligence |\
    \r\n+-------+-------------------------------------------+\
    \r\n|10 - 11| Characteristic: Leadership or Cool        |\
    \r\n+-------+-------------------------------------------+\
    \r\n| 12    | Ganger Becomes a Specialist               |\
    \r\n+-------+-------------------------------------------+`"
    else:
        return f"`+------+-------------------------------------------+\
    \r\n| Roll | Advancement                               |\
    \r\n+------+-------------------------------------------+\
    \r\n| 2    | Gain Random Secondary Skill               |\
    \r\n+------+-------------------------------------------+\
    \r\n| 3    | Gain Random Primary Skill                 |\
    \r\n+------+-------------------------------------------+\
    \r\n| 4    | Characteristic: Wound or Attack           |\
    \r\n+------+-------------------------------------------+\
    \r\n| 5    | Characteristic: Strength or toughness     |\
    \r\n+------+-------------------------------------------+\
    \r\n| 6    | Characteristic: Leadership or Cool        |\
    \r\n+------+-------------------------------------------+\
    \r\n| 7    | Characteristic: WS or BS                  |\
    \r\n+------+-------------------------------------------+\
    \r\n| 8    | Characteristic: Willpower or Intelligence |\
    \r\n+------+-------------------------------------------+\
    \r\n| 9    | Characteristic: Movement or Initiative    |\
    \r\n+------+-------------------------------------------+\
    \r\n| 10   | Gain a Custom Primary Skill               |\
    \r\n+------+-------------------------------------------+\
    \r\n| 11   | Gain a Random Secondary Skill             |\
    \r\n+------+-------------------------------------------+\
    \r\n| 12   | Promotion!                                |\
    \r\n+------+-------------------------------------------+`"