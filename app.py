# Copyright 2023 <Votre nom et code permanent>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, request, redirect, url_for
from flask import render_template
from flask import g
from .database import Database
import random
import os


app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


def recuperer_animaux():
    db = Database()
    animaux_adoptables = db.get_animaux()
    db.disconnect()

    return animaux_adoptables


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def form():
    animaux_adoptables = recuperer_animaux()
    animaux_random = random.sample(animaux_adoptables, 5)
    return render_template('index.html', animaux_select=animaux_random)


@app.route('/animal/<int:id_animal>')
def details_animal(id_animal):
    directory = 'templates/'
    os.path.join(directory, f'{id_animal}.html')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('templates/' + str(id_animal) + '.html', 'w') as file:
        contenu_html = "{% extends 'animal_base.html' %}"
        file.write(contenu_html)
    nom_template = str(id_animal) + ".html"
    animaux_adoptables = recuperer_animaux()
    animal_concerné = animaux_adoptables[id_animal-1]
    return render_template(nom_template, animal=animal_concerné)


def filtrer_animaux_par_attribut(animaux_adoptables, mot_recherchee, attribut):
    animaux_a_lister = []
    for animal in animaux_adoptables:
        animal_attribut = str(animal[attribut]).lower()
        if mot_recherchee in animal_attribut:
            animaux_a_lister.append(animal)
    return animaux_a_lister


def recherche_par_attribut(mode_recherche, animaux_adoptables, mot_recherchee):
    switch = {
        1: 'espece',
        2: 'race',
        3: 'ville'
    }
    attribut = switch.get(mode_recherche)
    return filtrer_animaux_par_attribut(
        animaux_adoptables,
        mot_recherchee,
        attribut
    )


@app.route('/search', methods=['GET'])
def recherche():
    mode_recherche = int(request.args.get('mode_recherche'))
    mot_recherchee = str(request.args.get('mot_recherchee')).replace(' ', '')
    mot_recherchee = mot_recherchee.lower()
    animaux_a_lister = []
    animaux_adoptables = recuperer_animaux()
    animaux_a_lister = recherche_par_attribut(
        mode_recherche,
        animaux_adoptables,
        mot_recherchee
    )
    return render_template('recherche.html', animaux_select=animaux_a_lister)


@app.route('/formulaire')
def formulaire():
    return render_template('formulaire.html')


@app.route('/envoyer', methods=['POST'])
def soumission():
    db = Database()
    id_added = db.add_animal(
        request.form['nom'],
        request.form['espece'],
        request.form['race'],
        request.form['age'],
        request.form['description'],
        request.form['courriel'],
        request.form['adresse'],
        request.form['ville'],
        request.form['cp']
    )
    return redirect(url_for('details_animal', id_animal=id_added))
