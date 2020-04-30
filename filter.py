import datetime
import time
import sys
import glob
import numpy as np
import pandas as pd
import re
import os
from util.util import getPath

filename = 'processed/listings-2020-03.csv'
all_files = ['raw/listings-2020-01-10.csv','raw/listings-2020-01-23.csv','raw/listings-2020-01-30.csv','raw/listings-2020-01-30-1.csv','raw/listings-2020-01-30-2.csv']
dst = 'processed/bad'
extension = '.csv'

file, directory = getPath(sys.argv)

os.chdir('../results') 

# if file == '':
#     #Processing a directory: assuming csv format
#     path = directory+'/*.{}'
#     if not os.path.exists(directory):
#         print('The directory: ' + str(directory) +' does not exist!')
#         exit 
#     all_filenames = [i for i in glob.glob(path.format(extension))]
#     for file in all_filenames:
#         process(file)


# elif directory == '':
#     #Processing a file: assuming csv format
#     process(file)


# else:
#     print ('Please specify a file or a directory to process!')
    

def process(file_name):
# Takes in a file path and perform dasta cleaning on the file
# assuming csv format
# After preprocessing, write back the file the path speficified by @dst, with the same file name

    # def clean_description(row,col):
    #     s = str(row[col])
    #     s = re.sub('\s+', ' ', s).rstrip()
    #     s.replace(' QR Code Link to This Post ','')
    #     s = re.sub('[!@#$*+]', ' ', s)
    #     return s


    ########## Actual work ##############################


    df = pd.read_csv(file_name)
    new_df =df[df.lat =='' & df.long =='']

     
    saved_to = os.path.splitext(os.path.basename(filename))[0]
    #prefix  = os.getcwd()
    #filepath = prefix +'/'+ dst + '/' + saved_to + extension,
    filepath = os.path.abspath(dst + '/' + saved_to + extension)
    print('Write to: ' + filepath)
    new_df.to_csv (filepath, header=True)





# #combine all files in the list
# combined_csv = pd.concat([pd.read_csv(f) for f in all_files ])
# #export to csv
# combined_csv.to_csv( "raw/listings_jan.csv", index=False, encoding='utf-8-sig')

process(filename)