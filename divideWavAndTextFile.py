#! /usr/bin/python2.7
# -*-coding:Utf-8 -*

import os
import subprocess
import wave
import contextlib

def getDuration(fname):
    try:
        with contextlib.closing(wave.open(fname, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
    except IOError:
        return None


def getSplitFrame(duration, fileName):
    if duration <= 30:
        return -1


if __name__ == "__main__":
    os.chdir('wav')
    listing = subprocess.Popen('ls', stdout=subprocess.PIPE)
    listing = listing.stdout.read().split('\n')

    for line in listing:
        if line != '\n':
            os.chdir(os.path.join(os.getcwd(), line))  # enter the folder
            # filter by wav file
            ls = subprocess.Popen('ls', stdout=subprocess.PIPE)
            grep = subprocess.Popen(['grep', '.SFO'], stdin=ls.stdout, stdout=subprocess.PIPE)
            ls.stdout.close()
            listWavFile = grep.communicate()[0]
            ls.wait()
            # get name of all wav files
            for elem in listWavFile.split(' '):
                if elem != ' ' or elem != '\n':
                    tmp = elem.split('.SFO\n')
                    # for each text file
                    for name in tmp:
                        if name != '\n':
                            duration = getDuration(name + '.wav')
                            if duration != None:
                                print('File ' + name + '.wav = ' + str(duration) + ' seconde')
        os.chdir('..')  # leave folder