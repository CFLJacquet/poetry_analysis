# poetry_analysis
French poetry analysis using machine learning 

# Settings

## Installed libraries
Python 3.6

* *scrapy* : to get the poems from the site 
* *treetaggerwrapper* : text preprocessing (tokenization and lemmatization in French) 
http://treetaggerwrapper.readthedocs.io/en/latest/
* *sklearn* : text processing (TFIDF and clustering)


<<<<<<< HEAD

DATAMINNING

Règles d'association
Pourraient peut etre permettre de générer des implications tq :
    si on a "aimer", "mère" alors le thème est "amour maternel"
    {set de mots} --> {theme}

Filtrage collaboratif ou clustering
Retrouver des courants littéraires, des périodes historiques
Approche utilisateur/utilisateur ou model based
Test modèles latents ?

Classif
Ḿethodes baśees sur des arbres de d́ecision - existe dans nltk
Ḿethodes baśees sur des r`egles.
Ŕeseaux de neurones.
Ḿethodes baýesiennes
Machines à vecteurs support


A FAIRE
- Analyses grossières
Voir s'il y a des données qui manquent
- Le coeur du sujet

# Analyses ideas

* proximité entre auteurs
* clusterisation et découverte de similarité entre poèmes -> thèmes ? vocabulaire ?
* prédiciton période écriture

Index(['ID', 'author', 'book', 'link_poem', 'link_theme', 'text', 'theme',
       'title'],
      dtype='object')

jouer avec les normes pour les classifs