sox tmp.wav tmp2.wav speed $1
play -q tmp2.wav -t alsa
rm tmp2.wav
