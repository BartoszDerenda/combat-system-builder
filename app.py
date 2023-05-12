from flask import Flask
from flask import render_template
from flask import request
from flask import session
import math
import random
import uuid

app = Flask(__name__)
app.secret_key = '8008135'

sessions = {}


class Fighter:
    def __init__(self, token):
        if token == 'Hero':
            self.name = 'Hero'
        else:
            self.name = 'Enemy'

        # Attributes
        self.level = 1
        self.strength = 1
        self.intelligence = 1
        self.agility = 1
        self.willpower = 1
        self.endurance = 1
        self.charisma = 1
        self.luck = 1
        self.speed = 1
        self.armor = 1
        self.likelihood_of_physical = 50
        self.likelihood_of_magical = 50
        self.total_value = 0

        # Skills and Spells
        self.attack_1_type = "physical"
        self.attack_1_name = "Slam"
        self.attack_1_min = 1.0
        self.attack_1_max = 1.2
        self.attack_1_chance = 50

        self.attack_2_type = "physical"
        self.attack_2_name = "Shield Bash"
        self.attack_2_min = 0.9
        self.attack_2_max = 1.3
        self.attack_2_chance = 50

        self.attack_3_type = "magical"
        self.attack_3_name = "Fireball"
        self.attack_3_min = 0.9
        self.attack_3_max = 1.3
        self.attack_3_chance = 50

        self.attack_4_type = "magical"
        self.attack_4_name = "Arcane Blast"
        self.attack_4_min = 0.5
        self.attack_4_max = 1.5
        self.attack_4_chance = 50

        # Summary
        self.physical_damage = 0
        self.magical_damage = 0
        self.dodge_chance = 0
        self.resistance = 0
        self.hitpoints = 0
        self.charisma_chance = 0
        self.critical_chance = 0
        self.armor_mitigation = 0


class System:
    def __init__(self):
        self.hero = Fighter('Hero')
        self.enemy = Fighter('Enemy')

        self.strength_dmg = 3
        self.strength_min = 0.9
        self.strength_max = 1.1
        self.strength_crit = 1.5
        self.strength_price = 2

        self.intelligence_dmg = 4
        self.intelligence_min = 0.8
        self.intelligence_max = 1.2
        self.intelligence_crit = 1.5
        self.intelligence_price = 2

        self.agility_type = "physical"
        self.agility_math = 1
        self.agility_x = "strength"
        self.agility_y = 3.0
        self.agility_cap = 33
        self.agility_price = 1

        self.willpower_type = "magical"
        self.willpower_math = 1
        self.willpower_x = "intelligence"
        self.willpower_y = 2.0
        self.willpower_cap = 50
        self.willpower_price = 1

        self.base_health = 200
        self.endurance_value = 10
        self.endurance_price = 3

        self.charisma_math = 1
        self.charisma_x = "level"
        self.charisma_y = 3.0
        self.charisma_min = 15
        self.charisma_max = 35
        self.charisma_cap = 33
        self.charisma_price = 1

        self.luck_math = 1
        self.luck_x = "level"
        self.luck_y = 2.0
        self.luck_cap = 50
        self.luck_price = 1

        self.speed_price = 3

        self.armor_type = "physical and magical"
        self.armor_math = 1
        self.armor_y = 100.0
        self.armor_cap = 75
        self.armor_price = 2


def math_type_chooser(attribute_x):
    system = sessions[session['key']]
    if attribute_x == "level":
        x = system.enemy.level
    elif attribute_x == "strength":
        x = system.enemy.strength
    elif attribute_x == "intelligence":
        x = system.enemy.intelligence
    elif attribute_x == "agility":
        x = system.enemy.agility
    elif attribute_x == "willpower":
        x = system.enemy.willpower
    elif attribute_x == "endurance":
        x = system.enemy.endurance
    elif attribute_x == "charisma":
        x = system.enemy.charisma
    elif attribute_x == "luck":
        x = system.enemy.luck
    elif attribute_x == "speed":
        x = system.enemy.speed
    elif attribute_x == "armor":
        x = system.enemy.armor
    else:
        x = system.enemy.level
    return x


def attribute_calculator(attribute, attribute_math, attribute_x, attribute_y):
    if attribute_math == 1:
        effect_chance = round(
            ((attribute / (math_type_chooser(attribute_x) * attribute_y)) * 100), 1)
    elif attribute_math == 2:
        effect_chance = round(
            ((attribute / (attribute + attribute_y)) * 100), 1)
    elif attribute_math == 3:
        effect_chance = round(
            ((attribute - math_type_chooser(attribute_x)) * attribute_y), 1)
    elif attribute_math == 4:
        effect_chance = round(
            (math.log(attribute, attribute_y) * 10), 1)
    elif attribute_math == 5:
        effect_chance = round(attribute / attribute_y)
    else:
        effect_chance = 0

    return effect_chance


def armor_calculator(attribute, attribute_math, attribute_y):
    if attribute_math == 1:
        armor_mitigation = round(
            ((attribute / (attribute + attribute_y)) * 100), 1)
    elif attribute_math == 2:
        armor_mitigation = round(
            (math.log(attribute, attribute_y) * 10), 1)
    elif attribute_math == 3:
        armor_mitigation = round(attribute / attribute_y)
    elif attribute_math == 4:
        armor_mitigation = attribute
    else:
        armor_mitigation = 0

    return armor_mitigation


