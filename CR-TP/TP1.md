<h2><b>1 Base de données</b></h2>
<h3><b>1.1 Spécifications de la base de données</b></h3>
<h3>Question 1</h3>
<p></p>Voici les explications du modèle relationnel de ma base de données correspondant au schéma montré à l'encadrant de TP :</p>
<ul>
<li>Un logement a plusieurs Pièces, chaque pièce est liée à un logement via la clé étrangère <b>id_loge</b>, relation 1:N.</li>
<li>Une pièce peut contenir plusieurs Capteurs et Actionneurs, un capteur est lié à une pièce via la clé étrangère <b>id_piece</b>, relation 1:N.</li>
<li>Un capteur peut avoir plusieurs mesures, une mesure est liée à un capteur via la clé étrangère <b>id_capteur</b>, relation 1:N.</li>
<li>Un capteur est lié à un Type_capteur via la clé étrangère <b>id_type</b>, relation N:1.</li>
</ul>
Il s'agit des relations entre les tables, les noms des colonnes de chaque table sont dans <b>logement.sql</b>.<br><br>
La table Actionneur a été rajoutée après cette étape, elle n'était pas encore présente lors de la validation.

<h3>Question 2</h3>
Pour détruire toutes les tables éventuellement présentes dans ma base j'ai utilisé le code :
<code>DROP TABLE IF EXISTS [Nom Table];</code><br>
pour chacune de mes tables.

<h3>Question 3</h3>
Chaque table a été créée avec le code suivant :<br>
<code>CREATE TABLE [Nom Table] (
    id_[Table] INTEGER PRIMARY KEY AUTOINCREMENT,  
    [champs...]                            
);</code> (voir <b>logement.sql</b>).
<h3>Question 4</h3>
Voir de la ligne 74 à la ligne 76 de <b>logement.sql</b>.<br>
Pour les questions 4 à 8 des codes similaires ont été utilisés, il s'agit de :<br>
<code>INSERT INTO [Table] ([noms des champs])
VALUES ([valeurs des champs]);</code>.

<h3>Question 5</h3>
Voir de la ligne 91 à la ligne 105 de <b>logement.sql</b>.

<h3>Question 6</h3>
Voir de la ligne 107 à la ligne 115 de <b>logement.sql</b>.

<h3>Question 7</h3>
Voir de la ligne 117 à la ligne 123 de <b>logement.sql</b>.<br>
Je n'ai rien inséré pour l'actionneur car il n'effectue pas de mesures.

<h3>Question 8</h3>
Voir de la ligne 132 à la ligne 144 de <b>logement.sql</b>.

<h3><b>1.2 Remplissage de la base de données</b></h3>
Voir le code dans le fichier remplissage.py.<br>
L'utilisation de la librarie sqlite3 permet de se connecter à la base
de données, grâce à la commande <code>conn = sqlite3.connect('logement.db')</code> puis  d'y exécuter des 
requêtes SQL pour insérer des données via <code>c.excute(query, données)</code> où query est la requête, <code>'''INSERT INTO Mesure (valeur, date_insert, id_capteur) VALUES (?, ?, ?)'''</code> par exemple.







