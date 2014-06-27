#! /usr/bin/python2.7
# -*-coding:Utf-8 -*

import os
import subprocess
import wave
import contextlib
import math

def getDuration(fname):
    """Get the duration of the wave file, in second."""
    try:
        with contextlib.closing(wave.open(fname, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
    except IOError:
        return None


def getMaxSizeSplitFrame(duration):
    """Return the numbre (in second) of the max size to split the wave file.
    Return -1 if the file don't need to be split, else return the number of frame"""
    if duration <= 30:
        return -1
    else:
        return min(30, math.floor((duration * 16000) / 48000)) * 16000


def getEndFramesFromFile(name):
    """Return a list of the end frame of each sentences."""
    textFile = open(name, 'r')
    txt = textFile.readlines()
    textFile.close()
    listFrame = []
    for line in txt:
        tmp = line.split(' ')
        if tmp[0] == 'LBR:':
            listFrame.append(tmp[2])
    return listFrame


def convertFrameList(f):
    i = 0
    while i < len(f):
        f[i] = int(f[i].replace(',', ''))
        i += 1
    return f

def convertFrameToSecond(frame):
    return frame / 16000.

def getListSplitFrame(splitSize, frameList):
    size = splitSize
    listSplitFrame = []
    previous = 0.
    i = 0
    # get the list of the ending frame of sentences where we need to cut
    while i < len(frameList):
        if frameList[i] < size:
            previous = frameList[i]
        else:
            listSplitFrame.append(previous)
            size += splitSize
        i += 1
    listSplitFrame.append(frameList[len(frameList) - 1])
    return listSplitFrame


def splitWavFile(name, splitSize, frameList):
    """Split one wave file into several smaller. Return the number of file created."""
    fileNumber = 0
    beginFrameInSecond = 0
    for elem in listSplitFrame:
        splitFileName = name.replace('.wav', '_' + str(fileNumber) + '.wav')
        subprocess.Popen(['sox', name, splitFileName, 'trim', str(beginFrameInSecond), str(convertFrameToSecond(elem))], stdout=subprocess.PIPE)
        #print('sox ' + name+' ' + splitFileName+' ' + 'trim ' + str(beginFrameInSecond)+' ' + str(convertFrameToSecond(elem)))
        beginFrameInSecond = convertFrameToSecond(elem + 1)
        fileNumber += 1
    return fileNumber


def returnSfoFileName(name):
    return name + '.SFO'


def returnWaveFileName(name):
    return name + '.wav'


def getTextFromSfoFile(name):
    """Return the text associated to the ending frame of the sentence"""
    textFile = open(name, 'r')
    txt = textFile.readlines()
    textFile.close()
    sentences = dict()
    for line in txt:
        tmp = line.split(' ')
        if tmp[0] == 'LBR:':
            i = 0
            string = ''
            for elem in tmp:
                if i < 6:
                    i += 1
                else:
                    string = string + ' ' + elem
            index = int(tmp[2].replace(',', ''))
            sentences[index] = string.replace('\r\r', '')
    return sentences


def generateSfoAndTextFile(numberOfFile, sentences, name, listSplitFrame):
    """Function that generate the sfo et text file associated to each audio file."""
    begin = 0
    for i in range(numberOfFile):
        listSentence = []
        for key in sentences.keys():
            if key > begin and key <= listSplitFrame[i]:
                listSentence.append(key)
                #print('0< ' + str(key)+ ' < '+ str(listSplitFrame[i]))
        listSentence.sort()
        sfo = open(name+'_'+str(i)+'.SFO', 'w')
        sfo.write('TXF: '+name+'_'+str(i)+'.txt\n')
        sfo.close()
        txt = open(name+'_'+str(i)+'.txt', 'w')
        for elem in listSentence:
            if elem <= listSplitFrame[i]:
                txt.write('TXT: ' + sentences[elem] + '\n')
        txt.close()
        begin = listSplitFrame[i] + 1


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
                            if duration is not None:
                                #part to process every files
                                #print('File ' + name + '.wav = ' + str(duration) + ' seconde')
                                #print(getEndFramesFromFile(name+'.SFO'))
                                #print('File ' + name + '.wav = ' + str(duration) + ' seconde. Splitsize : ' +str(getMaxSizeSplitFrame(duration)))
        os.chdir('..')  # leave folder