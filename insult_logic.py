from distutils.log import error
import random
import re
from numpy import true_divide
import pandas as pd
import os
from treasure import get_treasure_json
    
insult_predicate = ['moronic', 'obtuse', 'inane', 'rotund', 'fat', 'surly', 'ignorant', 'charged', 'addicted', 'overt', 'snobbish', 'irrepressible', 'hideous', 'blasphemous','spiteful','churlish','round-headed','purile', 'turgid', 'flappable', 'up-hive', 'impulsive', 'goat-faced', 'inbred']
insults = ['slattern', 'grox fucker', 'turkey', 'whoreson', 'fat cat', 'brigand', 'illiterate', 'cunt', 'whore','lummox','cad','heretic','simpleton','moron','catamite','fatso','virgin','nerd','grognard', 'swine', 'cockroach', 'mutton', 'plebian', 'fucker', 'shithead', 'imbecile']

def get_insult(arg):
    if arg == "long form":
        insult = f"{insult_predicate[random.randint(0, len(insult_predicate)-1)]} {insults[random.randint(0, len(insults)-1)]}"
    else:
        insult = f"{insults[random.randint(0, len(insults)-1)]}"
    return insult
         


