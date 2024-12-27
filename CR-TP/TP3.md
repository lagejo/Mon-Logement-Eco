<h2><b>3 HTML/CSS/Javascript</b></h2>

<h3>1. Consommation (électricité, eau, déchets etc.) du logement sous forme de graphiques selon
différentes échelles de temps</h3>
Description du fonctionnement de la page :<br><br>

Cette page étend le template de base base.html en utilisant <code>{% extends "base.html" %}</code>.
Les blocs <code>{% block content %}</code> sont utilisés pour définir le contenu principal de la page.<br><br>

La page affiche le montant total des factures si des factures sont disponibles (<code>{% if has_factures %}</code>).
Deux graphiques sont utilisés pour visualiser les données des factures : un graphique en camembert et un graphique d'évolution.<br><br>

Les graphiques sont générés en utilisant la bibliothèque Google Charts.
Les données des graphiques sont passées dynamiquement depuis le backend en utilisant Jinja2 pour insérer les valeurs dans le JavaScript.<br><br>

La bibliothèque Google Charts est chargée en utilisant une balise <script> avec l'URL https://www.gstatic.com/charts/loader.js.<br>

La fonction <b>drawCharts()</b> à la ligne 57 de <b>conso.html</b> est appelée lorsque la bibliothèque Google Charts est prête.<br>
Elle appelle à son tour <b>drawPieChart()</b> et <b>drawEvolutionChart()</b> aux ligne 62 et 96 de <b>conso.html</b> pour dessiner les graphiques.
La fonction <b>drawPieChart()</b> crée un graphique en camembert pour afficher la répartition des montants des factures par type, et la fonction <b>drawEvolutionChart()</b> crée un graphique d'évolution pour afficher l'évolution des consommations au fil du temps.

<h3>2. état des différents capteurs/actionneurs,</h3>
Description du fonctionnement de la page :<br><br>

Cette page affiche deux sections principales : "Capteurs Actifs" et "Actionneurs".<br>
Chaque section contient un tableau HTML (table) pour lister les capteurs et actionneurs avec leurs détails respectifs.<br><br>

Chaque capteur a un bouton "Afficher Mesures" qui permet de charger et afficher les mesures du capteur, chaque actionneur a un bouton "Allumer LED" qui permet d'envoyer une requête pour allumer la LED de l'actionneur.<br><br>

Les bibliothèques <b>Chart.js</b> et <b>Luxon</b> sont chargées en utilisant des balises script avec les URLs correspondantes pour pouvoir gérer les formats de dates dans les graphes.<br><br>

La fonction <b>loadGraph(capteurId)</b> à la ligne 99 envoie une requête HTTP GET pour récupérer les mesures d'un capteur et les affiche dans un graphique.<br>
La fonction <b>allumerLed(actionneurId)</b> envoie une requête HTTP POST pour allumer la LED d'un actionneur.

<h3>3. économies réalisées sous forme de comparatifs (graphiques) selon différentes échelles de
temps</h3>
Description du fonctionnement de la page :<br><br>

La page contient des formulaires pour sélectionner un logement et un type de facture.
Les éléments <b>select</b> et <b>option</b> sont utilisés pour permettre à l'utilisateur de faire des sélections.<br><br>

La page affiche des graphiques pour visualiser les économies réalisées et des messages pour informer l'utilisateur si les données sont insuffisantes pour une comparaison.<br>

Il y a également un bouton qui permet de naviguer vers la page de consommation globale des logements.<br><br>

La fonction <b>loadFactureTypes(logementId)</b> à la ligne 3 de <b>facture.js</b> est appelée lorsque l'utilisateur sélectionne un logement. Elle envoie une requête HTTP GET pour récupérer les types de factures disponibles pour le logement sélectionné.<br>

La fonction <b>loadGraph(factureTypeId)</b> à la ligne 60 de <b>facture.js</b> est appelée lorsque l'utilisateur sélectionne un type de facture. Elle envoie une requête HTTP GET pour récupérer les données des factures et les affiche dans des graphiques.

<h3>4. configuration : paramètres utilisateur, ajout de capteurs/actionneurs, etc.</h3>
Description du fonctionnement de la page :<br><br>
Comme les autres pages cette page étend le template de base <b>base.html</b> en utilisant <code>{% extends "base.html" %}</code>.<br><br>

Plusieurs boutons de menu permettent de sélectionner différentes actions de configuration, telles que l'ajout de capteurs, actionneurs, types de capteurs, pièces et logements.
Chaque formulaire est contenu dans un div avec un id unique et est initialement caché (<code>style="display:none;"</code>).<br>
La fonction en javascript <code>function showForm(formId)</code> contenue dans <b>static/js/script.js</b> permet d'afficher les formulaires lorsqu'ils sont sélectionnés par le bouton correspondant.<br>
Par exemple lorsque "Ajouter un capteur" est cliqué, le formulaire d'ajout du capteur s'affiche.<br><br>

Le formulaire d'ajout de capteur utilise des éléments HTML5 tels que <select> et <option> pour permettre à l'utilisateur de sélectionner un logement et une pièce.
L'attribut required est utilisé pour s'assurer que les champs obligatoires sont remplis avant la soumission du formulaire.
