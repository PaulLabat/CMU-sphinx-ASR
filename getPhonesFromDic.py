#! /usr/bin/python2.7
# -*-coding:Utf-8 -*

import re


def phoneInFile(phone):
    phoneFile = open('etc/frenchtraining.phone', 'r')
    text = phoneFile.read()
    phoneFile.close()
    text = text.split('\n')
    for elem in text:
        if elem == phone:
            return True
    return False

if __name__ == "__main__":
    print("Please wait while the file is being generated.")
    dic = open('etc/frenchtraining.dic', 'r')
    open('etc/frenchtraining.phone', 'w').close()  # empty the file
    text = dic.read()
    text = text.replace('\n', ' ')
    text = text.split(' ')
    dic.close()
    firstWord = True

    for word in text:
        if len(word) == 2:  # phones are all 2 characters only
            # reject word that contains characters other than letters
            if re.match("^[a-zA-Z]*$", word):
                if not phoneInFile(word):
                    phone = open('etc/frenchtraining.phone', 'a')
                    phone.write(word + '\n')
                    phone.close()
    phone.close()
    print("Work finished.")
