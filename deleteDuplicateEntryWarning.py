#! /usr/bin/python2.7
# -*-coding:Utf-8 -*

import os

if __name__ == "__main__":
	i = 1
	out = open('tmp.dic','w')
	first = ''
	with open('frenchtraining-original-v2.dic','r') as f:
		for line in f:
			if first == line.split(' ')[0]:
				i = i + 1
				#if i > 1:
					#txt = first + '(' + str(i) + ')' + line.replace(first, '')
					#out.write(txt)
				#else:
				if i <= 1:
					out.write(line)
			else:
				i = 1
				first = line.split(' ')[0]
				out.write(line)

	out.close()
	
	os.system('sort -u tmp.dic > frenchtraining.dic')
