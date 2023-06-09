from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask_mysqldb import MySQL

import math
import random
import uuid
import database_credentials

app = Flask(__name__)
database_key = database_credentials.Key()
app.config['MYSQL_HOST'] = database_key.host
app.config['MYSQL_USER'] = database_key.user
app.config['MYSQL_PASSWORD'] = database_key.password
app.config['MYSQL_DB'] = database_key.database

mysql = MySQL(app)

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
        self.strength = 10
        self.intelligence = 10
        self.agility = 10
        self.willpower = 10
        self.endurance = 10
        self.charisma = 10
        self.luck = 10
        self.speed = 10
        self.armor = 10
        self.likelihood_of_physical = 50
        self.likelihood_of_magical = 50

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
        self.physical_damage = 1
        self.magical_damage = 1
        self.dodge_chance = 0
        self.resistance = 0
        self.hitpoints = 0
        self.charisma_chance = 0
        self.critical_chance = 0
        self.armor_mitigation = 0
        self.total_value = 0


class System:
    def __init__(self):
        self.hero = Fighter('Hero')
        self.enemy = Fighter('Enemy')
        self.hero_wins = 0
        self.enemy_wins = 0

        self.strength_dmg = 3
        self.strength_crit = 1.5
        self.strength_price = 2

        self.intelligence_dmg = 4
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
    system.hero_wins = 0
    system.enemy_wins = 0

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
    system.hero_wins = 0
    system.enemy_wins = 0

    # Setting all the ruleset rules

    #
    # STRENGTH
    #
    if request.form.get("strength_dmg") != '' and int(request.form.get("strength_dmg")) > 0:
        system.strength_dmg = int(request.form.get("strength_dmg"))
    else:
        system.strength_dmg = 3

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
    session['loggedin'] = False
    if 'key' not in session:
        session['key'] = uuid.uuid4()
    sessions[session['key']] = System()

    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    system = sessions[session['key']]
    message = ''

    if request.method == 'POST':
        if request.form.get('registration_submit', False) == 'Register':
            username = request.form['username']
            password = request.form['password']
            password_confirm = request.form['password_confirm']

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE username = %s', [username])
            account = cursor.fetchone()
            if username == '' or password == '' or password_confirm == '':
                message = '<div class="authentication-message error-color">Please fill out the form!</div>'
            elif password != password_confirm:
                message = '<div class="authentication-message error-color">Passwords do not match!</div>'
            elif account:
                message = '<div class="authentication-message error-color">Username is already taken!</div>'
            elif len(username) > 64:
                message = '<div class="authentication-message error-color">Username is too long! (Max 64 characters)</div>'
            elif len(password) > 64:
                message = '<div class="authentication-message error-color">Password is too long! (Max 64 characters)</div>'
            else:
                cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, "USER")', ([username], [password]))
                cursor.execute('UPDATE users SET password = MD5(password) WHERE username = %s', [username])
                message = '<div class="authentication-message success-color">You have successfully registered!</div>'
                mysql.connection.commit()

            cursor.close()

    return render_template('registration.html', system=system, message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    system = sessions[session['key']]
    message = ''

    if request.method == 'POST':
        if request.form.get('login_submit', False) == 'Login':
            username = request.form['username']
            password = request.form['password']

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE username = %s and password = md5(%s)', ([username], [password]))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['username'] = account[1]
                session['user_type'] = account[3]
                cursor.close()
                return redirect(url_for('ruleset'))
            else:
                message = '<div class="authentication-message error-color">Incorrect username or password!</div>'

            cursor.close()

    return render_template('login.html', system=system, message=message)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    system = sessions[session['key']]
    if not session['loggedin']:
        return redirect(url_for('homepage'))

    session['loggedin'] = False
    session['username'] = ''

    return render_template('login.html', system=system)


@app.route('/share', methods=['GET', 'POST'])
def share():
    system = sessions[session['key']]
    if not session['loggedin']:
        return redirect(url_for('homepage'))

    if request.method == 'POST':
        if request.form.get('share_submit', False) == 'Share':
            cursor = mysql.connection.cursor()
            comment = request.form['comment']
            title = request.form['title']

            # I think this could've been done better by concatenating some sort of list of class attributes.

            cursor.execute('INSERT INTO combat_systems VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
                           '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
                           '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
                           '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
                           '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
                           '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
                           '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           ([session['username']], [title], [comment],
                            [system.strength_dmg], [system.strength_crit], [system.strength_price],

                            [system.intelligence_dmg], [system.intelligence_crit], [system.intelligence_price],

                            [system.agility_type], [system.agility_math], [system.agility_x],
                            [system.agility_y], [system.agility_cap], [system.agility_price],

                            [system.willpower_type], [system.willpower_math], [system.willpower_x],
                            [system.willpower_y], [system.willpower_cap], [system.willpower_price],

                            [system.base_health], [system.endurance_value], [system.endurance_price],

                            [system.charisma_math], [system.charisma_x], [system.charisma_y], [system.charisma_min],
                            [system.charisma_max], [system.charisma_cap], [system.charisma_price],

                            [system.luck_math], [system.luck_x], [system.luck_y], [system.luck_cap],
                            [system.luck_price],

                            [system.speed_price],

                            [system.armor_type], [system.armor_math], [system.armor_y], [system.armor_cap],
                            [system.armor_price],

                            [system.hero.name], [system.hero.level], [system.hero.strength], [system.hero.intelligence],
                            [system.hero.agility], [system.hero.willpower], [system.hero.endurance],
                            [system.hero.charisma], [system.hero.luck], [system.hero.speed], [system.hero.armor],

                            [system.hero.likelihood_of_physical], [system.hero.likelihood_of_magical],

                            [system.hero.attack_1_type], [system.hero.attack_1_name], [system.hero.attack_1_min],
                            [system.hero.attack_1_max], [system.hero.attack_1_chance],

                            [system.hero.attack_2_type], [system.hero.attack_2_name], [system.hero.attack_2_min],
                            [system.hero.attack_2_max], [system.hero.attack_2_chance],

                            [system.hero.attack_3_type], [system.hero.attack_3_name], [system.hero.attack_3_min],
                            [system.hero.attack_3_max], [system.hero.attack_3_chance],

                            [system.hero.attack_4_type], [system.hero.attack_4_name], [system.hero.attack_4_min],
                            [system.hero.attack_4_max], [system.hero.attack_4_chance],

                            [system.enemy.name], [system.enemy.level], [system.enemy.strength],
                            [system.enemy.intelligence], [system.enemy.agility], [system.enemy.willpower],
                            [system.enemy.endurance], [system.enemy.charisma], [system.enemy.luck],
                            [system.enemy.speed], [system.enemy.armor],

                            [system.enemy.likelihood_of_physical], [system.enemy.likelihood_of_magical],

                            [system.enemy.attack_1_type], [system.enemy.attack_1_name], [system.enemy.attack_1_min],
                            [system.enemy.attack_1_max], [system.enemy.attack_1_chance],

                            [system.enemy.attack_2_type], [system.enemy.attack_2_name], [system.enemy.attack_2_min],
                            [system.enemy.attack_2_max], [system.enemy.attack_2_chance],

                            [system.enemy.attack_3_type], [system.enemy.attack_3_name], [system.enemy.attack_3_min],
                            [system.enemy.attack_3_max], [system.enemy.attack_3_chance],

                            [system.enemy.attack_4_type], [system.enemy.attack_4_name], [system.enemy.attack_4_min],
                            [system.enemy.attack_4_max], [system.enemy.attack_4_chance],
                            ))

            mysql.connection.commit()
            cursor.close()

    return render_template('share.html', system=system)


