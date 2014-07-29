#!/bin/bash


function get_window_id() {
    window_id=$(wmctrl -l | grep "$1" | tail -1 | cut -f1 -d" ")
}

bash extractAudio.sh
python pocketsphinx_python.py test_16k_mono.wav 
gedit transcription.txt &
sleep 1
get_window_id gedit
wmctrl -i -r "$window_id" -e 0,1025,0,953,1000
cvlc -vvv test.mp4
get_window_id vlc
wmctrl -i -r "$window_id" -e 0,0,0,953,1000
