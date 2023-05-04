from flask import Flask
from flask import render_template
from flask import request
from flask import session
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

        self.physical_min = 0
        self.physical_max = 0
        self.magical_min = 0
        self.magical_max = 0
        self.dodge_chance = 0
        self.resistance = 0
        self.hitpoints = 0
        self.charisma_chance = 0
        self.charisma_min = 0
        self.charisma_max = 0
        self.critical_chance = 0
        self.haste = 0
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
        self.armor_price = 2


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
    game_state = 0

    def battle_turn(token):
        if token == 'Hero':
            placeholder = 0
        else:
            placeholder = 0

    def combatlog():
        if game_state == 0:
            if system.hero.speed >= system.enemy.speed:
                battle_turn('Hero')
            else:
                battle_turn('Enemy')

    return render_template('simulation.html', system=system)


if __name__ == '__main__':
    app.run()
