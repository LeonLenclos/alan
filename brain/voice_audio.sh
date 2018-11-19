pico2wave -l fr-FR -w tmp.wav "$1"
sox tmp.wav tmp2.wav speed $2
aplay -q tmp.wav
rm tmp.wav tmp2.wav