def set_stats():
    system = sessions[session['key']]

    # Hero statistics
    if request.form.get("hero_name") != '':
        system.hero.name = str(request.form.get("hero_name"))
    else:
        system.hero.name = 'Hero'

    if request.form.get("hero_lvl") != '' and int(request.form.get("hero_lvl")) > 0:
        system.hero.level = int(request.form.get("hero_lvl"))
    else:
        system.hero.level = 1

    if request.form.get("hero_str") != '' and int(request.form.get("hero_str")) > 0:
        system.hero.strength = int(request.form.get("hero_str"))
    else:
        system.hero.strength = 1

    if request.form.get("hero_int") != '' and int(request.form.get("hero_int")) > 0:
        system.hero.intelligence = int(request.form.get("hero_int"))
    else:
        system.hero.intelligence = 1

    if request.form.get("hero_agi") != '' and int(request.form.get("hero_agi")) > 0:
        system.hero.agility = int(request.form.get("hero_agi"))
    else:
        system.hero.agility = 0

    if request.form.get("hero_will") != '' and int(request.form.get("hero_will")) > 0:
        system.hero.willpower = int(request.form.get("hero_will"))
    else:
        system.hero.willpower = 0

    if request.form.get("hero_end") != '' and int(request.form.get("hero_end")) > 0:
        system.hero.endurance = int(request.form.get("hero_end"))
    else:
        system.hero.endurance = 1

    if request.form.get("hero_char") != '' and int(request.form.get("hero_char")) > 0:
        system.hero.charisma = int(request.form.get("hero_char"))
    else:
        system.hero.charisma = 0

    if request.form.get("hero_lck") != '' and int(request.form.get("hero_lck")) > 0:
        system.hero.luck = int(request.form.get("hero_lck"))
    else:
        system.hero.luck = 0

    if request.form.get("hero_spd") != '' and int(request.form.get("hero_spd")) > 0:
        system.hero.speed = int(request.form.get("hero_spd"))
    else:
        system.hero.speed = 1

    if request.form.get("hero_armor") != '' and int(request.form.get("hero_armor")) > 0:
        system.hero.armor = int(request.form.get("hero_armor"))
    else:
        system.hero.armor = 0

    if request.form.get("hero_likelihood_of_physical") != '' and int(
            request.form.get("hero_likelihood_of_physical")) >= 0:
        system.hero.likelihood_of_physical = int(request.form.get("hero_likelihood_of_physical"))
    else:
        system.hero.likelihood_of_physical = 50

    if request.form.get("hero_likelihood_of_magical") != '' and int(
            request.form.get("hero_likelihood_of_magical")) >= 0:
        system.hero.likelihood_of_magical = int(request.form.get("hero_likelihood_of_magical"))
    else:
        system.hero.likelihood_of_magical = 50

    if request.form.get("hero_attack_1_type") != '':
        system.hero.attack_1_type = str(request.form.get("hero_attack_1_type"))
    else:
        system.hero.attack_1_type = "physical"

    if request.form.get("hero_attack_1_name") != '':
        system.hero.attack_1_name = str(request.form.get("hero_attack_1_name"))
    else:
        system.hero.attack_1_name = "Default Attack"

    if request.form.get("hero_attack_1_min") != '' and float(request.form.get("hero_attack_1_min")) >= 0.1:
        system.hero.attack_1_min = float(request.form.get("hero_attack_1_min"))
    else:
        system.hero.attack_1_min = 0.1

    if request.form.get("hero_attack_1_max") != '' and float(request.form.get("hero_attack_1_max")) >= 0.2:
        system.hero.attack_1_max = float(request.form.get("hero_attack_1_max"))
    else:
        system.hero.attack_1_max = 0.2

    if request.form.get("hero_attack_1_chance") != '' and int(request.form.get("hero_attack_1_chance")) >= 0:
        system.hero.attack_1_chance = int(request.form.get("hero_attack_1_chance"))
    else:
        system.hero.attack_1_chance = 50

    if request.form.get("hero_attack_2_type") != '':
        system.hero.attack_2_type = str(request.form.get("hero_attack_2_type"))
    else:
        system.hero.attack_2_type = "physical"

    if request.form.get("hero_attack_2_name") != '':
        system.hero.attack_2_name = str(request.form.get("hero_attack_2_name"))
    else:
        system.hero.attack_2_name = "Default Attack"

    if request.form.get("hero_attack_2_min") != '' and float(request.form.get("hero_attack_2_min")) >= 0.1:
        system.hero.attack_2_min = float(request.form.get("hero_attack_2_min"))
    else:
        system.hero.attack_2_min = 0.1

    if request.form.get("hero_attack_2_max") != '' and float(request.form.get("hero_attack_2_max")) >= 0.2:
        system.hero.attack_2_max = float(request.form.get("hero_attack_2_max"))
    else:
        system.hero.attack_2_max = 0.2

    if request.form.get("hero_attack_2_chance") != '' and int(request.form.get("hero_attack_2_chance")) >= 0:
        system.hero.attack_2_chance = int(request.form.get("hero_attack_2_chance"))
    else:
        system.hero.attack_2_chance = 50

    if request.form.get("hero_attack_3_type") != '':
        system.hero.attack_3_type = str(request.form.get("hero_attack_3_type"))
    else:
        system.hero.attack_3_type = "magical"

    if request.form.get("hero_attack_3_name") != '':
        system.hero.attack_3_name = str(request.form.get("hero_attack_3_name"))
    else:
        system.hero.attack_3_name = "Default Attack"

    if request.form.get("hero_attack_3_min") != '' and float(request.form.get("hero_attack_3_min")) >= 0.1:
        system.hero.attack_3_min = float(request.form.get("hero_attack_3_min"))
    else:
        system.hero.attack_3_min = 0.1

    if request.form.get("hero_attack_3_max") != '' and float(request.form.get("hero_attack_3_max")) >= 0.2:
        system.hero.attack_3_max = float(request.form.get("hero_attack_3_max"))
    else:
        system.hero.attack_3_max = 0.2

    if request.form.get("hero_attack_3_chance") != '' and int(request.form.get("hero_attack_3_chance")) >= 0:
        system.hero.attack_3_chance = int(request.form.get("hero_attack_3_chance"))
    else:
        system.hero.attack_3_chance = 50

    if request.form.get("hero_attack_4_type") != '':
        system.hero.attack_4_type = str(request.form.get("hero_attack_4_type"))
    else:
        system.hero.attack_4_type = "magical"

    if request.form.get("hero_attack_4_name") != '':
        system.hero.attack_4_name = str(request.form.get("hero_attack_4_name"))
    else:
        system.hero.attack_4_name = "Default Attack"

    if request.form.get("hero_attack_4_min") != '' and float(request.form.get("hero_attack_4_min")) >= 0.1:
        system.hero.attack_4_min = float(request.form.get("hero_attack_4_min"))
    else:
        system.hero.attack_4_min = 0.1

    if request.form.get("hero_attack_4_max") != '' and float(request.form.get("hero_attack_4_max")) >= 0.2:
        system.hero.attack_4_max = float(request.form.get("hero_attack_4_max"))
    else:
        system.hero.attack_4_max = 0.2

    if request.form.get("hero_attack_4_chance") != '' and int(request.form.get("hero_attack_4_chance")) >= 0:
        system.hero.attack_4_chance = int(request.form.get("hero_attack_4_chance"))
    else:
        system.hero.attack_4_chance = 50

    system.hero.total_value = \
        system.strength_price * system.hero.strength + \
        system.intelligence_price * system.hero.intelligence + \
        system.agility_price * system.hero.agility + \
        system.willpower_price * system.hero.willpower + \
        system.endurance_price * system.hero.endurance + \
        system.charisma_price * system.hero.charisma + \
        system.luck_price * system.hero.luck + \
        system.speed_price * system.hero.speed + \
        system.armor_price * system.hero.armor

    # Enemy statistics
    if request.form.get("enemy_name") != '':
        system.enemy.name = str(request.form.get("enemy_name"))
    else:
        system.enemy.name = 'Enemy'

    if request.form.get("enemy_lvl") != '' and int(request.form.get("enemy_lvl")) > 0:
        system.enemy.level = int(request.form.get("enemy_lvl"))
    else:
        system.enemy.level = 1

    if request.form.get("enemy_str") != '' and int(request.form.get("enemy_str")) > 0:
        system.enemy.strength = int(request.form.get("enemy_str"))
    else:
        system.enemy.strength = 1

    if request.form.get("enemy_int") != '' and int(request.form.get("enemy_int")) > 0:
        system.enemy.intelligence = int(request.form.get("enemy_int"))
    else:
        system.enemy.intelligence = 1

    if request.form.get("enemy_agi") != '' and int(request.form.get("enemy_agi")) > 0:
        system.enemy.agility = int(request.form.get("enemy_agi"))
    else:
        system.enemy.agility = 0

    if request.form.get("enemy_will") != '' and int(request.form.get("enemy_will")) > 0:
        system.enemy.willpower = int(request.form.get("enemy_will"))
    else:
        system.enemy.willpower = 0

    if request.form.get("enemy_end") != '' and int(request.form.get("enemy_end")) > 0:
        system.enemy.endurance = int(request.form.get("enemy_end"))
    else:
        system.enemy.endurance = 1

    if request.form.get("enemy_char") != '' and int(request.form.get("enemy_char")) > 0:
        system.enemy.charisma = int(request.form.get("enemy_char"))
    else:
        system.enemy.charisma = 0

    if request.form.get("enemy_lck") != '' and int(request.form.get("enemy_lck")) > 0:
        system.enemy.luck = int(request.form.get("enemy_lck"))
    else:
        system.enemy.luck = 0

    if request.form.get("enemy_spd") != '' and int(request.form.get("enemy_spd")) > 0:
        system.enemy.speed = int(request.form.get("enemy_spd"))
    else:
        system.enemy.speed = 1

    if request.form.get("enemy_armor") != '' and int(request.form.get("enemy_armor")) > 0:
        system.enemy.armor = int(request.form.get("enemy_armor"))
    else:
        system.enemy.armor = 0

    if request.form.get("enemy_likelihood_of_physical") != '' and int(
            request.form.get("enemy_likelihood_of_physical")) >= 0:
        system.enemy.likelihood_of_physical = int(request.form.get("enemy_likelihood_of_physical"))
    else:
        system.enemy.likelihood_of_physical = 50

    if request.form.get("enemy_likelihood_of_magical") != '' and int(
            request.form.get("enemy_likelihood_of_magical")) >= 0:
        system.enemy.likelihood_of_magical = int(request.form.get("enemy_likelihood_of_magical"))
    else:
        system.enemy.likelihood_of_magical = 50

    if request.form.get("enemy_attack_1_type") != '':
        system.enemy.attack_1_type = str(request.form.get("enemy_attack_1_type"))
    else:
        system.enemy.attack_1_type = "physical"

    if request.form.get("enemy_attack_1_name") != '':
        system.enemy.attack_1_name = str(request.form.get("enemy_attack_1_name"))
    else:
        system.enemy.attack_1_name = "Default Attack"

    if request.form.get("enemy_attack_1_min") != '' and float(request.form.get("enemy_attack_1_min")) >= 0.1:
        system.enemy.attack_1_min = float(request.form.get("enemy_attack_1_min"))
    else:
        system.enemy.attack_1_min = 0.1

    if request.form.get("enemy_attack_1_max") != '' and float(request.form.get("enemy_attack_1_max")) >= 0.2:
        system.enemy.attack_1_max = float(request.form.get("enemy_attack_1_max"))
    else:
        system.enemy.attack_1_max = 0.2

    if request.form.get("enemy_attack_1_chance") != '' and int(request.form.get("enemy_attack_1_chance")) >= 0:
        system.enemy.attack_1_chance = int(request.form.get("enemy_attack_1_chance"))
    else:
        system.enemy.attack_1_chance = 50

    if request.form.get("enemy_attack_2_type") != '':
        system.enemy.attack_2_type = str(request.form.get("enemy_attack_2_type"))
    else:
        system.enemy.attack_2_type = "physical"

    if request.form.get("enemy_attack_2_name") != '':
        system.enemy.attack_2_name = str(request.form.get("enemy_attack_2_name"))
    else:
        system.enemy.attack_2_name = "Default Attack"

    if request.form.get("enemy_attack_2_min") != '' and float(request.form.get("enemy_attack_2_min")) >= 0.1:
        system.enemy.attack_2_min = float(request.form.get("enemy_attack_2_min"))
    else:
        system.enemy.attack_2_min = 0.1

    if request.form.get("enemy_attack_2_max") != '' and float(request.form.get("enemy_attack_2_max")) >= 0.2:
        system.enemy.attack_2_max = float(request.form.get("enemy_attack_2_max"))
    else:
        system.enemy.attack_2_max = 0.2

    if request.form.get("enemy_attack_2_chance") != '' and int(request.form.get("enemy_attack_2_chance")) >= 0:
        system.enemy.attack_2_chance = int(request.form.get("enemy_attack_2_chance"))
    else:
        system.enemy.attack_2_chance = 50

    if request.form.get("enemy_attack_3_type") != '':
        system.enemy.attack_3_type = str(request.form.get("enemy_attack_3_type"))
    else:
        system.enemy.attack_3_type = "magical"

    if request.form.get("enemy_attack_3_name") != '':
        system.enemy.attack_3_name = str(request.form.get("enemy_attack_3_name"))
    else:
        system.enemy.attack_3_name = "Default Attack"

    if request.form.get("enemy_attack_3_min") != '' and float(request.form.get("enemy_attack_3_min")) >= 0.1:
        system.enemy.attack_3_min = float(request.form.get("enemy_attack_3_min"))
    else:
        system.enemy.attack_3_min = 0.1

    if request.form.get("enemy_attack_3_max") != '' and float(request.form.get("enemy_attack_3_max")) >= 0.2:
        system.enemy.attack_3_max = float(request.form.get("enemy_attack_3_max"))
    else:
        system.enemy.attack_3_max = 0.2

    if request.form.get("enemy_attack_3_chance") != '' and int(request.form.get("enemy_attack_3_chance")) >= 0:
        system.enemy.attack_3_chance = int(request.form.get("enemy_attack_3_chance"))
    else:
        system.enemy.attack_3_chance = 50

    if request.form.get("enemy_attack_4_type") != '':
        system.enemy.attack_4_type = str(request.form.get("enemy_attack_4_type"))
    else:
        system.enemy.attack_4_type = "magical"

    if request.form.get("enemy_attack_4_name") != '':
        system.enemy.attack_4_name = str(request.form.get("enemy_attack_4_name"))
    else:
        system.enemy.attack_4_name = "Default Attack"

    if request.form.get("enemy_attack_4_min") != '' and float(request.form.get("enemy_attack_4_min")) >= 0.1:
        system.enemy.attack_4_min = float(request.form.get("enemy_attack_4_min"))
    else:
        system.enemy.attack_4_min = 0.1

    if request.form.get("enemy_attack_4_max") != '' and float(request.form.get("enemy_attack_4_max")) >= 0.2:
        system.enemy.attack_4_max = float(request.form.get("enemy_attack_4_max"))
    else:
        system.enemy.attack_4_max = 0.2

    if request.form.get("enemy_attack_4_chance") != '' and int(request.form.get("enemy_attack_4_chance")) >= 0:
        system.enemy.attack_4_chance = int(request.form.get("enemy_attack_4_chance"))
    else:
        system.enemy.attack_4_chance = 50

    system.enemy.total_value = \
        system.strength_price * system.enemy.strength + \
        system.intelligence_price * system.enemy.intelligence + \
        system.agility_price * system.enemy.agility + \
        system.willpower_price * system.enemy.willpower + \
        system.endurance_price * system.enemy.endurance + \
        system.charisma_price * system.enemy.charisma + \
        system.luck_price * system.enemy.luck + \
        system.speed_price * system.enemy.speed + \
        system.armor_price * system.enemy.armor

    # Hero extras
    system.hero.physical_damage = system.hero.strength * system.strength_dmg
    system.hero.magical_damage = system.hero.intelligence * system.intelligence_dmg

    system.hero.dodge_chance = attribute_calculator(system.hero.agility, system.agility_math, system.agility_x,
                                                    system.agility_y)
    if system.hero.dodge_chance > system.agility_cap:
        system.hero.dodge_chance = system.agility_cap

    system.hero.resistance = attribute_calculator(system.hero.willpower, system.willpower_math, system.willpower_x,
                                                  system.willpower_y)
    if system.hero.resistance > system.willpower_cap:
        system.hero.resistance = system.willpower_cap

    system.hero.hitpoints = system.base_health + (system.hero.endurance * system.endurance_value)

    system.hero.charisma_chance = attribute_calculator(system.hero.charisma, system.charisma_math, system.charisma_x,
                                                       system.charisma_y)
    if system.hero.charisma_chance > system.charisma_cap:
        system.hero.charisma_chance = system.charisma_cap

    system.hero.critical_chance = attribute_calculator(system.hero.luck, system.luck_math, system.luck_x,
                                                       system.luck_y)
    if system.hero.critical_chance > system.luck_cap:
        system.hero.critical_chance = system.luck_cap

    system.hero.armor_mitigation = armor_calculator(system.hero.armor, system.armor_math, system.armor_y)
    if system.armor_math != 4:
        if system.hero.armor_mitigation > system.armor_cap:
            system.hero.armor_mitigation = system.armor_cap

    # Enemy extras
    system.enemy.physical_damage = system.enemy.strength * system.strength_dmg
    system.enemy.magical_damage = system.enemy.intelligence * system.intelligence_dmg

    system.enemy.dodge_chance = attribute_calculator(system.enemy.agility, system.agility_math, system.agility_x,
                                                     system.agility_y)
    if system.enemy.dodge_chance > system.agility_cap:
        system.enemy.dodge_chance = system.agility_cap

    system.enemy.resistance = attribute_calculator(system.enemy.willpower, system.willpower_math, system.willpower_x,
                                                   system.willpower_y)
    if system.enemy.resistance > system.willpower_cap:
        system.enemy.resistance = system.willpower_cap

    system.enemy.hitpoints = system.base_health + (system.enemy.endurance * system.endurance_value)

    system.enemy.charisma_chance = attribute_calculator(system.enemy.charisma, system.charisma_math, system.charisma_x,
                                                        system.charisma_y)
    if system.enemy.charisma_chance > system.charisma_cap:
        system.enemy.charisma_chance = system.charisma_cap

    system.enemy.critical_chance = attribute_calculator(system.enemy.luck, system.luck_math, system.luck_x,
                                                        system.luck_y)
    if system.enemy.critical_chance > system.luck_cap:
        system.enemy.critical_chance = system.luck_cap

    system.enemy.armor_mitigation = armor_calculator(system.enemy.armor, system.armor_math, system.armor_y)
    if system.armor_math != 4:
        if system.enemy.armor_mitigation > system.armor_cap:
            system.enemy.armor_mitigation = system.armor_cap


