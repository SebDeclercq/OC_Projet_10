# Openclassrooms : DA Python : P8

## Contexte

Ce repo contient l'ensemble des développements réalisés pour le projet 8 du parcours DA Python d'Openclassrooms. L'objectif du projet est de créer un site web pour la société PurBeurre, répondant à un cahier des charges très précis.

## Présentation

### Organisation

Le projet Django PurBeurre contient diverses applications afin de mener les actions requises. Ces applications sont :
- **App** : l'application centrale
- **Favorite** : l'application permettant la sauvegarde des favoris préférés
- **Food** : l'application se chargeant des produits en eux-mêmes
- **OpenFoodFacts** : une application ne contenant qu'une commande *custom* permettant l'alimentation de la base de données
- **Testing** : une application ne contenant qu'une commande *custom* permettant de générer des rapports de couverture de tests (avec `coverage`)
- **User** : l'application se chargeant de la gestion des comptes utilisateurs

Chaque application, à l'exception de celles ne contenant qu'une commande *custom*, sont composées de fichiers dédiés
1. aux modèles
2. aux vues
3. aux tests, qui sont présentés dans des fichiers dédiés selon leur cible (modèles ou vues).

### Déploiement

La définition des variables d'environnement suivantes est requise pour permettre le bon déploiement du projet :

- `db_user` : le nom de l'utilisateur pour la base de données
- `db_pass` : le mot de passe pour l'utilisateur

La base de données attendue est une base PostgreSQL nommée `purbeurre`.

Le déploiement sur heroku est facilité grâce à la présence du fichier `Procfile` requis ainsi que de l'emploi du *package* `django-heroku`. Il est néanmoins nécessaire de définir la variable d'environnement `HEROKU` à 1 afin de permettre le déploiement effectif sur la plateforme.

### Tests

Il est possible de jouer l'ensemble des tests à l'aide de la commande `python manage.py test` mais la commande *custom* `python manage.py coverage` permet de lancer ces mêmes tests tout en générant un rapport de couverture de tests. En passant l'option `--html`, un rapport HTML sera généré.
