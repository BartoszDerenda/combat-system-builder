from flask import Flask
from flask import render_template
from flask import request
from flask import session
import random
import uuid

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
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
        self.magic_resistance = 0
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
        self.agility_versus = 1
        self.agility_math = 1
        self.agility_cap = 33
        self.agility_price = 1

        self.willpower_type = "magical"
        self.willpower_versus = 1
        self.willpower_math = 1
        self.willpower_cap = 50
        self.willpower_price = 1

        self.base_health = 100
        self.endurance_value = 10
        self.endurance_price = 3

        self.charisma_effect = "charisma_buff"
        self.charisma_math = 1
        self.charisma_cap = 33
        self.charisma_price = 1

        self.luck_calculation = 1
        self.luck_cap = 50
        self.luck_price = 1


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
        placehorder = 0

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

    return render_template('simulation.html', system=system)


if __name__ == '__main__':
    app.run()
