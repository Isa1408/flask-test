# Projet de session
## A1
Cette fonctionnalité permet de télécharger et d'insérer les données dans la base de données grâce au lien fourni. Le script python se trouve dans le chemin suivant :
`scripts/contraventions.py` où la commande `python3 contraventions.py` pourra être tappé pour lancer le script. \
Dans le cas où la table n'est pas vide, nous pouvons nous déplacer au chemain suivant à partir de la racine du projet :
`db` où nous pourrons tapper la commande `sqlite3 db.db < db.sql` qui permettra de vider la base de donnée.

## A2
Tel que demandé, la page d'accueil offre un outil de recherche qui permet de trouver les contraventions par :
- nom d'établisssement
- propriétaire
- rue

Afin de tester cette fonctionnalité, il suffit d'être sur la page d'accueil et de saisir une donnée.

**Exemple d'entrée** : Rosemont

## A3
Un BackgroundScheduler a été ajouté dans le fichier `scripts/contraventions.py`. Ce BackgroundScheduler va lancer le script que nous avons fait dans la fonctionnalité *A1* à chaque jour, à minuit. \
Pour le tester, il suffit de se placer dans le chemin `scripts` et de lancer la commande `python3 contraventions.py`.

## A4
Ici, nous offrons un service REST permettant d'obtenir la liste des contraventions ayant été émises entre deux dates spécifiées en paramètre selon la convention ISO 8601. \
Pour le tester, il suffit de saisir l'URL suivant : `/contrevenants?du=2022-05-08&au=2024-05-15` et les résultats s'afficheront.
Pour consulter la documentation, nous pouvons saisir `/doc` ou cliquer sur le bouton `documentation` dans le menu. 

## A5
Un formulaire de recherche rapide de deux dates a été ajouté sur la page d'accueil. Pour le tester, vous pouvez sélectionner deux dates, par exemple `2024-09-10` et `2024-10-16` et cliquer sur le bouton `Rechercher`. Cette recherche va afficher dynamiquement un tableau de deux colonnes contenant le nom de l'établissement et son nombre de contraventions durant la période choisi.\
Pour notre exemple, il est attendu d'avoir onze établissements différents qui ont chacun une seule contravention sauf pour les établissements `Pizza Poulet New York` et `Second Cup Loyola` qui ont chacun deux contraventions.\
Aussi, il est possible de voir la requête AJAX qui a été faite en utilisant l'outil `Inspect` et en se dirigeant dans la section `Network`.

## A6
Une liste déroulante a été ajoutée à côté du formulaire de recherche rapide par dates. Cette liste affiche les différents établissements qui ont reçus des contraventions entre ces dates. Cependant, il est un filtre optionnel.\
Le fonctionnement est le suivant : l'utilisateur sélectionne deux dates et une liste de tous les établissements qui ont reçu une contravention entre ces dates s'afficheront.\
Par exemple, vous pouvez sélectionner les dates `2024-09-10` et `2024-09-11` et les établissements `PIZZA POULET NEW YORK` et `GIULIETTA PIZZERIA` s'afficheront. En sélectionnant un de ces deux choix et que vous cliquez sur le bouton `Rechercher`, un tableau de deux colonnes contenant le nom de l'établissement et son nombre de contraventions s'afficheront.\
Dans le cas où aucune date n'est sélectionnée ou que la date est éronnée, la liste déroulante n'affichera aucun établissement. Aussi, un message d'erreur s'affichera quand l'utilisateur clique sur le bouton `Rechercher`.

## C1
Il est possible d'obtenir la liste des établissements ayant commis une ou plusieurs infractions en format JSON. Pour chaque établissement, on indique le nombre d'infractions connues dans une liste triée en ordre décroissant du nombre d'infractions.\
Pour y accéder, il suffit de naviguer à l'URL suivant : `/contrevenants.json`.\
Pour consulter la documentation, nous pouvons naviguer vers `/doc` ou cliquer sur le bouton `documentation` dans le menu. 

## C2
Il est possible d'obtenir la liste des établissements ayant commis une ou plusieurs infractions en format XML. Pour chaque établissement, on indique le nombre d'infractions connues dans une liste triée en ordre décroissant du nombre d'infractions.\
Pour y accéder, il suffit de naviguer à l'URL suivant : `/contrevenants.xml`.\
Pour consulter la documentation, nous pouvons naviguer vers `/doc` ou cliquer sur le bouton `documentation` dans le menu. 

## C3
Il est possible d'obtenir la liste des établissements ayant commis une ou plusieurs infractions en format CSV. Pour chaque établissement, on indique le nombre d'infractions connues dans une liste triée en ordre décroissant du nombre d'infractions.\
Pour y accéder, il suffit de naviguer à l'URL suivant : `/contrevenants.csv` où le fichier sera automatiquement téléchargé.\
Pour consulter la documentation, nous pouvons naviguer vers `/doc` ou cliquer sur le bouton `documentation` dans le menu. 
