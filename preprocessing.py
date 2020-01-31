import datetime
import time
import sys, getopt
import glob
import numpy as np
import pandas as pd
import re
import os


dst = '../results/processed/'
extension = '.csv'

file, directory = getPath(sys.argv)


if file == '':
    #Processing a directory: assuming csv format
    path = '///'+directory+'/*.{}'
    all_filenames = [i for i in glob.glob(path.format(extension))]
    for file in all_filenames:
        process(file)


elif directory == '':
    #Processing a file: assuming csv format
    process(file)


else:
    print ('Please specify a file or a directory to process!')
    

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

def process(file_name):
# Takes in a file path and perform dasta cleaning on the file
# assuming csv format
# After preprocessing, write back the file the path speficified by @dst, with the same file name
    to_do = ['price','location','map_address','rooms','sqft']
    num_only = ['price','rooms','sqft']
    df = pd.read_csv(file_name)



    for j in to_do:
        df[j]=df.apply(clean_symbols,col=j,axis = 1)
    for k in num_only:
        df[k]=df.apply(get_numbers,col=k,axis = 1)

    #df['description'] = df.apply(clean_description,col='description',axis=1)
    df['url_in_text']= df.apply(find_url,col='description',axis=1)
    

    def clean_symbols(row,col):
        return re.sub(r'[^\w]', ' ', str(row[col]))
    
    def get_numbers(row,col): 
        array = re.findall(r'[0-9]+', str(row[col])) 
        return array 

    # def clean_description(row,col):
    #     s = str(row[col])
    #     s = re.sub('\s+', ' ', s).rstrip()
    #     s.replace(' QR Code Link to This Post ','')
    #     s = re.sub('[!@#$*+]', ' ', s)
    #     return s

    def find_url(row,col):
        s = str(row[col])

        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',s)
        urls.extend(re.findall('www[s]?.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',s))
        return urls       



