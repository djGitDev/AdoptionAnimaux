
function modifier_indicateur_recherche(value) {
    var valeur = parseInt(value);
    switch(valeur){
    case 1:
        document.getElementById('recherche').placeholder = "Saisir l'espace de l'animal...";
        break;
    case 2:
        document.getElementById('recherche').placeholder = "Saisir la race de l'animal...";
        break;
    case 3 :
        document.getElementById('recherche').placeholder = "Saisir la localisation de l'animal...";
        break;
    }
}

function valider_nom(nom){
    if (nom.value.length < 3 || nom.value.length > 20) {
        nom.classList.add('is-invalid');
        nom.classList.remove('is-valid');
        document.getElementById('valid_nom').style.display = 'none'
        document.getElementById('erreur_nom').style.display = 'block'

    } else {
        nom.classList.remove('is-invalid');
        nom.classList.add('is-valid');
        document.getElementById('valid_nom').style.display = 'block'
        document.getElementById('erreur_nom').style.display = 'none'
    }
}

function valider_age(age){
    if (age.value === '' || isNaN(age.value) || parseInt(age.value) < 0 || parseInt(age.value) > 30) {
        age.classList.add('is-invalid');
        age.classList.remove('is-valid');
        document.getElementById('valid_age').style.display = 'none'
        document.getElementById('erreur_age').style.display = 'block'
     } else {
        age.classList.remove('is-invalid');
        age.classList.add('is-valid');
        document.getElementById('valid_age').style.display = 'block'
        document.getElementById('erreur_age').style.display = 'none'
    }     
}

function valider_adresse_mail(email){
     if (!email.checkValidity()) {
         email.classList.add('is-invalid');
         email.classList.remove('is-valid');
         document.getElementById('valid_email').style.display = 'none'
         document.getElementById('erreur_email').style.display = 'block'

     } else {
         email.classList.remove('is-invalid');
         email.classList.add('is-valid');
         document.getElementById('valid_email').style.display = 'block'
         document.getElementById('erreur_email').style.display = 'none'
     }
}

function valider_code_postal(codePostal){
    var codePostalRegex = /^[A-Za-z][0-9][A-Za-z] [0-9][A-Za-z][0-9]$/;
    if (!codePostalRegex.test(codePostal.value)) {
        codePostal.classList.add('is-invalid');
        codePostal.classList.remove('is-valid');
        document.getElementById('valid_code_postal').style.display = 'none'
        document.getElementById('erreur_code_postal').style.display = 'block'
    } else {
        codePostal.classList.remove('is-invalid');
        codePostal.classList.add('is-valid');
        document.getElementById('valid_code_postal').style.display = 'block'
        document.getElementById('erreur_code_postal').style.display = 'none'
    }
}

function valider_champ_pas_vide(champ,id_erreur,id_valid){

    if (champ.value.trim().length === 0) {
       champ.classList.add('is-invalid');
       champ.classList.remove('is-valid');
       id_valid.style.display = 'none'
       id_erreur.style.display = 'block'
     } else {
         champ.classList.remove('is-invalid');
         champ.classList.add('is-valid');
         id_valid.style.display = 'block'
         id_erreur.style.display = 'none'
     }
}
function tous_champs_valides() {
    const champs = document.querySelectorAll('#monFormulaire .is-valid');
    return champs.length === document.querySelectorAll('#monFormulaire input').length;
}