def set_ruleset():
    system = sessions[session['key']]

    # Setting all the ruleset rules

    #
    # STRENGTH
    #
    if request.form.get("strength_dmg") != '' and int(request.form.get("strength_dmg")) > 0:
        system.strength_dmg = int(request.form.get("strength_dmg"))
    else:
        system.strength_dmg = 3

    if request.form.get("strength_min") != '' and float(request.form.get("strength_min")) >= 0.1:
        system.strength_min = float(request.form.get("strength_min"))
    else:
        system.strength_min = 0.9

    if request.form.get("strength_max") != '' and float(request.form.get("strength_max")) >= 0.1:
        system.strength_max = float(request.form.get("strength_max"))
    else:
        system.strength_max = 1.1

    if system.strength_min > system.strength_max:
        temp = system.strength_min
        system.strength_min = system.strength_max
        system.strength_max = temp

    if request.form.get("strength_crit") != '' and float(request.form.get("strength_crit")) >= 0.1:
        system.strength_crit = float(request.form.get("strength_crit"))
    else:
        system.strength_crit = 1.5

    if request.form.get("strength_price") != '' and int(request.form.get("strength_price")) >= 1:
        system.strength_price = int(request.form.get("strength_price"))
    else:
        system.strength_price = 2

    #
    # INTELLIGENCE
    #
    if request.form.get("intelligence_dmg") != '' and int(request.form.get("intelligence_dmg")) > 0:
        system.intelligence_dmg = int(request.form.get("intelligence_dmg"))
    else:
        system.intelligence_dmg = 3

    if request.form.get("intelligence_min") != '' and float(request.form.get("intelligence_min")) >= 0.1:
        system.intelligence_min = float(request.form.get("intelligence_min"))
    else:
        system.intelligence_min = 0.9

    if request.form.get("intelligence_max") != '' and float(request.form.get("intelligence_max")) >= 0.1:
        system.intelligence_max = float(request.form.get("intelligence_max"))
    else:
        system.intelligence_max = 1.1

    if system.intelligence_min > system.intelligence_max:
        temp = system.intelligence_min
        system.intelligence_min = system.intelligence_max
        system.intelligence_max = temp

    if request.form.get("intelligence_crit") != '' and float(request.form.get("intelligence_crit")) >= 0.1:
        system.intelligence_crit = float(request.form.get("intelligence_crit"))
    else:
        system.intelligence_crit = 1.5

    if request.form.get("intelligence_price") != '' and int(request.form.get("intelligence_price")) >= 1:
        system.intelligence_price = int(request.form.get("intelligence_price"))
    else:
        system.intelligence_price = 2

    #
    # AGILITY
    #
    if request.form.get("agility_type") != '':
        system.agility_type = str(request.form.get("agility_type"))
    else:
        system.agility_type = "physical"

    if request.form.get("agility_math") != '':
        system.agility_math = int(request.form.get("agility_math"))
    else:
        system.agility_math = 1

    if request.form.get("agility_x") != '':
        system.agility_x = str(request.form.get("agility_x"))
    else:
        system.agility_x = "strength"

    if request.form.get("agility_y") != '' and float(request.form.get("agility_y")) >= 0.1:
        system.agility_y = float(request.form.get("agility_y"))
    else:
        system.agility_y = 3.0

    if request.form.get("agility_cap") != '' and int(request.form.get("agility_cap")) > 0:
        system.agility_cap = int(request.form.get("agility_cap"))
    else:
        system.agility_cap = 33

    if request.form.get("agility_price") != '' and int(request.form.get("agility_price")) >= 1:
        system.agility_price = int(request.form.get("agility_price"))
    else:
        system.agility_price = 1

    #
    # WILLPOWER
    #
    if request.form.get("willpower_type") != '':
        system.willpower_type = str(request.form.get("willpower_type"))
    else:
        system.willpower_type = "physical"

    if request.form.get("willpower_math") != '':
        system.willpower_math = int(request.form.get("willpower_math"))
    else:
        system.willpower_math = 1

    if request.form.get("willpower_x") != '':
        system.willpower_x = str(request.form.get("willpower_x"))
    else:
        system.willpower_x = "intelligence"

    if request.form.get("willpower_y") != '' and float(request.form.get("willpower_y")) >= 0.1:
        system.willpower_y = float(request.form.get("willpower_y"))
    else:
        system.willpower_y = 3.0

    if request.form.get("willpower_cap") != '' and int(request.form.get("willpower_cap")) > 0:
        system.willpower_cap = int(request.form.get("willpower_cap"))
    else:
        system.willpower_cap = 50

    if request.form.get("willpower_price") != '' and int(request.form.get("willpower_price")) >= 1:
        system.willpower_price = int(request.form.get("willpower_price"))
    else:
        system.willpower_price = 1

    #
    # ENDURANCE
    #
    if request.form.get("base_health") != '' and int(request.form.get("base_health")) >= 0:
        system.base_health = int(request.form.get("base_health"))
    else:
        system.base_health = 200

    if request.form.get("endurance_value") != '' and int(request.form.get("endurance_value")) >= 1:
        system.endurance_value = int(request.form.get("endurance_value"))
    else:
        system.endurance_value = 10

    if request.form.get("endurance_price") != '' and int(request.form.get("endurance_price")) >= 1:
        system.endurance_price = int(request.form.get("endurance_price"))
    else:
        system.endurance_price = 3

    #
    # CHARISMA
    #
    if request.form.get("charisma_math") != '':
        system.charisma_math = int(request.form.get("charisma_math"))
    else:
        system.charisma_math = 1

    if request.form.get("charisma_x") != '':
        system.charisma_x = str(request.form.get("charisma_x"))
    else:
        system.charisma_x = "level"

    if request.form.get("charisma_y") != '' and float(request.form.get("charisma_y")) >= 0.1:
        system.charisma_y = float(request.form.get("charisma_y"))
    else:
        system.charisma_y = 3.0

    if request.form.get("charisma_min") != '' and int(request.form.get("charisma_min")) >= 1:
        system.charisma_min = int(request.form.get("charisma_min"))
    else:
        system.charisma_min = 15

    if request.form.get("charisma_max") != '' and int(request.form.get("charisma_max")) >= 1:
        system.charisma_max = int(request.form.get("charisma_max"))
    else:
        system.charisma_max = 35

    if system.charisma_min > system.charisma_max:
        temp = system.charisma_min
        system.charisma_min = system.charisma_max
        system.charisma_max = temp

    if request.form.get("charisma_cap") != '' and int(request.form.get("charisma_cap")) > 0:
        system.charisma_cap = int(request.form.get("charisma_cap"))
    else:
        system.charisma_cap = 33

    if request.form.get("charisma_price") != '' and int(request.form.get("charisma_price")) >= 1:
        system.charisma_price = int(request.form.get("charisma_price"))
    else:
        system.charisma_price = 1

    #
    # LUCK
    #
    if request.form.get("luck_math") != '':
        system.luck_math = int(request.form.get("luck_math"))
    else:
        system.luck_math = 1

    if request.form.get("luck_x") != '':
        system.luck_x = str(request.form.get("luck_x"))
    else:
        system.luck_x = "level"

    if request.form.get("luck_y") != '' and float(request.form.get("luck_y")) >= 0.1:
        system.luck_y = float(request.form.get("luck_y"))
    else:
        system.luck_y = 2.0

    if request.form.get("luck_cap") != '' and int(request.form.get("luck_cap")) > 0:
        system.luck_cap = int(request.form.get("luck_cap"))
    else:
        system.luck_cap = 50

    if request.form.get("luck_price") != '' and int(request.form.get("luck_price")) >= 1:
        system.luck_price = int(request.form.get("luck_price"))
    else:
        system.luck_price = 1

    #
    # SPEED
    #
    if request.form.get("speed_price") != '' and int(request.form.get("speed_price")) >= 1:
        system.speed_price = int(request.form.get("speed_price"))
    else:
        system.speed_price = 3

    #
    # ARMOR
    #
    if request.form.get("armor_type") != '':
        system.armor_type = str(request.form.get("armor_type"))
    else:
        system.armor_type = "physical and magical"

    if request.form.get("armor_math") != '':
        system.armor_math = int(request.form.get("armor_math"))
    else:
        system.armor_math = 1

    if request.form.get("armor_y") != '' and float(request.form.get("armor_y")) >= 0.1:
        system.armor_y = float(request.form.get("armor_y"))
    else:
        system.armor_y = 100.0

    if request.form.get("armor_cap") != '' and float(request.form.get("armor_cap")) > 0:
        system.armor_cap = int(request.form.get("armor_cap"))
    else:
        system.armor_cap = 75

    if request.form.get("armor_price") != '' and int(request.form.get("armor_price")) >= 1:
        system.armor_price = int(request.form.get("armor_price"))
    else:
        system.armor_price = 3


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if 'key' not in session:
        session['key'] = uuid.uuid4()
    sessions[session['key']] = System()

    return render_template('index.html')


