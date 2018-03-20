# Documentation pour speach to text et inversement

Prise de note pour plus tard


## TTS avec espeak


Installer le loggiciel de synthèse. ([source](http://espeak.sourceforge.net/mbrola.html))


```
$ sudo apt-get install espeak
$ espeak "hello world"

$ wget http://www.tcts.fpms.ac.be/synthesis/mbrola/bin/pclinux/mbr301h.zip
$ unzip mbr301h.zip
$ sudo mv mbrola-linux-i386 /usr/bin/mbrola

$ wget http://tcts.fpms.ac.be/synthesis/mbrola/dba/fr1/fr1-990204.zip
$ unzip fr1-990204.zip
$ sudo mkdir /usr/share/mbrola/
$ sudo mv fr1/fr1 /usr/share/mbrola/
$ espeak -vmb-fr1 "Bonjour monde"
```

- [liste des langues mbrola](http://tcts.fpms.ac.be/synthesis/mbrola/mbrcopybin.html)


## STT

Un mémo déstiné surtout à moi-même. Tentative de receapituler les instructions de Abdel.

DONC, l'idée c'est d'installer [linstt](https://github.com/linto-ai/linstt-engine) ce après avoir installé Docker. toutes les infos sur le README de linstt-engine.

Après il faut faire tourner linstt avec la commande

#### Quelques commandes de Docker

`docker-compose up` devrait etre la seule que j'uttilise

```
$ docker ps -a # Affiche tous les Dockers
$ docker rm ID # Supprime le Docker qui a l'id spécifiée
$ docker-compose up # Lance le docker (à lancer depuis le dir linstt-poc)
```

#### Exemple d'un test du Docker.

Donc pendant que dans un terminal j'ai le docker qui tourne. Dans un autre je fais ça (PAR EXEMPLE)

```
$ wavesurfer & # pour m'enregistrer
$ play monfichier.wav # pour m'écouter
$ soxi monfichier.wav # pour les informations du fichier
#   verifier que :
#   Precision      : 16-bit
#   Sample Rate    : 16000
#   Chanels        : 1
$ sox in.wav -ar 16000 out.wav # s'il faut convertir
$ curl -X POST http://localhost:3000/api/transcript/modelV1 -H "Content-type:audio/wave" --data-binary "@monfichier.wav"  
```
