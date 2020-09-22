# Alan v1.5.2


## Description

Alan est un agent conversationel créé pour le spectacle [Turing Test](https://github.com/LeonLenclos/turing-test) par Léon Lenclos, Fabien Carbo-Gil et Bertrand Lenclos de la [cie Nokill](http://cienokill.fr) avec la collaboration de l'[IRIT](https://www.irit.fr/) et plus particulièrement de [Michael Vo](https://github.com/mvo-projects) et des équipes de recherche SAMoVA et MELODI.

[Une page lui est consacré sur le dépôt du spectacle Turing Test](https://github.com/LeonLenclos/turing-test/blob/master/contenu/robots/alan.md)

![](ressources/logo/logo.png)

**Attention : le contenu de ce dépôt est un travail en cours, des fonctionnalités peuvent ne pas être opérationnelles. Des éléments de documentations peuvent être obsolètes.**

## Comment parler avec Alan

**Version de python requise : Python 3.5**

En spectacle nous utilisons le Alan de la branche `master`. Mais la version d'Alan la plus récente est contenu dans la branche `develop`.

Ces instructions ne concernent pas la partie *mvo-chatbot* ou *mode impro*.


### installer

```
  $ cd alan
  $ pip install -r requirements.txt
  $ python3
  >>> import nltk
  >>> nltk.download("punkt")
  >>> quit()
```

### Lancer l'interface terminal

```
  $ cd alan/brain
  $ ./alan.py -h # pour obtenir l'aide
  $ ./alan.py
```

### Lancer l'interface web

```
  $ cd alan/brain
  $ ./server.py -h # pour obtenir l'aide
  $ ./server.py
```

puis visiter http://localhost:8000 avec un navigateur.

### indiquer des fichiers de réglage spécifique

Les fichier de réglage sont contenu dans `alan/brain/settings`.

Par defaut, alan se lance avec les réglages contenu dans le fichier `default.json`.

D'autres fichier de réglages peuvent être choisis grace à l'argument `-s`.

```
 $ ./alan.py -s speak
 # lance Alan avec les réglages contenus dans le fichier speak.json
 $ ./alan.py -s base interface/text logic
 # lance Alan avec les réglages contenus dans les fichier base.json interface/text.json et logic/default.json
```

Voir [brain/settings/README.md](brain/settings/README.md) pour plus d'information sur le fonctionnement des fichiers settings

