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
import re


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
    return render_template('home.html', animaux_select=animaux_random)

@app.route('/animal/<int:id_animal>', defaults={'created': False})
@app.route('/animal/<int:id_animal>/<created>')
def animal_details(id_animal, created):
    animaux_adoptables = recuperer_animaux()
    animal_concerné = animaux_adoptables[id_animal-1]
    return render_template("animal.html", animal=animal_concerné, created=created)


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


@app.route('/recherche', methods=['GET'])
def recherche():
    # mode_recherche = int(request.args.get('mode_recherche'))
    # mot_recherchee = str(request.args.get('mot_recherchee')).replace(' ', '')

    mots_recherche = str(request.args.get('mot_recherchee')).strip().split()

    criteres = list(filter(lambda x: len(x) > 0, mots_recherche))
    criteres = list(map(lambda x: x.lower(), criteres))

    animaux_adoptables = recuperer_animaux()
    animaux_a_lister = []
    for animal in animaux_adoptables:
        matches = 0
        for critere in criteres:
            if critere in animal['nom'].lower() or critere in animal['espece'].lower() or critere in animal['race'].lower() or critere in animal['description'].lower() or critere in animal['ville'].lower():
                matches = matches + 1
        if matches == len(criteres):
            animaux_a_lister.append(animal)


    # mot_recherchee = mot_recherchee.lower()
    # animaux_a_lister = []
    # animaux_adoptables = recuperer_animaux()
    # animaux_a_lister = recherche_par_attribut(
    #     mode_recherche,
    #     animaux_adoptables,
    #     mot_recherchee
    # )
    return render_template('search.html', animaux_select=animaux_a_lister)


@app.route('/formulaire')
def formulaire():
    animal = empty_animal()
    return render_template('form.html', animal=animal, errors=[])


@app.route('/envoyer', methods=['POST'])
def soumission():
    errors = valider_formulaire(request.form)
    if len(errors) > 0 :
        animal = map_animal(request.form)
        return render_template('form.html', animal=animal, errors=errors)

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
    return redirect(url_for('animal_details', id_animal=id_added, created=True))


def valider_formulaire(form):
    errors = []

    if "nom" not in form or len(form["nom"]) == 0 :
        errors.append("Le nom de l'animal est requis.")
    elif len(form["nom"]) < 3 or len(form["nom"]) > 20 :
        errors.append("Le nom de l'animal doit avoir entre 3 et 20 caractères.")
    elif "," in form["nom"] :
        errors.append("Le nom de l'animal ne peut contenir une virgule.")

    if "espece" not in form or len(form["espece"]) == 0 :
        errors.append("L'espéce de l'animal est requise.")
    elif "," in form["espece"] :
        errors.append("L'espéce de l'animal ne peut contenir une virgule.")

    if "race" not in form or len(form["race"]) == 0 :
        errors.append("La race de l'animal est requise.")
    elif "," in form["race"] :
        errors.append("La race de l'animal ne peut contenir une virgule.")

    if "age" not in form or len(form["age"]) == 0 :
        errors.append("L'age de l'animal est requis.")
    else:
        try:
            age = int(form["age"])
            if age < 0 or age >= 30 :
                errors.append("L'age de l'animal doit être une valeur numérique entre 0 et 30.")
        except:
            errors.append("L'age de l'animal doit être une valeur numérique valide.")

    if "description" not in form or len(form["description"]) == 0 :
        errors.append("La description de l'animal est requise.")
    elif "," in form["description"] :
        errors.append("La description de l'animal ne peut contenir une virgule.")

    if "courriel" not in form or len(form["courriel"]) == 0 :
        errors.append("Le courriel est requis.")
    elif not re.fullmatch('^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$', form["courriel"]) :
        errors.append("Le courriel est en format non valide.")
    elif "," in form["courriel"] :
        errors.append("Le courriel ne peut contenir une virgule.")

    if "adresse" not in form or len(form["adresse"]) == 0 :
        errors.append("L'adresse est requise.")
    elif "," in form["adresse"] :
        errors.append("L'adresse ne peut contenir une virgule.")

    if "ville" not in form or len(form["ville"]) == 0 :
        errors.append("La ville est requise.")
    elif "," in form["ville"] :
        errors.append("La ville ne peut contenir une virgule.")

    if "cp" not in form or len(form["cp"]) == 0 :
        errors.append("Le code postal est requis.")
    elif not re.fullmatch('^[A-Za-z][0-9][A-Za-z] [0-9][A-Za-z][0-9]$', form["cp"]) :
        errors.append("Le code postal est en format non valide.")
    elif "," in form["cp"] :
        errors.append("Le courriel ne peut contenir une virgule.")
        
    return errors

def empty_animal():
    return {
        'nom' : '',
        'espece' : '',
        'race' : '',
        'age' : '',
        'description' : '',
        'courriel' : '',
        'adresse' : '',
        'ville' : '',
        'cp' : ''
    }

def map_animal(form):
    animal = {
        'nom' : form.get('nom', ''),
        'espece' : form.get('espece', ''),
        'race' : form.get('race', ''),
        'age' : form.get('age', ''),
        'description' : form.get('description', ''),
        'courriel' : form.get('courriel', ''),
        'adresse' : form.get('adresse', ''),
        'ville' : form.get('ville', ''),
        'cp' : form.get('cp', '')
    }
    return animal