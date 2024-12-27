Présentation de l'archive : 
Vous avez ici tous les fichiers permettant d'utiliser le site web Mon-Logement-Eco en local sur votre marchine.
Le framework web FastAPI a été utilisé pour réaliser l'interface web, le fichier main.py contient l'application FastAPI, les routes et les fonctions principales pour gérer les requêtes HTTP.
Dans le dossier templates, il y a les différentes pages du site : 
    - base.html le template de base pour toutes les pages qui définit la structure HTML des autres pages,
    - conso.html la page de gestion des factures,
    - config.html Page pour la configuration des capteurs, actionneurs, types de capteurs, pièces, et logements,
    - etat_capteur.html l page pour afficher l'état des capteurs et actionneurs,
    - eco.html la page pour afficher les économies réalisées,
    - index.html la lage d'accueil de l'application.
Le dossier static contient les fichiers statiques tels que les feuilles de style CSS et les scripts JavaScript qui étaient trop longs pour être laissés dans les fichiers html.
Les fichiers code_esp_actionneur.cpp et code_esp_capteur.cpp contiennent les codes C++ utilisés pour utiliser un capteur/actionneur. 
Ces codes sont conçus pour être implémentés dans un ESP8266 relié à une LED et à un caoteur de température et d'humidité, le dht11.
Description: Dossier contenant les fichiers statiques tels que les feuilles de style CSS et les scripts JavaScript.
Afin ne pas surcharger le fichier main, quelques fonctions permettant l'acquisition ou l'écriture d'éléments de la base de données ont été placées dans utils.py.
