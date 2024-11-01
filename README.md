# Projet de Scraping de données d'un site de vente de livres en ligne

Ce programme permet de récupérer les données de tous les livres d'un site de vente de livres en ligne et de les stocker dans des fichiers csv.
La norme de nommage des fichiers csv est la suivante : catégorie + date, dans un dossier portant le nom de la catégorie. Pour chaque livre, on trouve les informations suivantes : url du livre, titre, UPC, prix HT, prix TTC, nombre de disponibilité, description, note, catégorie, url de l'image.
Les images sont téléchargées et stockées dans un dossier portant le nom "images_data", avec pour nom de chaque image le UPC du livre.
Le script est entièrement automatisé et fonctionne de manière incrémentale, mais ne surveille pas les prix en temps réel, il doit etre relancé manuellement pour une mise à jour.

## Prérequis

récupération du repository : https://github.com/CRX2B/scraping_project


## Installation

création d'un environnement virtuel python :

    python -m venv env
    env\Scripts\activate

installation des dépendances :

    pip install -r requirements.txt


## Execution du script

    rendez vous dans le dossier du projet
    python main.py


## Lecture des fichiers csv

    le script a du vous créer un dossier data dans lequel se trouve un dossier pour chaque catégorie avec pour nom la catégorie.
    les fichiers csv sont nommés : catégorie + date + .csv
    les images sont telechargés dans le dossier images_data et sont nommées : UPC + .jpg
    utilisez un tableur pour lire les fichiers csv
    Puis dans l'assistant importation de texte sélectionner les configurations suivantes :

        _ type de données d'origine (étape 1 sur 3) : Délimité
        _ Séparateur (étape 2 sur 3) : Virgule
        _ Format de données en colonne (étape 3 sur 3) : Standard
        _ Puis cliquer sur Terminer et OK




