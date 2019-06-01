# Usage : ./voice_audio.sh text speed
# Dependencies : pico-tts, sox

pico2wave 2>/tmp/error_pico -l fr-FR -w /tmp/alan_voice.wav "$1"
play 2>/tmp/error_alsa -q /tmp/alan_voice.wav -t alsa speed $2 highpass 600
while [ -s /tmp/error_alsa ]
do
	cat /tmp/error_alsa >> /tmp/error_alsa_log
        rm /tmp/error_alsa
        sleep 0.01
        play 2>/tmp/error_alsa -q /tmp/alan_voice.wav -t alsa speed $2 highpass 600

done
