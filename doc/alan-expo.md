ALAN EXPO - Documentation
=========================

Cette doc est destinée aux personnes en charge de l'installation et de la maintenance du dispositif. Pour toute question, doute ou soucis n'hésitez pas à me contacter.

## Description du dispositif

Le visiteur discute avec le chatbot par l'intermédiaire d'un clavier. La discussion s'affiche sur un écran.

## Matériel

### Fournit par la compagnie

(Ce matériel prêté par la Cie Nokill devra être restitué en l'état.)

- Un raspberry-pi 4 (micro-ordinateur) dans son boîtier.
- Une carte micro SD sur laquelle est installé le programme du chatbot (la carte micro SD est insérée dans le raspberry et ne doit pas en être retiré.).
- Une alimentation pour raspberry-pi 4 (USB C).
- Un raccord mini-HDMI vers HDMI.
- Cette documentation.

### Non-fournit, mais nécessaire

- Un écran.
- Une souris et un clavier.

## Mise en place

1. Brancher le clavier, la souris et l'écran au raspberry.
2. Brancher l'alimentation du raspberry.
3. Le raspberry s'allume et lance automatiquement l'interface en plein écran (le démarrage devrait prendre moins d'une minute).

## Utilisation

Au démarrage, le message "Ouverture d'une nouvelle conversation" s'affiche.

Quand la conversation est chargée, le message est remplacé par "Conversation ouverte".

À partir de ce moment, on peut parler à Alan en tapant au clavier, appuyer sur le bouton `[Parler]` ou sur la touche entrée du clavier pour valider.

**Il est conseillé d'ouvrir une nouvelle conversation pour chaque nouvelle personne qui vient parler à Alan.**

Pour ouvrir une nouvelle conversation, appuyer sur le bouton `[+]` ou sur la touche `F5` du clavier.

Pour profiter un maximum d'une conversation avec Alan, il est important de lui parler sans faute d'orthographe ni faute de frappe. Relisez-vous !

## Ajuster la taille de l'interface en fonction de la taille de l'écran

Si l'interface s'affiche trop petite ou trop grande par rapport à l'écran, il est possible d'ajuster le facteur de zoom. Deux options :
- Maintenir `Ctrl` et régler le facteur de zoom avec la molette de la souris.
- Appuyer sur `Ctrl` + `+` (ou `Ctrl` + `Maj` + `+` ), un menu s'ouvre pour régler le facteur de zoom.

## En cas de problème

Pendant l'utilisation, on n'est pas à l'abri d'un bug du logiciel ou d'un problème lié à une utilisation maladroite ou malicieuse du dispositif. Dans la plus-part des cas, moins de deux minutes suffiront à régler le problème en suivant ce protocole :

1. Essayer d'ouvrir une nouvelle conversation en rechargeant la page (appuyer sur la touche `F5`).
2. Si le problème persiste ou si vous n'arrivez pas à recharger la page, rebooter le raspberry :
    - Méthode propre pour rebooter : `Ctrl` + `Esc` ; un menu s'ouvre, appuyez sur `Déconnexion` puis `Reboot`.
    - Méthode sale pour rebooter : débrancher et rebrancher l'alimentation du raspberry

Si le problème persiste après avoir rebooté le raspberry, ou si un problème survient trop souvent, contactez-moi !

## Problèmes connus

- La touche F1 du clavier ouvre l'aide de chromium, si un utilisateur appuie sur F1 par erreur le plus simple est de rebooter.
- D'autres touches ou combinaisons de touche peuvent ouvrir des menus qui sont souvent simples à quitter.

## Utilisation avancée

- pour quitter le mode kiosk et accéder au bureau : `Alt` + `F4`
- pour accéder à une console : `Ctrl` + `Alt` + `F1`

Le mot de passe de l'utilisateur pi : `turingtest`

## Contact

Léon Lenclos - contact@leonlenclos.net - 0627656833

## Voir aussi

- Lien permanent vers cette documentation : https://github.com/LeonLenclos/alan/blob/master/doc/alan-expo.md
- Parler avec Alan en ligne : http://alan.cienokill.fr/
- Alan sur le site de Turing Test : http://turing-test.cienokill.fr/contenu/robots/alan.html
- Alan sur Github : https://github.com/LeonLenclos/alan



