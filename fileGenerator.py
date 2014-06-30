#! /usr/bin/python2.7
# -*-coding:Utf-8 -*

import subprocess
import os

def generateFileids(database):
	fileIdsTrain = open(database+'_train.fileids', 'w')
	fileIdsTest = open(database+'_test.fileids', 'w')

	fileTranscriptionTrain = open(database+'_train.transcription','w')
	fileTranscriptionTest = open(database+'_test.transcription','w')

	os.chdir('wav')
	listing = subprocess.Popen('ls',stdout=subprocess.PIPE)
	listing = listing.stdout.read().split('\n')

	for line in listing:
		if line != '\n':
			os.chdir(os.path.join(os.getcwd(),line))#enter the folder
			#filter by wav file
			ls = subprocess.Popen('ls', stdout=subprocess.PIPE)
			grep = subprocess.Popen(['grep', '.wav'], stdin=ls.stdout, stdout=subprocess.PIPE)
			ls.stdout.close()
			listWavFile = grep.communicate()[0]
			ls.wait()

			#get name of all wav files		
			for elem in listWavFile.split(' ') :
				if elem != ' ' or elem != '\n':
					tmp = elem.split('.wav\n')
					for name in tmp:
						if name:
							if '_test' in line:
								fileIdsTest.write(line+'/'+name+'\n')#write speaker_test/wavName
								textFileName = searchForTxf(name)
								if textFileName is not None :
									addTextToTranscription('frenchtraining_test_doc', textFileName, fileTranscriptionTest, name)

							else:
								fileIdsTrain.write(line+'/'+name+'\n')#write speaker/wavName
								textFileName = searchForTxf(name)
								if textFileName is not None :
									addTextToTranscription('frenchtraining_doc', textFileName,fileTranscriptionTrain, name)

			
		os.chdir('..')#leave folder

	fileTranscriptionTrain.close()
	fileTranscriptionTest.close()
	fileIdsTrain.close()
	fileIdsTest.close()

def addTextToTranscription(folder, fileName, file, name):
	oldPath = os.getcwd()
	os.chdir('../..')
	os.chdir(folder)#enter the folder with .txt files
	fileName = fileName.replace('\r\r','')
	textFile = open(fileName, 'r')
	lines = textFile.readlines()
	#remove unneccesary text and \n so that it will fit on one line
	txt=''
	for line in lines:
		if 'SPR: ' not in line or 'EPR' not in line:
			if 'TXT: ' in line:
				txt = txt + line.replace('TXT: ','')
			elif 'EXT: ' in line:
				txt = txt + line.replace('EXT: ', '')
	txt = txt.replace('\n',' ')
	if txt != '':
		file.write('<s>')
		file.write(txt)
		file.write('</s>'+' ('+name+')\n')

	textFile.close()
	os.chdir('..')
	os.chdir(oldPath)


def searchForTxf(file):
	if os.path.isfile(file+'.SFO') :
		fileName = open(file+'.SFO','r')
	elif os.path.isfile(file+'.PFO'):
		fileName = open(file+'.PFO','r')
	else:
		return None#in case the sfo or pfo file doesn't exist

	text = fileName.read().split(' ')
	fileName.close()
	find = False
	name = ''

	for elem in text:
		tmp = elem.split('\n')
		for elem2 in tmp:
			if elem2 == 'TXF:':
				find = True
			if find and '.txt' in elem2:
				name = elem2
	return name

if __name__ == "__main__" :
	print("Please wait while generating files")
	generateFileids('frenchtraining')
