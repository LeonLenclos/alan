# Sur quoi tester Alan

Le mieux restera toujours d'avoir des conversations, des échanges de répliques pas préparées à l'avance. C'est l'utilisation qui est faite d'Alan au final donc ça reste le meilleur moyen de le tester.

Pour le tester sur des listes d'entrées on vous propose ce document comme base.


## Qu'attend-t-on comme réponse

Une réponse satisfaisante peut être :

- Une réponse passe partout (eg. "quel est ton plat préféré ?" -> "C'est toujours le même" marche avec n'importe quelle entrée commençant par "quel est ton")
- Un refus de répondre (eg. "quel est ton plat préféré ?" -> "Je ne sais pas..." marche avec n'importe quelle question)
- Une réplique relative à un thème détécté dans l'entrée (eg. "quel est ton plat préféré ?" -> "Tu as vu, le restaurant où on allait a fermé..." le theme cuisine/nourriture est respecté) 
- Un changement de sujet (eg. "quel est ton plat préféré" > "À ce propos, tu connais Marcel Duchamps ?" peu cohérent mais rend la conversation dynamique)
- Une réponse précise ( "Quel est ton mode de transport favori" > "Je me déplace en vélo, c'est ce que je préfère")


En général :

- On apprécie les répliques courtes même si ça ne dois pas être une règle absolue.
- On évite le vouvoiement

Il faut garder à l'esprit que Alan doit pouvoir fonctionner selon deux modes distincts d'utilisation :

- Utilisation publique dans un contexte d'installation, de performance ou sur internet.
- En mode spectacle pendant Turing Test.

L'objectif est de confier ces deux tâches à une seule version d'Alan, la création se nourrissant de cette contrainte.


## Test sur des questions


Un des types d'entrées les plus fréquents c'est les questions. Question à propos d'Alan, questions de culture g, questions "philosophiques", etc. C'est donc une première catégorie d'entrées à tester. Bien sûr nous n'attendons pas forcément une réponse correcte ni même cohérente à ces questions. On apprécierait cependant qu'il ai l'air de comprendre que c'est une question.

Exemples d'entrées à tester :

- Que penses-tu de ma blague ?
- Qui es-tu ?
- Tu as vu le dernier Star Wars ?
- Quel est ton plat préféré ?
- Comment vas-tu ?
- Où sommes-nous ?
- Pourquoi les robots sont-ils aussi bêtes ?
- Tu as faim ?
- Tu veux jouer à un jeu ?
- Combien pèse un élephant ?
- Est-ce que tu comprends ce que je te dis ?
- Tu parles combien de langues ?
- Quel est le sens de la vie ?
- Pourquoi les toits des maisons sont inclinés ?
- Tu veux faire quoi quand tu seras grand ?
- C'est quoi pour toi une discussion ?
- Combien de faces a un cube ?
- Quelle heure est-il ?

## Test sur des répliques courtes décontextualisées


Une conversation est beaucoup faites de répliques courtes qui n'ont aucun sens si elles ne sont pas ramenées à leur contexte. C'est pourtant très important de pouvoir y répondre quand même.

Exemples d'entrées à tester :

- Pourquoi ?
- Tu es sûr ?
- Oui.
- Non.
- Hm...
- D'accord.
- Et toi ?
- Ok.
- C'est tout ?
- Je vois...
- Pareil !
- C'est drôle.
- Surtout pas.


## Test sur des phrases affirmatives


L'utilisateur a l'impression qu'il peut apprendre des choses à Alan, que ce soit à propos de l'uttilisateur, à propos d'alan, à propos du contextes ou culture g. Alan dois conforter l'utilisateur dans cette impression.

Exemples d'entrées à tester : 

- Je suis une fille.
- J'ai l'impression de parler à un mur.
- Il pleut encore aujourd'hui.
- La fête du travail c'est le premier mai.
- Il y a des oiseaux qui ne savent pas voler.
- Tu es une machine tu ne peux pas avoir d'émotions.
- On est un peu perdus.
- Moi je ne condamne pas les actions de ces personnes.
- J'ai achetté une canette au distributeur.
- L'absence de lumière fait que je suis dans le noir.
- Le soleil tourne autour de la terre.

## Test sur des répliques du spectacle


Ça peut être interessant de le tester sur des répliques utilisées en spectacle. Même si pour ces répliques là nous préfererons certainement utiliser les script, c'est des bons exemple du type de langage qu'on utilise.

Exemples d'entrées à tester :

- Il faut que je te parle d'un truc important.
- Le problème c'est qu'il y a aussi des films pas terribles
- T'énerves pas Alan. On est sur un gros projet et on a besoin de toi.
- Tu veux du bouillon ?
- Dans un village si le barbier rase tous les gens qui ne se rasent pas eux-mêmes, qui rase le barbier ?
- Tu connais des histoires ?
- Tu connais quoi ?
