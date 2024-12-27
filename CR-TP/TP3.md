<h2><b>3 HTML/CSS/Javascript</b></h2>

<h3>1. Consommation (électricité, eau, déchets etc.) du logement sous forme de graphiques selon
différentes échelles de temps</h3>

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

<h3>3. économies réalisées sous forme de comparatifs (graphiques) selon différentes échelles de
temps</h3>

<h3>4. configuration : paramètres utilisateur, ajout de capteurs/actionneurs, etc.</h3>
Description du fonctionnement de la page :<br><br>
Comme les autres pages cette page étend le template de base <b>base.html</b> en utilisant <code>{% extends "base.html" %}</code>.<br><br>

Plusieurs boutons de menu permettent de sélectionner différentes actions de configuration, telles que l'ajout de capteurs, actionneurs, types de capteurs, pièces et logements.
Chaque formulaire est contenu dans un div avec un id unique et est initialement caché (<code>style="display:none;"</code>). 
La fonction en javascript <code>function showForm(formId)</code> contenue dans <b>static/js/script.js</b> permet d'afficher les formulaires lorsqu'ils sont sélectionnés par le bouton correspondant.<br>
Par exemple lorsque "Ajouter un capteur" est cliqué, le formulaire d'ajout du capteur s'affiche.<br><br>

Le formulaire d'ajout de capteur utilise des éléments HTML5 tels que <select> et <option> pour permettre à l'utilisateur de sélectionner un logement et une pièce.
L'attribut required est utilisé pour s'assurer que les champs obligatoires sont remplis avant la soumission du formulaire.
