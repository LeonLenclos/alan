# Alan v1.5.2

## Description

Alan est un agent conversationel créé pour le spectacle [Turing Test](https://github.com/LeonLenclos/turing-test) par Léon Lenclos, Fabien Carbo-Gil et Bertrand Lenclos de la [cie Nokill](http://cienokill.fr) avec la collaboration de l'[IRIT](https://www.irit.fr/) et plus particulièrement de [Michael Vo](https://github.com/mvo-projects) et des équipes de recherche SAMoVA et MELODI.

[Une page lui est consacré sur le dépôt du spectacle Turing Test](https://github.com/LeonLenclos/turing-test/blob/master/contenu/robots/alan.md)

![](ressources/logo/logo.png)

**Attention : le contenu de ce dépôt est un travail en cours, des fonctionnalités peuvent ne pas être opérationnelles. Des éléments de documentations peuvent être obsolètes.**

## Contenu du dépôt

En spectacle nous utilisons le Alan de la branche `master`. Mais la version d'Alan la plus récente est contenu dans la branche `develop`.

Le dossier brain/ contient le cerveau d'alan, l'ensemble des scripts et des ressources necessaire pour qu'il fonctionne.

## Installation

### 1. Le bon python

La version de python requise est **Python 3.5**. Alan risque de ne pas fonctionner avec des versions anterieures et posterieures de Python.

Ces instructions ne concernent pas la partie *mvo-chatbot* ou *mode impro*.

### 2. Télécharger alan

Cloner le dépôt depuis github :

```
  $ git clone https://github.com/LeonLenclos/alan.git
```

### 3. Installer les dépendances

Installer les dépendances avec pip

```
  $ cd alan
  $ python3.5 -m pip install -r requirements.txt
```

### 4. Installer un dictionnaire

À documenter

### 5. Installer pico (optionnel)

À documenter


### 5. Installer mvo-chatbot, le *mode impro* (optionnel)

À documenter


## Usage

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

puis visiter http://localhost:8000/ avec un navigateur web.

### Settings

#### Tableau des settings

| setting   | commande à éxécuter        | interface | TTS | logic adapters **exclus**     |
|-----------|----------------------------|-----------|-----|-------------------------------|
| default   | `./alan.py`                | Terminal  | OUI |                               |
| local     | `./server.py`              | Web       | OUI | rive/online et rive/spectacle |
| spectacle | `./server.py -s spectacle` | Web       | OUI | rive/online                   |
| internet  | `./server.py -s internet`  | Web       | NON | rive/audio et  rive/spectacle |

#### Fonctionnement des settings

Les fichier de réglage sont contenu dans `alan/brain/settings`.

Par defaut, `alan.py` se lance avec le réglage `default`. Et `server.py` se lance avec le réglage `local`.

D'autres fichier de réglages peuvent être choisis grace à l'argument `-s`.

Voir [brain/settings/README.md](brain/settings/README.md) pour plus d'information sur le fonctionnement des fichiers settings

### Server

Le script `server.py` fait tourner un server web. L'adresse par defaut est http://localhost:8000.

- La page `/` ou `/index.html` contient une interface pour parler avec Alan.
- La page `/labo.html` contient l'interface simplifiée utilisée en spectacle.
- La page `/dev.html` donne accès aux conversations, aux logs et aux todos pour faciliter le travail de developpement et de maintenance.


