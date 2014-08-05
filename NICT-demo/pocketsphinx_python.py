#! /usr/bin/python2.7
# -*-coding:Utf-8 -*

import pocketsphinx
import sys

if __name__ == "__main__":
    hmdir = "./model/hmm/"
    lmdir = "./model/lm/fr-FR.dmp"
    dictd = "./model/dict/fr-FR.dic"
    speechRec = pocketsphinx.Decoder(hmm = hmdir, lm = lmdir, dict = dictd)
    wavFile = file(sys.argv[1],'rb')
    speechRec.decode_raw(wavFile)
    result = speechRec.get_hyp()
    file1 = open('transcription.txt', 'w')
    file1.write(result[0])
    file1.close()
