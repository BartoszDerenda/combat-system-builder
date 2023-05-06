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

        self.physical_min = 0
        self.physical_max = 0
        self.magical_min = 0
        self.magical_max = 0
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
        self.agility_y = 3
        self.agility_cap = 33
        self.agility_price = 1

        self.willpower_type = "magical"
        self.willpower_math = 1
        self.willpower_x = "intelligence"
        self.willpower_y = 2
        self.willpower_cap = 50
        self.willpower_price = 1

        self.base_health = 200
        self.endurance_value = 10
        self.endurance_price = 3

        self.charisma_math = 1
        self.charisma_x = "level"
        self.charisma_y = 3
        self.charisma_min = 15
        self.charisma_max = 35
        self.charisma_cap = 33
        self.charisma_price = 1

        self.luck_math = 1
        self.luck_x = "level"
        self.luck_y = 2
        self.luck_cap = 50
        self.luck_price = 1

        self.speed_price = 3

        self.armor_type = "physical and magical"
        self.armor_math = 1
        self.armor_y = 100
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
        effect_chance = attribute
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
    elif attribute_math == 3 or attribute_math == 4:
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
        system.hero.agility = 1

    if request.form.get("hero_will") != '' and int(request.form.get("hero_will")) > 0:
        system.hero.willpower = int(request.form.get("hero_will"))
    else:
        system.hero.willpower = 1

    if request.form.get("hero_end") != '' and int(request.form.get("hero_end")) > 0:
        system.hero.endurance = int(request.form.get("hero_end"))
    else:
        system.hero.endurance = 1

    if request.form.get("hero_char") != '' and int(request.form.get("hero_char")) > 0:
        system.hero.charisma = int(request.form.get("hero_char"))
    else:
        system.hero.charisma = 1

    if request.form.get("hero_lck") != '' and int(request.form.get("hero_lck")) > 0:
        system.hero.luck = int(request.form.get("hero_lck"))
    else:
        system.hero.luck = 1

    if request.form.get("hero_spd") != '' and int(request.form.get("hero_spd")) > 0:
        system.hero.speed = int(request.form.get("hero_spd"))
    else:
        system.hero.speed = 1

    if request.form.get("hero_armor") != '' and int(request.form.get("hero_armor")) > 0:
        system.hero.armor = int(request.form.get("hero_armor"))
    else:
        system.hero.armor = 1

    if request.form.get("hero_likelihood_of_physical") != '' and int(
            request.form.get("hero_likelihood_of_physical")) > 0:
        system.hero.likelihood_of_physical = int(request.form.get("hero_likelihood_of_physical"))
    else:
        system.hero.likelihood_of_physical = 50

    if request.form.get("hero_likelihood_of_magical") != '' and int(request.form.get("hero_likelihood_of_magical")) > 0:
        system.hero.likelihood_of_magical = int(request.form.get("hero_likelihood_of_magical"))
    else:
        system.hero.likelihood_of_magical = 50

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
        system.enemy.agility = 1

    if request.form.get("enemy_will") != '' and int(request.form.get("enemy_will")) > 0:
        system.enemy.willpower = int(request.form.get("enemy_will"))
    else:
        system.enemy.willpower = 1

    if request.form.get("enemy_end") != '' and int(request.form.get("enemy_end")) > 0:
        system.enemy.endurance = int(request.form.get("enemy_end"))
    else:
        system.enemy.endurance = 1

    if request.form.get("enemy_char") != '' and int(request.form.get("enemy_char")) > 0:
        system.enemy.charisma = int(request.form.get("enemy_char"))
    else:
        system.enemy.charisma = 1

    if request.form.get("enemy_lck") != '' and int(request.form.get("enemy_lck")) > 0:
        system.enemy.luck = int(request.form.get("enemy_lck"))
    else:
        system.enemy.luck = 1

    if request.form.get("enemy_spd") != '' and int(request.form.get("enemy_spd")) > 0:
        system.enemy.speed = int(request.form.get("enemy_spd"))
    else:
        system.enemy.speed = 1

    if request.form.get("enemy_armor") != '' and int(request.form.get("enemy_armor")) > 0:
        system.enemy.armor = int(request.form.get("enemy_armor"))
    else:
        system.enemy.armor = 1

    if request.form.get("enemy_likelihood_of_physical") != '' and int(
            request.form.get("enemy_likelihood_of_physical")) > 0:
        system.enemy.likelihood_of_physical = int(request.form.get("enemy_likelihood_of_physical"))
    else:
        system.enemy.likelihood_of_physical = 50

    if request.form.get("enemy_likelihood_of_magical") != '' and int(
            request.form.get("enemy_likelihood_of_magical")) > 0:
        system.enemy.likelihood_of_magical = int(request.form.get("enemy_likelihood_of_magical"))
    else:
        system.enemy.likelihood_of_magical = 50

    # Hero extras
    system.hero.physical_min = round(system.hero.strength * system.strength_dmg * system.strength_min)
    system.hero.physical_max = round(system.hero.strength * system.strength_dmg * system.strength_max)

    system.hero.magical_min = round(system.hero.intelligence * system.intelligence_dmg * system.intelligence_min)
    system.hero.magical_max = round(system.hero.intelligence * system.intelligence_dmg * system.intelligence_max)

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

    # Hero extras
    system.enemy.physical_min = round(system.enemy.strength * system.strength_dmg * system.strength_min)
    system.enemy.physical_max = round(system.enemy.strength * system.strength_dmg * system.strength_max)

    system.enemy.magical_min = round(system.enemy.intelligence * system.intelligence_dmg * system.intelligence_min)
    system.enemy.magical_max = round(system.enemy.intelligence * system.intelligence_dmg * system.intelligence_max)

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

    if request.form.get("strength_min") != '' and float(request.form.get("strength_min")) > 0:
        system.strength_min = float(request.form.get("strength_min"))
    else:
        system.strength_min = 0.9

    if request.form.get("strength_max") != '' and float(request.form.get("strength_max")) > 0:
        system.strength_max = float(request.form.get("strength_max"))
    else:
        system.strength_max = 1.1

    if system.strength_min > system.strength_max:
        temp = system.strength_min
        system.strength_min = system.strength_max
        system.strength_max = temp

    if request.form.get("strength_crit") != '' and float(request.form.get("strength_crit")) > 0:
        system.strength_crit = float(request.form.get("strength_crit"))
    else:
        system.strength_crit = 1.5

    if request.form.get("strength_price") != '' and int(request.form.get("strength_price")) > 0:
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

    if request.form.get("intelligence_min") != '' and float(request.form.get("intelligence_min")) > 0:
        system.intelligence_min = float(request.form.get("intelligence_min"))
    else:
        system.intelligence_min = 0.9

    if request.form.get("intelligence_max") != '' and float(request.form.get("intelligence_max")) > 0:
        system.intelligence_max = float(request.form.get("intelligence_max"))
    else:
        system.intelligence_max = 1.1

    if system.intelligence_min > system.intelligence_max:
        temp = system.intelligence_min
        system.intelligence_min = system.intelligence_max
        system.intelligence_max = temp

    if request.form.get("intelligence_crit") != '' and float(request.form.get("intelligence_crit")) > 0:
        system.intelligence_crit = float(request.form.get("intelligence_crit"))
    else:
        system.intelligence_crit = 1.5

    if request.form.get("intelligence_price") != '' and int(request.form.get("intelligence_price")) > 0:
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

    if request.form.get("agility_y") != '' and int(request.form.get("agility_y")) > 0:
        system.agility_y = int(request.form.get("agility_y"))
    else:
        system.agility_y = 3

    if request.form.get("agility_cap") != '' and int(request.form.get("agility_cap")) > 0:
        system.agility_cap = int(request.form.get("agility_cap"))
    else:
        system.agility_cap = 33

    if request.form.get("agility_price") != '' and int(request.form.get("agility_price")) > 0:
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

    if request.form.get("willpower_y") != '' and int(request.form.get("willpower_y")) > 0:
        system.willpower_y = int(request.form.get("willpower_y"))
    else:
        system.willpower_y = 3

    if request.form.get("willpower_cap") != '' and int(request.form.get("willpower_cap")) > 0:
        system.willpower_cap = int(request.form.get("willpower_cap"))
    else:
        system.willpower_cap = 50

    if request.form.get("willpower_price") != '' and int(request.form.get("willpower_price")) > 0:
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

    if request.form.get("endurance_value") != '' and int(request.form.get("endurance_value")) > 0:
        system.endurance_value = int(request.form.get("endurance_value"))
    else:
        system.endurance_value = 10

    if request.form.get("endurance_price") != '' and int(request.form.get("endurance_price")) > 0:
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

    if request.form.get("charisma_y") != '' and int(request.form.get("charisma_y")) > 0:
        system.charisma_y = int(request.form.get("charisma_y"))
    else:
        system.charisma_y = 3

    if request.form.get("charisma_min") != '' and int(request.form.get("charisma_min")) > 0:
        system.charisma_min = int(request.form.get("charisma_min"))
    else:
        system.charisma_min = 15

    if request.form.get("charisma_max") != '' and int(request.form.get("charisma_max")) > 0:
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

    if request.form.get("charisma_price") != '' and int(request.form.get("charisma_price")) > 0:
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

    if request.form.get("luck_y") != '' and int(request.form.get("luck_y")) > 0:
        system.luck_y = int(request.form.get("luck_y"))
    else:
        system.luck_y = 2

    if request.form.get("luck_cap") != '' and int(request.form.get("luck_cap")) > 0:
        system.luck_cap = int(request.form.get("luck_cap"))
    else:
        system.luck_cap = 50

    if request.form.get("luck_price") != '' and int(request.form.get("luck_price")) > 0:
        system.luck_price = int(request.form.get("luck_price"))
    else:
        system.luck_price = 1

    #
    # SPEED
    #
    if request.form.get("speed_price") != '' and int(request.form.get("speed_price")) > 0:
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

    if request.form.get("armor_price") != '' and int(request.form.get("armor_price")) > 0:
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
    turn = ''

    hero_health = (system.hero.endurance * system.endurance_value) + system.base_health
    enemy_health = (system.enemy.endurance * system.endurance_value) + system.base_health
    hero_speed_base = system.hero.speed
    enemy_speed_base = system.enemy.speed
    hero_charisma_buff = False
    hero_buff = 0.0
    enemy_charisma_buff = False
    enemy_buff = 0.0
    hero_charisma_debuff = False
    hero_debuff = 0.0
    enemy_charisma_debuff = False
    enemy_debuff = 0.0
    absorbed = 0
    critical = False
    dodged = False
    absorption = False

    while not win_condition:
        turn = ''
        if hero_speed_base >= enemy_speed_base:
            chance_physical = system.hero.likelihood_of_physical
            chance_magical = system.hero.likelihood_of_physical + system.hero.likelihood_of_magical
            if chance_physical <= random.randint(1, 100):
                damage = (random.randint(system.strength_min * 10,
                                         system.strength_max * 10) * system.hero.strength * system.strength_dmg) / 10
                attack_type = "physical"
            else:
                damage = (random.randint(system.intelligence_min * 10,
                                         system.intelligence_max * 10) * system.hero.intelligence * system.intelligence_dmg) / 10
                attack_type = "magical"

            if random.randint(1, 100) <= system.hero.critical_chance:
                critical = True
                if attack_type == "physical":
                    damage *= system.strength_crit
                else:
                    damage *= system.intelligence_crit

            if hero_charisma_buff:
                damage *= (hero_buff / 10)
            if hero_charisma_debuff:
                damage *= (hero_debuff / 10)

            if system.armor_type == attack_type or system.agility_type == "physical and magical":
                if system.armor_math != 4:
                    damage *= (system.hero.armor_mitigation / 100)
                else:
                    damage -= system.hero.armor_mitigation
                if damage < 0:
                    damage = 0

            if system.agility_type == attack_type or system.agility_type == "physical and magical":
                if random.randint(1, 100) <= system.hero.dodge_chance:
                    damage = 0
                    dodged = True

            if system.willpower_type == attack_type or system.willpower_type == "physical and magical":
                absorbed = damage * (system.hero.resistance / 100)
                absorbed = round(absorbed)
                damage *= (system.hero.resistance / 100)
                absorption = True

            damage = round(damage)
            enemy_health -= damage

            if dodged:
                turn += system.hero.name + ' attacks the opponent but he manages to dodge the attack!'
                dodged = False
            else:
                if attack_type == 'physical':
                    turn += system.hero.name + ' strikes the opponent dealing ' + str(damage) + ' damage!'
                else:
                    turn += system.hero.name + ' slings a spell at the opponent dealing ' + str(damage) + ' damage!'

                if critical:
                    turn += ' Critical strike!'
                    critical = False

                if absorption:
                    turn += '<br>' + system.enemy.name + ' manages to absorb ' + str(absorbed) + ' of that damage!'
                    absorption = False

            turn += '<br>'

            if random.randint(1, 100) <= system.hero.charisma_chance:
                if random.getrandbits(1) == 1:
                    hero_buff = random.randint(system.charisma_min, system.charisma_max)
                    turn += '<i>' + system.hero.name + "let's out a rallying cry, increasing the power of his next " \
                                                       "attack by " + str(hero_buff) + '%!</i>'
                    hero_charisma_buff = True
                else:
                    enemy_debuff = random.randint(system.charisma_min, system.charisma_max)
                    turn += '<i>' + system.hero.name + "let's out an intimidating roar, decreasing the power of " \
                                                       "opponent's next attack " + str(enemy_debuff) + '%!</i>'
                    enemy_charisma_debuff = True

            enemy_speed_base += enemy_speed_base

        else:
            chance_physical = system.enemy.likelihood_of_physical
            if chance_physical <= random.randint(1, 100):
                damage = (random.randint(system.strength_min * 10,
                                         system.strength_max * 10) * system.enemy.strength * system.strength_dmg) / 10
                attack_type = "physical"
            else:
                damage = (random.randint(system.intelligence_min * 10,
                                         system.intelligence_max * 10) * system.enemy.intelligence * system.intelligence_dmg) / 10
                attack_type = "magical"

            if random.randint(1, 100) <= system.enemy.critical_chance:
                critical = True
                if attack_type == "physical":
                    damage *= system.strength_crit
                else:
                    damage *= system.intelligence_crit

            if enemy_charisma_buff:
                damage *= (enemy_buff / 10)
            if enemy_charisma_debuff:
                damage *= (enemy_debuff / 10)

            if system.armor_type == attack_type or system.agility_type == "physical and magical":
                if system.armor_math != 4:
                    damage *= (system.enemy.armor_mitigation / 100)
                else:
                    damage -= system.enemy.armor_mitigation
                if damage < 0:
                    damage = 0

            if system.agility_type == attack_type or system.agility_type == "physical and magical":
                if random.randint(1, 100) <= system.enemy.dodge_chance:
                    damage = 0
                    dodged = True

            if system.willpower_type == attack_type or system.willpower_type == "physical and magical":
                absorbed = damage * (system.enemy.resistance / 100)
                absorbed = round(absorbed)
                damage *= (system.enemy.resistance / 100)
                absorption = True

            damage = round(damage)
            enemy_health -= damage

            if dodged:
                turn += system.enemy.name + ' attacks the opponent but he manages to dodge the attack!'
                dodged = False
            else:
                if attack_type == 'physical':
                    turn += system.enemy.name + ' strikes the opponent dealing ' + str(damage) + ' damage!'
                else:
                    turn += system.enemy.name + ' slings a spell at the opponent dealing ' + str(damage) + ' damage!'

                if critical:
                    turn += ' Critical strike!'
                    critical = False

                if absorption:
                    turn += '<br>' + system.enemy.name + ' manages to absorb ' + str(absorbed) + ' of that damage!'
                    absorption = False

            turn += '<br>'

            if random.randint(1, 100) <= system.enemy.charisma_chance:
                if random.getrandbits(1) == 1:
                    enemy_buff = random.randint(system.charisma_min, system.charisma_max)
                    turn += '<i>' + system.enemy.name + "let's out a rallying cry, increasing the power of his next " \
                                                        "attack by " + str(enemy_buff) + '%!</i>'
                    enemy_charisma_buff = True
                else:
                    hero_debuff = random.randint(system.charisma_min, system.charisma_max)
                    turn += '<i>' + system.enemy.name + "let's out an intimidating roar, decreasing the power of " \
                                                        "opponent's next attack " + str(hero_debuff) + '%!</i>'
                    hero_charisma_debuff = True

            hero_speed_base += hero_speed_base

        if hero_health <= 0:
            turn += system.hero.name + ' has fallen. ' + system.enemy.name + ' has won the battle!<br>'
            win_condition = True
        if enemy_health <= 0:
            turn += system.enemy.name + ' has fallen. ' + system.hero.name + ' has won the battle!<br>'
            win_condition = True

        combatlog.append(turn)

    return render_template('simulation.html', system=system, combatlog=combatlog)


if __name__ == '__main__':
    app.run()
