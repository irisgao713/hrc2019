import scrapy
import datetime
import random
import time
import sys, getopt
import glob

dst = '../results/processed/'

file, directory = tryarg(sys.argv)


if file == '':
    #Processing a directory: assuming csv format



elif directory == '':
    #Processing a file: assuming csv format


else:
    print ('Please use one of the following modes: web, archive, normal')
    

def getPath(fullCmdArguments):
# read commandline arguments, first
#fullCmdArguments = sys.argv

    # - further arguments
    argumentList = fullCmdArguments[1:]

    unixOptions = "fd"
    gnuOptions = ["file=", "dir="]

    try:
        arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        sys.exit(2)

    #initiate optional arguments
    directory = ''
    file = ''
    # evaluate given options
    for currentArgument, currentValue in arguments,values:
        if currentArgument in ("-f", "--file"):
            print (("Pointing source file to: %s") % (currentValue))
            file = str(currentValue)
        elif currentArgument in ("-d", "--dir"):
            print (("Pointing source directory to: %s") % (currentValue))
            directory = str(currentValue)

    return file, directory