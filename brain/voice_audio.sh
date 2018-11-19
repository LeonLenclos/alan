pico2wave -l fr-FR -w tmp.wav "$1"
sox tmp.wav tmp2.wav speed $2
play -q tmp.wav -t alsa
rm tmp.wav tmp2.wav
