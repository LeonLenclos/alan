# Alan v1.2.0



[Le dépôt github de Alan](https://github.com/LeonLenclos/alan) est consacré au code source d'alan.

## Description

Alan est un agent conversationel en cours de développement créé pour le spectacle [Turing Test](https://github.com/LeonLenclos/turing-test) avec la collaboration de l'[IRIT](https://www.irit.fr/) (Institut de Recherche en Informatique de Toulouse) et plus particulièrement des équipes de recherche SAMoVA et MELODI. C'est un robot spécialisé dans la communication verbale, conçu pour donner l'illusion d'être conscient.
On peut discuter avec lui de choses et d'autres mais sa spécialité c'est la conscience de soi. Il a été programmé pour donner l'illusion qu'il est conscient d'exister. Vous trouverez plus d'informations sur le git du spectacle https://github.com/LeonLenclos/turing-test/blob/master/contenu/robots/alan.md

![](https://github.com/LeonLenclos/turing-test/ressources/dessin1.png)


## Fonctionnement

L'architecture d'Alan est basé sur le module python [chatterbot](https://github.com/gunthercox/ChatterBot). Le programme d'Alan est ainsi composé de modules, des bouts de programmes qui répondent à des taches précises :
- Des modules servant à générer en fonction d'un texte entré par l'utilisateur une réponse sous forme de texte en fonction et un indice de confiance. Il sont appelés des LogicAdapter.
- Un module servant à gérer la reconnaissance vocale (conversion voix vers texte) sera un InputAdapter
- Un module servant à gérer la synthèse vocale (conversion texte vers voix) sera un OutputAdapter

Lorsque l'utilisateur dis quelque-chose à Alan, certains logic adapters se mettront en marche et c'est la réponse de celui qui renverra l'indice de confiance le plus haut qui sera sélectionnée. Si tout les logic adapters ne se mettent pas en marche à chaque fois, c'est parce que certains ne sont conçus que pour répondre à un certain type de phrases.

## Comment parler avec Alan

**Version de python requise : Python 3.5**

Le projet est encore en cours de développement, github est un outil adapté à ce contexte : il existe plusieurs "branches" qui sont des versions plus ou moins avancées d'Alan. Le Alan contenu dans la branche `master` doit normalement pouvoir fonctionner, il en est pour l'instant à la version 1. Il existe par exemple une branche développement sur laquelle nous travaillons et qui peut donc contenir un certain nombre de problèmes pas encores résolus. En attendant de pouvoir parler avec Alan sur internet vous pouvez suivre les indications suivantes pour installer Alan sur votre ordinateur ! Tout d'abord il vous faut télécharger ce dossier git en cliquant sur clone or download, puis rentrer les commandes suivantes dans le terminal depuis le dossier alan :


```
  $ pip install -r requirements.txt
  $ python
  >>> import nltk
  >>> nltk.download("punkt")
  >>> quit()
  $ cd brain
  $ ./alan.py
  ```
#### installer pyenchant sur mac

```
 $ brew install enchant --with-python
 $ export PYENCHANT_LIBRARY_PATH=/usr/local/opt/enchant/lib/libenchant-2.dylib

```
puis telecharger la [source](https://github.com/rfk/pyenchant)
```
 $ python3 setup.py install
```

#### installer le dictionnaire francais sous linux

```
 $ sudo apt-get install myspell-fr-fr
```
### indiquer des fichiers de réglage spécifique

Par defaut, alan se lance avec les réglages contenu dans le fichier default.json.

D'autres fichier de réglages (settings) peuvent être choisis grace à l'argument `-s`.

```
 $ ./alan.py -s speak
 # lance Alan avec les réglages contenus dans le fichier speak.json
 $ ./alan.py -s base interface_text logic_rive
 # lance Alan avec les réglages contenus dans les fichier base.json interface_text.json et logic_rive.json
 ```

Voir [brain/settings/README.md](brain/settings/README.md) pour plus d'information sur le fonctionnement des fichiers settings


### commandes spéciales

- Pour quitter `> ciao`
- Pour une annalyse des logic adapters en jeu dans la dernière réponse `> info`
- Pour noter les deux dernières répliques dans la liste todo.md `> todo`
- Pour redémarrer `> rst`
