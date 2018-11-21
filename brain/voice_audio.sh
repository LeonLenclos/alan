pico2wave -l fr-FR -w tmp.wav "$1"
play -q tmp.wav -t alsa speed $2
rm tmp.wav
