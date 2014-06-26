#Check if the scrip is run with root access
if [ "$(whoami)" != 'root' ]; then
        echo "You have to be root to run $0"
        exit 1;
fi

sudo apt-get install bison automake autoconf libasound-dev

#untar all file in folder
for a in `ls *.tar.gz`;
do
	tar xzf $a;
done

#installing sphinxbase at first
for a in `ls`;
do
	if [ -d "$a" ] ;
	then
		if [[ $a == sphinxbase* ]];
		then
			cd $a;
			echo installing $a;
			sh autogen.sh
			make
			make install
			cd ..;
		fi
	fi 
done

#install all the sphinx programm
for a in `ls`;
do
	if [ -d "$a" ] ;
	then
		if [[ $a != sphinxbase* ]];
		then
			cd $a;
			echo installing $a;
			sh autogen.sh
			make
			make install
			cd ..;
		fi
	fi
done
#creation of a file run on boot used to make the use of pocketsphinx possible
cd /etc/profile.d/
touch pocketSphinxInit.sh
echo "export LD_LIBRARY_PATH=/usr/local/lib" > pocketSphinxInit.sh
echo "export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig" >> pocketSphinxInit.sh
export LD_LIBRARY_PATH=/usr/local/lib
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
