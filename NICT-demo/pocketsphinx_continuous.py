#! /usr/bin/python2.7
# -*-coding:Utf-8 -*

import subprocess
import sys

if __name__ == "__main__":
    txt = subprocess.Popen(['pocketsphinx_continuous','-hmm','model/hmm/','-dict','model/dict/fr-FR.dic','-lm','model/lm/fr-FR.dmp','-infile',sys.argv[1]], stdout=subprocess.PIPE)
    txt.wait()
    res = txt.communicate()[0]
    res = res.replace('000000000: ', '')
    file1 = open('transcription.txt', 'w')
    file1.write(res)
    file1.close()
