#! /usr/bin/python2.7
# -*-coding:Utf-8 -*

import wave
import contextlib
import os
import subprocess


def getDuration(fname):
    try:
        with contextlib.closing(wave.open(fname, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
    except IOError:
        return None

if __name__ == "__main__":
    durationArray = [[0 for x in xrange(8)] for x in xrange(8)]
    durationArray[0][0] = '< 30'
    durationArray[1][0] = '30 - 40'
    durationArray[2][0] = '40 - 50'
    durationArray[3][0] = '50 - 60'
    durationArray[4][0] = '60 - 70'
    durationArray[5][0] = '70 - 80'
    durationArray[6][0] = '80 - 90'
    durationArray[7][0] = '> 90'

    durationArray[0][1] = 0
    durationArray[1][1] = 0
    durationArray[2][1] = 0
    durationArray[3][1] = 0
    durationArray[4][1] = 0
    durationArray[5][1] = 0
    durationArray[6][1] = 0
    durationArray[7][1] = 0

    max = 0
    min = 800


    os.chdir('wav')
    listing = subprocess.Popen('ls', stdout=subprocess.PIPE)
    listing = listing.stdout.read().split('\n')
    for line in listing:
        if line != '\n':
            os.chdir(os.path.join(os.getcwd(), line))  # enter the folder
            #filter by wav file
            ls = subprocess.Popen('ls', stdout=subprocess.PIPE)
            grep = subprocess.Popen(['grep', '.wav'], stdin=ls.stdout, stdout=subprocess.PIPE)
            ls.stdout.close()
            listWavFile = grep.communicate()[0]
            ls.wait()
            for elem in listWavFile.split('\n'):
                if elem != ' ' or elem != '\n':
                    duration = getDuration(elem)
                    if duration is not None:
                        if max < duration:
                            max = duration
                        if min > duration:
                            min = duration
                        if duration < 30:
                            durationArray[0][1] += 1
                        elif duration >= 30 and duration < 40:
                            durationArray[1][1] += 1
                        elif duration >= 40 and duration < 50:
                            durationArray[2][1] += 1
                        elif duration >= 50 and duration < 60:
                            durationArray[3][1] += 1
                        elif duration >= 60 and duration < 70:
                            durationArray[4][1] += 1
                        elif duration >= 70 and duration < 80:
                            durationArray[5][1] += 1
                        elif duration >= 80 and duration < 90:
                            durationArray[6][1] += 1
                        elif duration >= 90:
                            durationArray[7][1] += 1
        os.chdir('..')
    nbrFiles = 0
    for i in range(8):
        print(durationArray[i][0] + ' = ' + str(durationArray[i][1]))
        nbrFiles += durationArray[i][1]
    print("Numbre of wave files : " + str(nbrFiles))
    print('Max = '+str(max))
    print('Min = '+str(min))