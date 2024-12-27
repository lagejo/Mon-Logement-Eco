<h2><b>2 Serveur RESTful</b></h2>
<h3>2.1 Exercice 1 : remplissage de la base de données</h3>
Dans mon site, j'ai utilisé des requêtes POST pour rajouter des éléments dans la base de données.<br>
Par exemple pour rajouter un capteur j'ai créé le chemin /add_capteur, voir de la ligne 31 à la ligne 45 de <b>main.py</b>,
que j'ai relié au bouton "Ajouter un capteur" dans la page de configuration, voir de la ligne 17 à la ligne 53 de <b>config.html</b>.<br><br>

La fonction :<br> <code>async def add_capteur(ref_commerciale: str = Form(...), port_communication: str = Form(...), type_capteur: int = Form(...), piece: int = Form(...))
</code> permet de récupérer les données du form complété et de les écrire dans la base de données via les mêmes instruction de sqlite3 que celles utilisées dans <b>remplissage.py</b>,
sqlite3.connect, c.execute...

Pour ce qui est des requêtes GET servant à consulter ma base de données, je les ai utilisées à plusieurs reprises,
par exemple dans la page de configuration, pour afficher les pièces existantes dans un logment.<br> Cette requête est à l'adresse /get_pieces
, le code correspondant est à la ligne 235 du fichier <b>main.py</b>, les fonction de sqlite3 permettent de récupérer les pièces correspondant au logement d'id id_loge via la commande
<code>"SELECT id_piece, nom FROM Piece WHERE id_loge = ?"</code>.<br><br>
Un objet json est ensuite renvoyé à la fonction loadPiece(logementId) (<b>config.html</b>, ligne 367) qui avait au préalable déclenché l'exécution de la fonction présente au chemin /get_pieces,
en transmettant l'id du logement sélectionné.<br>
Cela a été effectué grâce à l'instruction <code>fetch(`/get_pieces?logement_id=${logementId}`)</code> qui envoie une requête HTTP GET à l'URL /get_pieces avec le paramètre logement_id.

<h3>2.2 Exercice 2 : serveur web</h3>
J'ai utilisé cette partie du TP dans la page consommation, le code de la requête GET correspondante est à la ligne 159 de <b>main.py</b>, 
mais le code présent dans le main concerne le reformatage des données récupérées des fonctions get_factures() et get_logments() aux lignes 20 et 146 de <b>utils.py</b>.<br><br>

Le code formaté est transmis à la page de consommation via les ligne 221 à 232, sous forme de template grâce au code <code>return templates.TemplateResponse("conso.html",{...})</code>.<br>
Puis dans <b>conso.html</b>, des lignes 51 à 91, le code javascript correspondant au camebert de Google Charts récupère les données du template pour les afficher, je me suis aidé du tutoriel de google :
https://developers.google.com/chart/interactive/docs/gallery/piechart pour réaliser ce code.<br> Les fonctions javascript de google situées à l'adresse "></script>
        https://www.gstatic.com/charts/loader.js sont utilisées (importées à la ligne 52).

<h3>2.3 Exercice 3 : météo</h3>
Pour obtenir les données de météo j'ai utilisé le site openweathermap, où j'ai pu créer un compte gratuitement.<br>
Pour avoir accès aux données météo via une requête à l'url : https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric.
J'ai choisi comme lattitude = 48.8566 et comme longitude = 2.3522, ce qui correspond aux coordonnées de Paris, voir de la ligne 156 à la ligne 167 de <b>utils.py</b>.<br>
J'ai utilisé cette partie du TP dans la page d'accueil, j'utilise les données météo récupérées de la ligne 14 à la ligne 28 de <b>index.html</b>, ces données sont transmises via le GET de la racine du site, ligne 104 de <b>main.py</b>.
<h3>2.4 Exercice 4 : intégration</h3>