@app.route('/ruleset', methods=['GET', 'POST'])
def ruleset():
    system = sessions[session['key']]

    if request.method == 'POST':
        if request.form.get('ruleset_update', False) == 'Confirm':
            set_ruleset()

    return render_template('ruleset.html', system=system)


@app.route('/stat_sheet', methods=['GET', 'POST'])
def stat_sheet():
    system = sessions[session['key']]

    if request.method == 'POST':
        if request.form.get('stats_update', False) == 'Confirm':
            set_stats()

    return render_template('stat-sheet.html', system=system)


@app.route('/simulation', methods=['GET', 'POST'])
def simulation():
    system = sessions[session['key']]
    win_condition = False
    combatlog = []

    hero_health = (system.hero.endurance * system.endurance_value) + system.base_health
    enemy_health = (system.enemy.endurance * system.endurance_value) + system.base_health
    hero_speed_base = system.hero.speed
    enemy_speed_base = system.enemy.speed
    damage = 0
    attack_type = 'Default'
    attack_name = 'Default'
    hero_charisma_buff = False
    hero_buff = 0.0
    enemy_charisma_buff = False
    enemy_buff = 0.0
    hero_charisma_debuff = False
    hero_debuff = 0.0
    enemy_charisma_debuff = False
    enemy_debuff = 0.0
    amount_absorbed = 0
    critical = False
    dodged = False
    absorption = False

    # The following is the most abhorrent piece of code I have ever written.
    # It came from pilled up decisions that got implemented in HTML
    # but were not properly thought through in terms of backend.
    def attack_choice(token, damage_input, attack_name_output):
        chance_physical = getattr(getattr(system, token), "likelihood_of_physical")
        physical_damage = getattr(getattr(system, token), "physical_damage")
        magical_damage = getattr(getattr(system, token), "magical_damage")

        attack_1_type = getattr(getattr(system, token), "attack_1_type")
        attack_1_name = getattr(getattr(system, token), "attack_1_name")
        attack_1_min = getattr(getattr(system, token), "attack_1_min")
        attack_1_max = getattr(getattr(system, token), "attack_1_max")
        attack_1_chance = getattr(getattr(system, token), "attack_1_chance")

        attack_2_type = getattr(getattr(system, token), "attack_2_type")
        attack_2_name = getattr(getattr(system, token), "attack_2_name")
        attack_2_min = getattr(getattr(system, token), "attack_2_min")
        attack_2_max = getattr(getattr(system, token), "attack_2_max")
        attack_2_chance = getattr(getattr(system, token), "attack_2_chance")

        attack_3_type = getattr(getattr(system, token), "attack_3_type")
        attack_3_name = getattr(getattr(system, token), "attack_3_name")
        attack_3_min = getattr(getattr(system, token), "attack_3_min")
        attack_3_max = getattr(getattr(system, token), "attack_3_max")
        attack_3_chance = getattr(getattr(system, token), "attack_3_chance")

        attack_4_type = getattr(getattr(system, token), "attack_4_type")
        attack_4_name = getattr(getattr(system, token), "attack_4_name")
        attack_4_min = getattr(getattr(system, token), "attack_4_min")
        attack_4_max = getattr(getattr(system, token), "attack_4_max")
        attack_4_chance = getattr(getattr(system, token), "attack_4_chance")

        physical_attack_chances = []
        magical_attack_chances = []
        if attack_1_type == "physical":
            physical_attack_chances.append(attack_1_chance)
            magical_attack_chances.append(0)
        else:
            magical_attack_chances.append(attack_1_chance)
            physical_attack_chances.append(0)
        if attack_2_type == "physical":
            physical_attack_chances.append(attack_2_chance)
            magical_attack_chances.append(0)
        else:
            magical_attack_chances.append(attack_2_chance)
            physical_attack_chances.append(0)
        if attack_3_type == "physical":
            physical_attack_chances.append(attack_3_chance)
            magical_attack_chances.append(0)
        else:
            magical_attack_chances.append(attack_3_chance)
            physical_attack_chances.append(0)
        if attack_4_type == "physical":
            physical_attack_chances.append(attack_4_chance)
            magical_attack_chances.append(0)
        else:
            magical_attack_chances.append(attack_4_chance)
            physical_attack_chances.append(0)

        if chance_physical >= random.randint(1, 100):
            roll = random.randint(1, 100)
            if attack_1_type == "physical" and physical_attack_chances[0] >= roll:
                damage_input = (random.randint(attack_1_min * 1000,
                                               attack_1_max * 1000) * physical_damage) / 1000
                attack_name_output = attack_1_name

            elif attack_2_type == "physical" and \
                    physical_attack_chances[0] + \
                    physical_attack_chances[1] >= roll:
                damage_input = (random.randint(attack_2_min * 1000,
                                               attack_2_max * 1000) * physical_damage) / 1000
                attack_name_output = attack_2_name

            elif attack_3_type == "physical" and \
                    physical_attack_chances[0] + \
                    physical_attack_chances[1] + \
                    physical_attack_chances[2] >= roll:
                damage_input = (random.randint(attack_3_min * 1000,
                                               attack_3_max * 1000) * physical_damage) / 1000
                attack_name_output = attack_3_name

            elif attack_4_type == "physical" and \
                    physical_attack_chances[0] + \
                    physical_attack_chances[1] + \
                    physical_attack_chances[2] + \
                    physical_attack_chances[3] >= roll:
                damage_input = (random.randint(attack_4_min * 1000,
                                               attack_4_max * 1000) * physical_damage) / 1000
                attack_name_output = attack_4_name

            attack_type_output = "physical"
        else:
            roll = random.randint(1, 100)
            if attack_1_type == "magical" and magical_attack_chances[0] >= roll:
                damage_input = (random.randint(attack_1_min * 1000,
                                               attack_1_max * 1000) * magical_damage) / 1000
                attack_name_output = attack_1_name

            elif attack_2_type == "magical" and \
                    magical_attack_chances[0] + \
                    magical_attack_chances[1] >= roll:
                damage_input = (random.randint(attack_2_min * 1000,
                                               attack_2_max * 1000) * magical_damage) / 1000
                attack_name_output = attack_2_name

            elif attack_3_type == "magical" and \
                    magical_attack_chances[0] + \
                    magical_attack_chances[1] + \
                    magical_attack_chances[2] >= roll:
                damage_input = (random.randint(attack_3_min * 1000,
                                               attack_3_max * 1000) * magical_damage) / 1000
                attack_name_output = attack_3_name

            elif attack_4_type == "magical" and \
                    magical_attack_chances[0] + \
                    magical_attack_chances[1] + \
                    magical_attack_chances[2] + \
                    magical_attack_chances[3] >= roll:
                damage_input = (random.randint(attack_4_min * 1000,
                                               attack_4_max * 1000) * magical_damage) / 1000
                attack_name_output = attack_4_name

            attack_type_output = "magical"

        return damage_input, attack_type_output, attack_name_output

    def critical_chance(token, damage_input, critical_state):
        crit_chance = getattr(getattr(system, token), "critical_chance")
        if random.randint(1, 100) <= crit_chance:
            critical_state = True
            if attack_type == "physical":
                damage_input *= system.strength_crit
            else:
                damage_input *= system.intelligence_crit
        return damage_input, critical_state

    def armor_mitigation(token, damage_input):
        armor = getattr(getattr(system, token), "armor_mitigation")
        if system.armor_type == attack_type or system.armor_type == "physical and magical":
            if system.armor_math != 4:
                damage_input *= (100 - armor) / 100
            else:
                damage_input -= armor
            if damage_input < 0:
                damage_input = 0
        return damage_input

    def agility_dodge(token, damage_input, dodged_state):
        dodge = getattr(getattr(system, token), "dodge_chance")
        if system.agility_type == attack_type or system.agility_type == "physical and magical":
            if random.randint(1, 100) <= dodge:
                damage_input = 0
                dodged_state = True
        return damage_input, dodged_state

    def willpower_resistance(token, damage_input, absorbed_input, absorption_state):
        resistance = getattr(getattr(system, token), "resistance")
        if dodged is False and (
                system.willpower_type == attack_type or system.willpower_type == "physical and magical") \
                and damage > 0 and resistance > 0:
            absorbed_input = damage_input * (resistance / 100)
            absorbed_input = round(absorbed_input)
            damage_input -= absorbed_input
            absorption_state = True
        return damage_input, absorbed_input, absorption_state

    while not win_condition:
        turn = ""
        if hero_speed_base >= enemy_speed_base:

            damage, attack_type, attack_name = attack_choice("hero", damage, attack_name)

            if hero_charisma_buff:
                damage *= ((100 + hero_buff) / 100)
                hero_charisma_buff = False
            if hero_charisma_debuff:
                damage *= ((100 - hero_debuff) / 100)
                hero_charisma_debuff = False

            damage, critical = critical_chance("hero", damage, critical)
            damage = armor_mitigation("hero", damage)
            damage, dodged = agility_dodge("hero", damage, dodged)
            damage, amount_absorbed, absorption = willpower_resistance("hero", damage, amount_absorbed, absorption)

            damage = round(damage)
            enemy_health -= damage

            turn += '<div class="hero-turn">'
            if dodged:
                turn += system.hero.name + ' strikes with ' + attack_name + ' but the opponent manages to <span ' \
                                                                    'class="agility-dodge">dodge the attack!</span> '
                dodged = False
            else:
                if attack_type == 'physical':
                    turn += system.hero.name + ' strikes with ' + attack_name + ' dealing ' \
                                                '<span class="physical-damage">' + str(damage) + ' damage!</span>'
                else:
                    turn += system.hero.name + ' casts ' + attack_name + ' dealing <span class="magical-damage">' + str(
                        damage) + ' damage!</span>'

                if critical:
                    turn += '<span class="critical-effect"> Critical strike!</span>'
                    critical = False

                if absorption:
                    turn += '<br>' + system.enemy.name + ' manages to <span class="willpower-absorb">absorb ' + str(
                        amount_absorbed) + '</span> of that damage!'
                    absorption = False

            if random.randint(1, 100) <= system.hero.charisma_chance:
                if random.getrandbits(1) == 1:
                    hero_buff = random.randint(system.charisma_min, system.charisma_max)
                    turn += '<br><i class="charisma-effect">' + system.hero.name + " let's out a rallying cry, increasing the power of his next " \
                                                                                   "attack by " + str(
                        hero_buff) + '%!</i>'
                    hero_charisma_buff = True
                else:
                    enemy_debuff = random.randint(system.charisma_min, system.charisma_max)
                    turn += '<br><i class="charisma-effect">' + system.hero.name + " let's out an intimidating roar, decreasing the power of " \
                                                                                   "opponent's next attack " + str(
                        enemy_debuff) + '%!</i>'
                    enemy_charisma_debuff = True

            turn += '</div><br>'
            enemy_speed_base += system.enemy.speed

        else:

            damage, attack_type, attack_name = attack_choice("enemy", damage, attack_name)

            if enemy_charisma_buff:
                damage *= ((100 + enemy_buff) / 100)
                enemy_charisma_buff = False
            if enemy_charisma_debuff:
                damage *= ((100 - enemy_debuff) / 100)
                enemy_charisma_debuff = False

            damage, critical = critical_chance("enemy", damage, critical)
            damage = armor_mitigation("enemy", damage)
            damage, dodged = agility_dodge("enemy", damage, dodged)
            damage, amount_absorbed, absorption = willpower_resistance("enemy", damage, amount_absorbed, absorption)

            damage = round(damage)
            hero_health -= damage

            turn += '<div class="enemy-turn">'
            if dodged:
                turn += system.enemy.name + ' strikes with ' + attack_name + ' but the opponent manages to <span ' \
                                                                    'class="agility-dodge">dodge the attack!</span> '
                dodged = False
            else:
                if attack_type == 'physical':
                    turn += system.enemy.name + ' strikes with ' + attack_name + ' dealing ' \
                                                '<span class="physical-damage">' + str(damage) + ' damage!</span>'
                else:
                    turn += system.enemy.name + ' casts ' + attack_name + ' dealing <span class="magical-damage">' + str(
                        damage) + ' damage!</span>'

                if critical:
                    turn += '<span class="critical-effect"> Critical strike!</span>'
                    critical = False

                if absorption:
                    turn += '<br>' + system.enemy.name + ' manages to <span class="willpower-absorb"> absorb ' + str(
                        amount_absorbed) + '</span> of that damage!'
                    absorption = False

            if random.randint(1, 100) <= system.enemy.charisma_chance:
                if random.getrandbits(1) == 1:
                    enemy_buff = random.randint(system.charisma_min, system.charisma_max)
                    turn += '<br><i class="charisma-effect">' + system.enemy.name + " let's out a rallying cry, increasing the power of his next " \
                                                                                    "attack by " + str(
                        enemy_buff) + '%!</i>'
                    enemy_charisma_buff = True
                else:
                    hero_debuff = random.randint(system.charisma_min, system.charisma_max)
                    turn += '<br><i class="charisma-effect">' + system.enemy.name + " let's out an intimidating roar, decreasing the power of " \
                                                                                    "opponent's next attack " + str(
                        hero_debuff) + '%!</i>'
                    hero_charisma_debuff = True

            turn += '</div><br>'
            hero_speed_base += system.hero.speed

        if hero_health <= 0:
            turn += '<br><div class="enemy-victory">' + system.hero.name + ' has fallen. ' + system.enemy.name + ' has won the battle!</div><br>'
            win_condition = True
        if enemy_health <= 0:
            turn += '<br><div class="hero-victory">' + system.enemy.name + ' has fallen. ' + system.hero.name + ' has won the battle!</div><br>'
            win_condition = True

        combatlog.append(turn)

    return render_template('simulation.html', system=system, combatlog=combatlog)


if __name__ == '__main__':
    app.run()
