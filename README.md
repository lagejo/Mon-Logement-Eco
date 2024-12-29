<h2><b>Présentation de l'archive :</b></h2>

Vous avez ici tous les fichiers permettant d'utiliser le site web Mon-Logement-Eco sur votre marchine.<br>
Le framework web FastAPI a été utilisé pour réaliser l'interface web, le fichier <b>main.py</b> contient l'application FastAPI, les routes et les fonctions principales pour gérer les requêtes HTTP.

<p>Dans le dossier templates, il y a les différentes pages du site :</p>
<ul>
	<li><b>base.html</b> le template de base pour toutes les pages qui définit la structure HTML des autres pages,</li>
	<li><b>conso.html</b> la page de gestion des factures,</li>
	<li><b>config.html</b> la page pour la configuration des capteurs, actionneurs, types de capteurs, pièces, et logements,</li>
	<li><b>etat_capteur.html</b> la page pour afficher l'état des capteurs et actionneurs,</li>
	<li><b>eco.html</b> la page pour afficher les économies réalisées,</li>
	<li><b>accueil.html</b> la lage d'accueil de l'application.</li>
</ul>
Le dossier static contient les feuilles de style CSS et les scripts JavaScript qui étaient trop longs pour être laissés dans les fichiers html, ainsi que les images/logo utilisés.
Dans le dossier <b>capteurs-actionneurs</b> les fichiers <b>code_esp_actionneur.cpp</b> et <b>code_esp_capteur.cpp</b> contiennent les codes utilisés pour tester un capteur/actionneur. 
Ces codes sont conçus pour être implémentés dans un ESP8266 relié à une LED et à un capteur de température et d'humidité, le dht11.
La base de données utilisée est <b>logement.db</b>, elle a été au départ remplie avec le code contenu dans <b>logement.sql</b>.<br>
Afin ne pas surcharger le fichier main, quelques fonctions permettant l'acquisition ou l'écriture d'éléments de la base de données ont été placées dans <b>utils.py</b>.

<h2><b>Pour lancer Mon-Logement-Eco :</b></h2>
Dépendances nécessaires : fastapi, unicorn, jinja2, pydantic.<br>
Elles peuvent être installées simplement avec la commmande : pip install fastapi uvicorn jinja2 pydantic.<br>
Après le téléchargement de l'archive, il suffit de lancer la commande : <mark>fastapi run main.py</mark> dans le dossier <b>Mon-logement-eco</b>.<br>
Il faut ensuite se rendre à l'adresse <a href=http://127.0.0.1:8000/>http://127.0.0.1:8000/</a> en utilisant votre navigateur internet.
