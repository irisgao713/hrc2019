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