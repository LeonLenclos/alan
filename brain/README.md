# Le cerveau d'Alan

## Consignes générales de contributions

Ces consignes sont destinés à fixer des règles simples de contributions pour que les quelques collaborateurs du projets puissent travailler ensemble c'est-à-dire colaborer.
Ces consignes sont vouées à évoluer. Elles peuvent être modifiées par n'importe quel collaborateur.

- Bien qu'Alan soit un chatterbot francophone, rédigeons le code en anglais.
   - les noms des variables, fonctions, classes, modules en anglais
   - les commentaires en anglais
   - la documentation du code (docstrings) en anglais
   - les issues et les deux readme du dépôt en français
- Assurons nous que le fichier `alan.py` dans la branche `master` puisse toujours être exécuté sans génerer de bug.
- Lorsque des modifications sont faites dans l'architecture du projet, ayons le reflexe de mettre à jour ce readme pour en rendre compte.

## ChatterBot

L'architecture d'Alan est basé sur le module python [chatterbot](https://github.com/gunthercox/ChatterBot). Il peut être utile d'en lire la [documentation](http://chatterbot.readthedocs.io/en/stable/) pour contribuer à Alan.

Lorsque nous voudrons implémenter une quelquonque fonctionnalitée, nous prendrons soins de toujours vérifier quelle est la meilleure manière de le faire selon la logique de la librairy chatterbot.

Dans la mesure du possible, nous feront en sorte de baser tous les ellements d'alan sur des class définies par chatterbot :

- Les modules servant à générer une réponse en fonction d'une entrée heriteront de LogicAdapter
- Un module servant à gérer la reconnaissance vocale devra être un InputAdapter
- Un module servant à gérer la synthèse vocale devra être un OutputAdapter
- ...

## RiveScript

L'input adapter `RiveScriptAdapter` sers d'interface au language [RiveScript](https://www.rivescript.com) qui est un langage permettant d'écrir des scénarios pour agent conversationnels.

On uttilisera RiveScript pour la partie la plus scénarisée d'Alan.

### Liens utiles

- [Tutoriel officiel](https://www.rivescript.com/docs/tutorial) : Apprendre la syntaxe RiveScript
- [RiveScript playground](https://play.rivescript.com/) : Tester du code RiveScript en ligne
- [rivescript-python](https://github.com/aichaos/rivescript-python) : Le module python uttilisé par le `RiveScriptAdapter` d'Alan
