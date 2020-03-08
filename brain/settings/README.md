Fichiers de Réglages
====================

Les fichier settings sont des fichiers json. Ils contiennent des information de réglage pour alan.

Il est possible dans un fichier settings de renseigner le nom d'autres fichiers settings à importer. La syntaxe est :

```
"import" : ["un_fichier"]
```
ou
```
"import" : ["un_fichier", "un_autre_fichier"]
```

## super settings

ce sont des fichiers de configuration qui ne font qu'importer d'autres fichiers de configuration


#### default

Utile pour bosser sur alan.

- Commande à executer : `alan.py` ou `alan.py -s default`
- Interface : Dans le terminal sans stt
- Logic : Tout les logics adapter


#### spectacle

À lancer en spectacle.

- Commande à executer : `server.py -s spectacle` puis visiter `/labo.html`
- Interface : interface web avec stt
- Logic : Tout les logics adapter sauf `rive/online/*.rive`

#### local

À lancer en expo.

- Commande à executer : `server.py -s local` puis visiter `/index.html`
- Interface : interface web avec stt
- Logic : Tout les logics adapter sauf `rive/online/*.rive` et `rive/spectacle/*.rive`


#### internet

À lancer sur le server pour mise en ligne.

- Commande à executer : `server.py -s internet` puis visiter `/index.html`
- Interface : interface web sans stt
- Logic : Tout les logics adapter sauf `rive/audio/*.rive` et `rive/spectacle/*.rive`


## error

error.json contient les messages à afficher en cas d'erreur

## base

base.json contient les réglages de base qui doivent être renseignés quelque soit la configuration.

## logic

les fichiers commençant par `logic/` configurent des logics adapters

#### logic/all

logic/all.json s'occupe de tous les logic adapters

#### logic/rive

logic/rive.json s'occupe de tous les logic adapters rivescript

#### logic/misc

logic/misc.json s'occupe de tous les logic adapters qui ne sont pas rivescript

## interface

les fichiers commençant par `interface/` configurent des input adapters et des output adapters

#### interface/text

interface/text.json configure une interface textuelle

#### interface/mac_speak

interface/mac_speak.json configure une interface vocale pour mac
