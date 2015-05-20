#!/usr/bin/python
import os, sys  


def main():
    tagsJarik = []
    tagsLaurence = []
    tagsJohan = []

    directory = os.getcwd()
    for root, dirs, filenames in os.walk(directory):
        for file in filenames:
            if ((file == "en.tok.off.johan") or (file == "en.tok.off.pos Laurence") or (file == "en.tok.off.pos")):
                with open(root+'/'+file, 'r') as in_f:
                    for line in in_f:
                        columns = line.split()
                        tokenList = columns
                        
                        print(file)
                        print(columns)
                        print(tokenList)
                        
                        
                        if (len(columns) == 6):
                            tokenList.append("-")

                            print("len=6")
                            print(tokenList)
                        
                        newLine = ' '.join(tokenList)    
                        with open(root+'/'+file+'.tmp', 'a') as posfile:
                            posfile.write(newLine + '\n')

main()
