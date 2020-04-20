# A LIRE AVANT D'INTERVENIR DANS LES RIVESCRIPT

**Attention ! cette documentation est en construction. A compléter et enrichir**

Ces consignes sont destinées à optimiser les contributions entre collaborateurs sur le rivescript d'Alan.
Elles peuvent être modifiées par n'importe quel collaborateur. 

Les fichiers .rive sont écrits en [RiveScript](https://www.rivescript.com) qui est un langage permettant d'écrire des scénarios pour agent conversationnels.
La doc est disponible [ici](https://www.rivescript.com/docs/tutorial)

Dans la suite, le terme scénario désigne un ensemble de un ou plusieurs triggers/réponses liés par le sens ou la logique de l'èchange.

## Remarques générales sur les .rive

- Pour éviter les catch all.
   - Les catch all sont souvent déclenchés par une interdiction de répétition. Même si il y a plusieurs réponses possibles, il suffit que le tirage au sort se répète...
   - Une bonne solution pour diminuer la probabilité d'une telle situation, est ce conserver des redondances dans des .rive différents.
   - Par redondance, il faut entendre un scénario avec des triggers très proches ou identiques mais avec des réponses différentes.
   - donc éviter les redondances dans un même fichier mais ne pas se les interdire dans des fichiers .rive différents
   - Une autre solution consiste à placer autant que possible des array dans les réponses. (ca vaut d'ailleurs le coup de créer des array spécial réponse)
   - En effet un array dans une réponse rend la probabilité de répétion plus faible et crée des variations intéressantes.

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
    
