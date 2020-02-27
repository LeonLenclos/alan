De tête, peu de temps après avoir fait une install sur raspberry :


# Le bon python

Alan marche avec Python3.5 mais c'est con il ne marche pas avec les Python autour. donc il faut installer Python3.5

Si la commande `$ python --version` donne `Python 3.5.x` bravo ya rien a faire

Sinon si la commande `$ python3.5 --version` donne `Python 3.5.x` il faudra désormais écrire `python3.5` au lieu de `python` pour toutes les commandes dans le terminal

Sinon il faut installer python3.5 et écrire `python3.5` au lieu de `python` pour toutes les commandes dans le terminal

pour installer python3.5 :

    $ apt-get install python3.5

# Cloner le repo

    $ git clone https://github.com/LeonLenclos/alan.git

# Installer les dépendances 

Les instructions sur le readme devrait marcher.

Attention par contre que `pip` installe bien les librairies pour le bon python (3.5)

Je crois que un truc du genre `python3.5 -m pip install ...` est plus sûr que `pip install ...`

# Lancer alan

$ cd alan/brain
$ python3.5 server.py

aller à http://localhost:8000

# ça marche pas ya pas les packages

moi ça n'a pas marché du premier coup parce que il avait pas bien installé les dépendances (je crois que l'erreur c'est "cant import blablabla, blablabla not found")

donc faut réinstaller une par une les dependances qui manquent (**pour python3.5**)

# ok ça marche mais il parle bizar

c'est là que j'ai bloqué pendant qqs heures.

en gros il se comporte très bizarrement avec les accents. et les lettres spéciales.

L'idée c'est de taper 

    $ locales
    
et là si t'as pas une seule fois ecrit le mot "UTF-8" dans ce qui sors c'est que c'est de la merde. (merci ce monsieur : https://stackoverflow.com/a/60433169/8752259 )

donc pour avoir les bonnes locales je sais plus trop comment j'ai fait mais je crois que c'était avec `update-locale`. 

# Redémarer.

ça marche super.