@app.route('/browse', methods=['GET', 'POST'])
def browse():
    system = sessions[session['key']]
    if not session['loggedin']:
        return redirect(url_for('homepage'))

    if request.method == 'POST':
        if request.form.get('delete', False) == 'Delete':
            cursor = mysql.connection.cursor()
            cursor.execute('DELETE FROM combat_systems WHERE `id` = %s', [request.form['systemId']])
            mysql.connection.commit()
            cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT `id`, `username`, `title`, `comment` FROM combat_systems')
    database = cursor.fetchall()
    cursor.close()

    return render_template('browse.html', system=system, database=database, user_type=session['user_type'])


@app.route('/ruleset', methods=['GET', 'POST'])
def ruleset():
    system = sessions[session['key']]

    if request.method == 'POST':
        if request.form.get('ruleset_update', False) == 'Confirm':
            set_ruleset()
        elif request.form.get('confirm', False) == 'Use this':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM combat_systems WHERE `id` = %s', [request.form['systemId']])
            data = cursor.fetchone()

            system.strength_dmg = data[4]
            system.strength_crit = data[5]
            system.strength_price = data[6]

            system.intelligence_dmg = data[7]
            system.intelligence_crit = data[8]
            system.intelligence_price = data[9]

            system.agility_type = data[10]
            system.agility_math = data[11]
            system.agility_x = data[12]
            system.agility_y = data[13]
            system.agility_cap = data[14]
            system.agility_price = data[15]

            system.willpower_type = data[16]
            system.willpower_math = data[17]
            system.willpower_x = data[18]
            system.willpower_y = data[19]
            system.willpower_cap = data[20]
            system.willpower_price = data[21]

            system.base_health = data[22]
            system.endurance_value = data[23]
            system.endurance_price = data[24]

            system.charisma_math = data[25]
            system.charisma_x = data[26]
            system.charisma_y = data[27]
            system.charisma_min = data[28]
            system.charisma_max = data[29]
            system.charisma_cap = data[30]
            system.charisma_price = data[31]

            system.luck_math = data[32]
            system.luck_x = data[33]
            system.luck_y = data[34]
            system.luck_cap = data[35]
            system.luck_price = data[36]

            system.speed_price = data[37]

            system.armor_type = data[38]
            system.armor_math = data[39]
            system.armor_y = data[40]
            system.armor_cap = data[41]
            system.armor_price = data[42]

            system.hero.name = data[43]
            system.hero.level = data[44]
            system.hero.strength = data[45]
            system.hero.intelligence = data[46]
            system.hero.agility = data[47]
            system.hero.willpower = data[48]
            system.hero.endurance = data[49]
            system.hero.charisma = data[50]
            system.hero.luck = data[51]
            system.hero.speed = data[52]
            system.hero.armor = data[53]

            system.hero.likelihood_of_physical = data[54]
            system.hero.likelihood_of_magical = data[55]

            system.hero.attack_1_type = data[56]
            system.hero.attack_1_name = data[57]
            system.hero.attack_1_min = data[58]
            system.hero.attack_1_max = data[59]
            system.hero.attack_1_chance = data[60]

            system.hero.attack_2_type = data[61]
            system.hero.attack_2_name = data[62]
            system.hero.attack_2_min = data[63]
            system.hero.attack_2_max = data[64]
            system.hero.attack_2_chance = data[65]

            system.hero.attack_3_type = data[66]
            system.hero.attack_3_name = data[67]
            system.hero.attack_3_min = data[68]
            system.hero.attack_3_max = data[69]
            system.hero.attack_3_chance = data[70]

            system.hero.attack_4_type = data[71]
            system.hero.attack_4_name = data[72]
            system.hero.attack_4_min = data[73]
            system.hero.attack_4_max = data[74]
            system.hero.attack_4_chance = data[75]

            system.enemy.name = data[76]
            system.enemy.level = data[77]
            system.enemy.strength = data[78]
            system.enemy.intelligence = data[79]
            system.enemy.agility = data[80]
            system.enemy.willpower = data[81]
            system.enemy.endurance = data[82]
            system.enemy.charisma = data[83]
            system.enemy.luck = data[84]
            system.enemy.speed = data[85]
            system.enemy.armor = data[86]

            system.enemy.likelihood_of_physical = data[87]
            system.enemy.likelihood_of_magical = data[88]

            system.enemy.attack_1_type = data[89]
            system.enemy.attack_1_name = data[90]
            system.enemy.attack_1_min = data[91]
            system.enemy.attack_1_max = data[92]
            system.enemy.attack_1_chance = data[93]

            system.enemy.attack_2_type = data[94]
            system.enemy.attack_2_name = data[95]
            system.enemy.attack_2_min = data[96]
            system.enemy.attack_2_max = data[97]
            system.enemy.attack_2_chance = data[98]

            system.enemy.attack_3_type = data[99]
            system.enemy.attack_3_name = data[100]
            system.enemy.attack_3_min = data[101]
            system.enemy.attack_3_max = data[102]
            system.enemy.attack_3_chance = data[103]

            system.enemy.attack_4_type = data[104]
            system.enemy.attack_4_name = data[105]
            system.enemy.attack_4_min = data[106]
            system.enemy.attack_4_max = data[107]
            system.enemy.attack_4_chance = data[108]

            cursor.close()

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
    loops = 1
    combatlog = []

    if request.method == 'POST':
        if request.form.get('simulate_10', False) == 'x10':
            loops = 10
        elif request.form.get('simulate_100', False) == 'x100':
            loops = 100
        elif request.form.get('simulate_1000', False) == 'x1000':
            loops = 1000

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

    while loops > 0:
        win_condition = False
        combatlog.clear()
        turn_number = 0

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
        critical = False
        dodged = False
        absorption = False

        loops -= 1

        while not win_condition:
            turn = ""
            amount_absorbed = 0
            if hero_speed_base >= enemy_speed_base:

                turn_number += 1
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

                turn += '<div class="hero-turn tooltip">Turn ' + str(turn_number) + ':<br><br><div class="hero-damage">'
                if dodged:
                    turn += system.hero.name + ' strikes with ' + attack_name + ' but the opponent manages to <span ' \
                                                                                'class="agility-dodge">dodge the attack!</span> '
                    dodged = False
                else:
                    if attack_type == 'physical':
                        turn += system.hero.name + ' strikes with ' + attack_name + ' dealing ' \
                                                                                    '<span class="physical-damage">' + str(
                            damage + amount_absorbed) + ' damage!</span>'
                    else:
                        turn += system.hero.name + ' casts ' + attack_name + ' dealing <span class="magical-damage">' + str(
                            damage + amount_absorbed) + ' damage!</span>'

                    if critical:
                        turn += '<span class="critical-effect"> Critical strike!</span>'
                        critical = False

                    if absorption:
                        turn += '<br>' + system.enemy.name + ' manages to <span class="willpower-absorb">resist ' + str(
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
                                                                                       "opponent's next attack by " + str(
                            enemy_debuff) + '%!</i>'
                        enemy_charisma_debuff = True

                turn += '</div><br>' + system.hero.name + "'s health: " + str(hero_health) + "<br>" + \
                        system.enemy.name + "'s health: " + str(enemy_health + damage) + " (-" + str(damage) + ")" + \
                        '</span></div><br>'
                enemy_speed_base += system.enemy.speed

            else:

                turn_number += 1
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

                turn += '<div class="enemy-turn tooltip">Turn ' + str(turn_number) + ':<br><br><div class="enemy-damage">'
                if dodged:
                    turn += system.enemy.name + ' strikes with ' + attack_name + ' but the opponent manages to <span ' \
                                                                                 'class="agility-dodge">dodge the attack!</span> '
                    dodged = False
                else:
                    if attack_type == 'physical':
                        turn += system.enemy.name + ' strikes with ' + attack_name + ' dealing ' \
                                                                                     '<span class="physical-damage">' + str(
                            damage + amount_absorbed) + ' damage!</span>'
                    else:
                        turn += system.enemy.name + ' casts ' + attack_name + ' dealing <span class="magical-damage">' + str(
                            damage + amount_absorbed) + ' damage!</span>'

                    if critical:
                        turn += '<span class="critical-effect"> Critical strike!</span>'
                        critical = False

                    if absorption:
                        turn += '<br>' + system.enemy.name + ' manages to <span class="willpower-absorb"> resist ' + str(
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
                                                                                        "opponent's next attack by " + str(
                            hero_debuff) + '%!</i>'
                        hero_charisma_debuff = True

                turn += '</div><br>' + system.hero.name + "'s health: " + str(hero_health + damage) + " (-" + str(
                    damage) + ")<br>" + system.enemy.name + "'s health: " + str(enemy_health) + '</span></div><br>'
                hero_speed_base += system.hero.speed

            if hero_health <= 0:
                turn += '<br><div class="enemy-victory">' + system.hero.name + ' has fallen. ' + system.enemy.name + ' has won the battle!</div><br>'
                system.enemy_wins += 1
                win_condition = True
            if enemy_health <= 0:
                turn += '<br><div class="hero-victory">' + system.enemy.name + ' has fallen. ' + system.hero.name + ' has won the battle!</div><br>'
                system.hero_wins += 1
                win_condition = True

            combatlog.append(turn)

    return render_template('simulation.html', system=system, combatlog=combatlog)


if __name__ == '__main__':
    app.run()
