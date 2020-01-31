# include standard modules
import getopt, sys

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
