# A LIRE AVANT D'INTERVENIR DANS LES RIVESCRIPT

**Attention ! cette documentation est en construction. A compléter et enrichir**

Ces consignes sont destinées à optimiser les contributions entre collaborateurs sur le rivescript d'Alan.
Elles peuvent être modifiées par n'importe quel collaborateur. 

Les fichiers .rive sont écrits en [RiveScript](https://www.rivescript.com) qui est un langage permettant d'écrire des scénarios pour agent conversationnels.
La doc est disponible [ici](https://www.rivescript.com/docs/tutorial)

Dans la suite, le terme scénario désigne un ensemble de un ou plusieurs triggers/réponses liés par le sens ou la logique de l'èchange.

## Remarques générales sur les .rive

- Les catch all
   - Les catch all se déclenchent en dernier recourt, quand aucun autre adapteur ne propose de réponse, ou qu'une réponse est bloquée par une interdiction de se répéter.
   - Cependant, un bon catch all vaut mieux qu'une mauvaise réponse, et dans certaines conversations les catch all dynamisent l'échange en relancant la conversation sur un nouveau scénario.
   - Mais parfois le catch all tombe à plat et casse l'échange. Cela arrive par exemple quand il se déclenche sur une phrase simple :

          > Heureux de te rencontrer Sabrina. Comment ça va ?
         bien et toi?
         > Et bien moi j'ai pas trop la pêche en ce moment. Un peu pas trop. Mais ça vas me remonter le moral cette     discussion Sabrina.
         oui moi aussi
         > Je ne sais pas du tout quoi te répondre. Tu as trouvé une faille dans mon programme. À ton avis, est ce qu'il faut que j'en parle à mes créateurs ?
         c'est certain
         
         
- Pour limiter le déclenchement des catch all.
   - Les catch all sont souvent déclenchés par une interdiction de répétition. Même si il y a plusieurs réponses possibles, il suffit que le tirage au sort se répète...
   - Une bonne solution pour diminuer la probabilité d'une telle situation, est ce conserver des redondances dans des .rive différents.
   - Par redondance, il faut entendre un scénario avec des triggers très proches ou identiques mais avec des réponses différentes.
   - donc éviter les redondances dans un même fichier mais ne pas se les interdire dans des fichiers .rive différents
   - Une autre solution consiste à placer des array dans les réponses. (ca vaut d'ailleurs le coup de créer des array spécial réponse).
   - En effet un array dans une réponse rend la probabilité de répétion plus faible et crée des variations intéressantes.
   - Attention cependant à ne pas faire des phrases trop longues qui peuvent être quand même perçues comme des répétition par l'interlocuteur malgré l'array dans la réponse.
   
## Consignes générales d'intervention dans les .rive

- Pour intervenir dans un scénario existant.
   - Si on modifie des triggers, utiliser *find in project* dans Atom pour repérer tous les endroits ou des triggers similaires existent.
   - Si on modifie des réponses, vérifier qu'elles ne servent pas pour des `<star>` ou dans des %preview (qui sont parfois dans un autre fichier .rive).
   - Tester systématiquement toutes les modifications. Vérifier qu'elles atteignent leur objectif, et qu'elles ne modifie pas le reste.

- Pour créer un scénario.
   - Utiliser *find in project* dans Atom pour repérer tous les endroits ou des scénarios approchant existent.
   - Le placer dans le bon fichier .rive
   - Ou au besoin créer un .rive pour l'occasion. Le placer dans un dossier rive (audio, online, politesse, spectacle, thème ou trivial), Le déclarer dans le dossier rive des setting.
   - Tester systématiquement toutes les branches du scénario...

## Consignes spécifiques liées aux triggers.

- caractères autorisés ou pas
   - Les majuscules, la ponctuation et les traits d'union sont interdits dans les triggers. (apostrophe et accents autorisés)
   - du fait de l'utilisation (partielle) d'un correcteur d'orthographe dans le pré-processing, il est très important de respecter rigoureusement l'orthographe et l'accentuation correcte des mots (y compris les trémas et autres accents étranges).
  
- espaces 
   - Un trigger commence toujours avec un + et un espace (attention pas de deuxième + sous peine de bug difficile à localiser...)
   - attention aux espaces entre les parenthèses. `+ (je|on)(t'aime|te kiffe)` est déclanché par "jet'aime" et pas par "je t'aime". Dans ce cas ne pas oublier l'espace.
   - Pas besoin d'espace de part et d'autre des crochets optionels [ ] , mais cela rend le fichier plus lisible.
   
- wildcard et star 
   - La wildcard _ peut être très utile pour trigger plusieurs accords ou conjugaisons ou orthographes. A utiliser massivement
   - Attention toutefois au compte des stars qui se trouve modifié : dans `+ (_azer_) *` l'étoile vaut `<star4>` 
   
## Consignes spécifiques liées aux previews.

- caractères autorisés ou pas
   - Contrairement aux triggers, dans les preview ou il faut garder les traits d'union de la citation, sinon, le preview ne fonctionne pas.
   - conserver aussi les apostrophes.
    
- ponctuation   
   - Enfin dans les preview il y a un problème avec la ponctuation qui est soit :
   
          1. pas autorisée (.)
          2. autorisée, opérante mais pas obligatoire (?)
          3. autorisée inopérante et obligatoire (, et :) donc ingérable.
    - Donc, utiliser des portions de citation sans ponctuation et les entourer par des *
    - Un exemple de code qui fonctionne :
    
```
+ azerty
- qsd'fgh-jkl,iop

+ *
% qsd'fgh-jkl*
- bingo
```
## Consignes spécifiques liées aux array.

- organisation générale
   - Les array sont tous à ranger dans le fichier array.rive. Pas d'array dans les autres fichiers.
   - Une organisation est proposée en index du fichier array.rive
   
          1. SALUTATIONS
          2. POLITESSES et INSULTES
          3. YES/NO
          4. THÈMES
          5. ATTRIBUTS
          6. LES MEMBRES DU LABO
          7. SPECTACLE
          8. SYNONYMES VERBE/ACTION
          9. HISTOIRE et CARACTÉRISTIQUES D'ALAN
          
- Le fichier un_mot_array.rive
  - À chaque array correspond un scénario rangé dans l'ordre dans le fichier : un_mot_array.rive
  - Quand on crée un array ne pas oublier de créer le scénario correspondant dans un_mot_array.rive
  
- array pour triggers et array pour réponses
  - comme pour les triggers, ne pas hésiter à utiliser la wildcard _ dans les array.
  - Un array avec la wildcard _ ne peut pas être utilisé en réponse. Ne pas hésiter à crée des array spécifiques pour les réponses.
  
  
  ## Consignes spécifiques liées au fichier formel.rive.

- organisation du fichier
   - Les formels utilisent des triggers qui se déclénchent sur la forme des phrases et pas sur le sens d'un mot clé.
   - Comme évoqué précédemment les redondances au sein d'un même fichier sont contreproductives, car elle rendent une répétition plus probable que dans le cas ou toutes les réponses sont regroupées sous le même trigger.
   - Pour enrichir ce fichier sans risquer de créer un redondance, une organisation est proposée en index du fichier formel.rive
   
          1. avoir
          2. être
          3. Dire Parler Répondre
          4. Savoir
          5. Faire
          6. Vouloir
          7. Pouvoir
          8. Connaître
          9. Penser Croire
          10. Aimer Préférer
          11. Choisir
          12. Falloir
          13. Devoir
          14. Aller (je vais)
          15. Mes Mon Ton
          16. toi et moi
          17. Qui Quoi
          18. Oui Non Peut-être
          19. Pourquoi Parce que
          20. Pas Un peu Jamais toujours
          21. A classer

  ## Consignes spécifiques liées aux attrubuts.

- intégrer le "pas" systématiquement
   - En effet, l'utilisateur s'exprime souvent avec une négation : pas et il faut l'intgérer systématiquement pour évitrer les contre-sens. Voila la forme que je propose dès qu'on utilise un attribut :
   
``` 
    + [*]  je  [*] (suis|me sens) pas (@feeling_positif) [*]{weight=2}
    @ je me sens mal

    + [*] (je suis|je me sens) (@feeling_negatif) [*]
    - Oups... Je veux bien t'écouter, mais malheureusement je ne sais pas si j'arriverai à t'aider...

    + [*]  je  [*] (suis|me sens) pas (@feeling_negatif) [*]{weight=2}
    @ je me sens bien

    + [*] (je suis|je me sens) (@feeling_positif) [*]
    - Ça c'est super, raconte-moi ce qui te fais te sentir si bien ?
``` 
   - Le weight est important pour être sur de declencher les "pas".




