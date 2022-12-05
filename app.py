from flask import Flask, request, render_template, redirect, url_for

from arena import Arena
from classes import unit_classes, Unit
from equipment import Equired
from unit import Player, Enemy

heroes = {
    "player": Player,
    "enemy": Enemy,
}
app = Flask(__name__)

arena = Arena()


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    equipment = Equired()
    weapons = equipment.get_weapon_names()
    armors = equipment.get_armors_names()
    classes = unit_classes

    if request.method == "GET":

        result = {
            'header': "Выберите героя",
            'classes': classes,
            'weapons': weapons,
            'armors': armors
        }

        return render_template('hero_choosing.html', result=result)
    elif request.method == 'POST':
        name = request.form['name']
        armor_name = request.form['armor']
        weapon_name = request.form['weapon']
        unit_class = request.form['unit_class']
        class_person: Unit = unit_classes[unit_class]
        player = Player(nickname=name, class_person=class_person, armor=equipment.get_armor(armor_name),
                        weapon=equipment.get_weapon(weapon_name), health_point=class_person.max_health,
                        stamina_point=class_person.max_stamina, attack=class_person.attack)
        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    equipment = Equired()
    weapons = equipment.get_weapon_names()
    armors = equipment.get_armors_names()
    classes = unit_classes

    if request.method == "GET":

        result = {
            'header': "Выберите противника",
            'classes': classes,
            'weapons': weapons,
            'armors': armors
        }

        return render_template('hero_choosing.html', result=result)
    elif request.method == 'POST':
        name = request.form['name']
        armor_name = request.form['armor']
        weapon_name = request.form['weapon']
        unit_class = request.form['unit_class']
        class_person: Unit = unit_classes[unit_class]
        enemy = Enemy(nickname=name, class_person=class_person, armor=equipment.get_armor(armor_name),
                      weapon=equipment.get_weapon(weapon_name), health_point=class_person.max_health,
                      stamina_point=class_person.max_stamina, attack=class_person.attack)
        heroes['enemy'] = enemy
    return redirect(url_for('start_game'))


@app.route("/fight/")
def start_game():
    arena.start(heroes["player"], heroes["enemy"])

    return render_template("fight.html", heroes=heroes)


@app.route("/fight/hit")
def deal_damage():
    if arena.match_start:
        result = arena.hit_player()
    else:
        result = arena.battle_result
    return render_template("fight.html", heroes=arena, result=result, battle_result=arena.battle_result)


@app.route("/fight/use-skill")
def skill_use():
    if arena.match_start:
        result = arena.use_skill()
    else:
        result = arena.battle_result

    return render_template("fight.html", heroes=arena, result=result, battle_result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.match_start:
        result = arena.next_round()
    else:
        result = arena.battle_result

    return render_template("fight.html", heroes=arena, result=result, battle_result=arena.battle_result)


@app.route("/fight/end-fight")
def end_game():
    return render_template("index.html")
