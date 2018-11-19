pico2wave -l fr-FR -w tmp1.wav "Je"
pico2wave -l fr-FR -w tmp2.wav "ris"
pico2wave -l fr-FR -w tmp3.wav "de me voir si"
pico2wave -l fr-FR -w tmp4.wav "belle"
pico2wave -l fr-FR -w tmp5.wav "dans ce"
pico2wave -l fr-FR -w tmp6.wav "miroir"
sox tmp1.wav tmp11.wav speed 0.85
sox tmp2.wav tmp22.wav speed 0.2 pitch 3000
sox tmp3.wav tmp33.wav speed 0.85 pitch 500
sox tmp4.wav tmp44.wav speed 0.7
sox tmp5.wav tmp55.wav speed 0.85
sox tmp6.wav tmp66.wav speed 0.5 pitch 2000
aplay tmp11.wav
aplay tmp22.wav
aplay tmp33.wav
aplay tmp44.wav
aplay tmp55.wav
aplay tmp66.wav
rm tmp1.wav tmp2.wav tmp3.wav tmp4.wav tmp5.wav tmp6.wav tmp11.wav tmp22.wav tmp33.wav tmp44.wav tmp55.wav tmp66.wav
