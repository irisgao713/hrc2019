# include standard modules
import getopt, sys
import glob
import os
import shutil
import datetime

def getArg(fullCmdArguments):
# read commandline arguments, first
#fullCmdArguments = sys.argv

    # - further arguments
    argumentList = fullCmdArguments[1:]

    unixOptions = "md"
    gnuOptions = ["mode=", "dir="]

    try:
        arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        sys.exit(2)

    #initiate optional arguments
    directory = ''
    # evaluate given options
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-m", "--mode"):
            print (("enabling scraper mode: %s") % (currentValue))
            mode = str(currentValue)
        elif currentArgument in ("-d", "--dir"):
            print (("pointing source directory to: %s") % (currentValue))
            directory = str(currentValue)

    return mode, directory


def getPath(fullCmdArguments):
# read commandline arguments, first
#fullCmdArguments = sys.argv

    # - further arguments
    argumentList = fullCmdArguments[1:]

    unixOptions = "fd"
    gnuOptions = ["file=", "dir="]

    # try:
    #     arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    # except getopt.error as err:
    #     # output error, and return with an error code
    #     print (str(err))
    #     sys.exit(2)

    # #initiate optional arguments
    # directory = ''
    # file = ''
    # # evaluate given options
    # for currentArgument, currentValue in arguments,values:
    #     if currentArgument in ("-f", "--file"):
    #         print (("Pointing source file to: %s") % (currentValue))
    #         file = str(currentValue)
    #     elif currentArgument in ("-d", "--dir"):
    #         print (("Pointing source directory to: %s") % (currentValue))
    #         directory = str(currentValue)

    try:
        argument, value = getopt.getopt(argumentList, unixOptions, gnuOptions)
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        sys.exit(2)

    #initiate optional arguments
    directory = ''
    file = ''
    # evaluate given options
    if argument in ("-f", "--file"):
            print (("Pointing source file to: %s") % (value))
            file = str(value)
    elif argument in ("-d", "--dir"):
            print (("Pointing source directory to: %s") % (value))
            directory = str(value)

    return file, directory


def movefile(dstDir):
    '''
     move HTML files to the right monthly folder
    '''

    srcDir = ''
    path = srcDir + '*.{}'
    if os.path.isdir(dstDir) :
        # Iterate over all the files in source directory
        for filePath in glob.glob(path.format('html')):
            # Move each file to destination Directory, use absolute path to replace existing
            dst = dstDir + "/" + filePath
            shutil.move(os.path.abspath(filePath), os.path.abspath(dst))
    else:
        'Can not move htmls to designated folder'


def last_month():
    '''
    Return the previous month in the format of YYYY-MM
    '''
    month = datetime.date.today().month 
    if month == 1:
        ll = str(datetime.date.today().year) + '-12' 
    elif month < 11:
        ll = str(datetime.date.today().year) + '-0' + str(month-1)
    else:
        ll = str(datetime.date.today().year) + '-' + str(month-1)

    return ll 