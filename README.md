# Alan

Alan est un agent conversationel créé pour le spectacle Turing Test.

Ce dépôt est consacré au code source d'alan. Pour des information concernant alan, pour une description d'alan, pour des images d'alan, preferons le dépôt turing-test.

- [Turing Test](https://github.com/LeonLenclos/turing-test)
- [Présentation d'Alan](https://github.com/LeonLenclos/turing-test/blob/master/textes/alan.md)
- [Discussion à propos de la construction et de la conception d'Alan](https://github.com/LeonLenclos/turing-test/blob/master/robots/alan.md)


Les consignes d'écritures pour le développement d'Alan sont dans le `brain/README.md`. Ce `README.md` sers aux visiteurs et aux consignes d'installation.

## Comment parler avec Alan

Version de python requise : Python 3.5

Le projet en est encore au début du développement. Néamoins, le Alan contenu dans la branche `master` doit normalement pouvoir tourner. En attendant de pouvoir parler avec Alan sur internet vous pouvez suivre les indications suivantes pour installer alan sur votre ordinateur !


 ```
  $ pip install -r requirements.txt
  $ python
  >>> import nltk
  >>> nltk.download("punkt")
  >>> quit()
  $ cd brain
  $ ./alan.py
  ```

### commandes spéciales

Pour quitter

```
 > ciao
```

Pour une annalyse des logic adapters en jeu dans la dernière réponse

```
 > info
```
Pour noter les deux dernières répliques dans la liste todo.md

```
 > todo
```
