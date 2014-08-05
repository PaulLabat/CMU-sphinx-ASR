#!/bin/bash
vlc -I dummy --sout "#transcode{acodec=s16l,channels=2}:std{access=file,mux=wav,dst=test.wav}" test.mp4 vlc://quit
sox test.wav test_mono.wav channels 1
sox test_mono.wav  -r 16000 test_16k_mono.wav
