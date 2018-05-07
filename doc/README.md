# Documentation pour Alan

**Attention ! cette documentation est certainement dépassée. Elle est peu consultée est rarement mise à jour ! Nous la concervons ici car elle peut servir de base pour une documentation plus serieuse.**

## Consignes générales de contributions

Ces consignes sont destinés à fixer des règles simples de contributions pour que les quelques collaborateurs du projets puissent travailler ensemble c'est-à-dire collaborer.

Ces consignes sont vouées à évoluer. Elles peuvent être modifiées par n'importe quel collaborateur.

- Bien qu'Alan soit un chatterbot francophone, rédigeons le code en anglais.
   - les noms des variables, fonctions, classes, modules en anglais
   - les commentaires en anglais
   - la documentation du code (docstrings) en anglais
   - les issues et les readme du dépôt en français
- Assurons nous que le fichier `alan.py` dans la branche `master` puisse toujours être exécuté sans génerer de bug.
- Lorsque des modifications sont faites dans l'architecture du projet, ayons le reflexe de mettre à jour ce readme pour en rendre compte.

## ChatterBot

L'architecture d'Alan est basé sur le module python [chatterbot](https://github.com/gunthercox/ChatterBot). Il peut être utile d'en lire la [documentation](http://chatterbot.readthedocs.io/en/stable/) pour contribuer à Alan.

Lorsque nous voudrons implémenter une quelquonque fonctionnalitée, nous prendrons soins de toujours vérifier quelle est la meilleure manière de le faire selon la logique de la librairy chatterbot.

Dans la mesure du possible, nous feront en sorte de baser tous les ellements d'alan sur des class définies par chatterbot :

- Les modules servant à générer une réponse en fonction d'une entrée heriteront de LogicAdapter
- Un module servant à gérer la reconnaissance vocale devra être un InputAdapter
- Un module servant à gérer la synthèse vocale devra être un OutputAdapter
- ....

## RiveScript

L'input adapter `RiveScriptAdapter` sers d'interface au language [RiveScript](https://www.rivescript.com) qui est un langage permettant d'écrir des scénarios pour agent conversationnels.

On uttilisera RiveScript pour la partie la plus scénarisée d'Alan.

### Liens utiles

- [La doc rs](https://www.rivescript.com/wd/RiveScript)
- [Tutoriel officiel](https://www.rivescript.com/docs/tutorial) : Apprendre la syntaxe RiveScript
- [RiveScript playground](https://play.rivescript.com/) : Tester du code RiveScript en ligne
- [rivescript-python](https://github.com/aichaos/rivescript-python) : Le module python utilisé par le `RiveScriptAdapter` d'Alan

## Statement

Les objets staement

```
   statement.text # str : Le texte du statement
   statement.confidence # int : l'indice de confiance
   statement.extra_data["speaker"] # str : qui a parlé ("alan" ou "human")
   statement.extra_data["logic_identifier"] # str : quel logic adapter a parlé (eg. "einstein")
```


## architecture

Inspirée de celle du package chatterbot. En voici un résumé

#### alan.py

Le fichier qu'il faut lancer pour parler avec alan. On y défini alan et on lance la discussion.

#### settings/

Les réglages d'Alan pour son initialisation. Il y est surtout question de quels adapters il faut utiliser avec quels réglages.

#### logic/

Un dossier contenant les logic_adapters d'Alan. contient aussi un `__init__.py` à tenir à jour.

#### txt/

Un dossier contenant des fichiers .txt utilisés par les RelevantQuotation (pour l'instant)

#### rive/

Un dossier contenant des fichiers .rive utilisés par les RiveScriptAdapter

#### test/

Un dossier contenant des test

#### storage/

Gère la manière dont sont stockées et sont récupérées les infos dans la base de donnée

#### preprocessors.py

Un fichier contenant des fonctions de type preprocessor

#### utils.py

Un fichier contenant des fonctions de type utilitaires
