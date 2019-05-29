pico2wave -l fr-FR -w tmp.wav "Youpi !"
sox tmp.wav tmp2.wav speed 0.85
n=1000; while [ $n -gt 400 ]; do beep -f $n -l 5; n=$((n*97/100)); done
n=2000; while [ $n -gt 400 ]; do beep -f $n -l 5; n=$((n*97/100)); done
n=3000; while [ $n -gt 400 ]; do beep -f $n -l 5; n=$((n*97/100)); done
aplay -q tmp.wav
beep -f 1000 -n -f 1500 -n -f 600 -n -f 500 -n -f 100 -r 2 -l 10 -n -f 50 -r 2 -l 200 -n -f 40 -r 2 -l 300 -n -f 60 -r 3 -n -f 50 -r 3
aplay -q tmp.wav
aplay -q tmp.wav
aplay -q tmp.wav
n=1000; while [ $n -gt 400 ]; do beep -f $n -l 5; n=$((n*97/100)); done
n=2000; while [ $n -gt 400 ]; do beep -f $n -l 5; n=$((n*97/100)); done
n=3000; while [ $n -gt 400 ]; do beep -f $n -l 5; n=$((n*97/100)); done
rm tmp.wav tmp2.wav
