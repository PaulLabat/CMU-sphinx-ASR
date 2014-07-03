#!/bin/bash

mkdir convert
cd convert
mkdir frenchtraining_doc
mkdir frenchtraining_test_doc
cd ..

for f in frenchtraining_doc/*.txt ;
do
	var=$f
	echo $var
	path=convert;
	iconv -f 8859_1 -t UTF-8 $f > ${path}/$f
done

for f in frenchtraining_test_doc/*.txt ;
do
	var=$f
	echo $var
	path=convert;
	iconv -f 8859_1 -t UTF-8 $f > ${path}/$f
done
