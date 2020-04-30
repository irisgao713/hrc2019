import datetime
import time
import sys
import glob
import numpy as np
import pandas as pd
import re
import os
from util.util import getPath

filename = 'parsed_raw/apa/listings-2020-04.csv'
all_files = ['raw/listings-2020-01-10.csv','raw/listings-2020-01-23.csv','raw/listings-2020-01-30.csv','raw/listings-2020-01-30-1.csv','raw/listings-2020-01-30-2.csv']
dst = 'processed'
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

    def clean_symbols(row,col):
        return re.sub(r'[^\w]', ' ', str(row[col]))
    
    def get_numbers(row,col): 
        array = re.findall(r'[0-9]+', str(row[col])) 
        if array:
            ans = ''
            for num in array:
                ans += num
            return ans
        else:
            return ''

    def find_bed(row,col):
        array = re.findall(r"(\d+)BR", str(row[col])) 
        if array:
            return array[0]
        else:
            return ''

    def find_bath(row,col):
        array = re.findall(r"(\d+)Ba", str(row[col])) 
        if array:
            return array[0]
        else:
            return ''


    def find_availability(row,col):
        tags = str(row[col]).split(",")
        ans = ''
        for t in tags:
            if 'available' in t:
                ans =  t.partition('available')[2]
        
        return ans


    def find_pets(row,col):
        tags = str(row[col]).split(",")
        ans = ''
        for t in tags:
            if 'cats' in t:
                ans += 'cats '
            elif 'dogs' in t:
                ans += 'dogs '

        
        return ans


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


    ########## Actual work ##############################



    to_do = ['price','location','map_address','rooms','sqft']
    num_only = ['price','rooms','sqft']
    df = pd.read_csv(file_name)


    # If title is  nan then drop row
    df = df.dropna(subset = ['title','description'])

    # Deduplication
    df.drop_duplicates(subset =['title'], keep = 'first', inplace = True)

    # Remove units and weird symbols
    for j in to_do:
        df[j]=df.apply(clean_symbols,col=j,axis = 1)
    for k in num_only:
        df[k]=df.apply(get_numbers,col=k,axis = 1)


    # extract url from description
    #df['description'] = df.apply(clean_description,col='description',axis=1)
    df['url_in_text']= df.apply(find_url,col='description',axis=1)
    df['bed'] = df.apply(find_bed,col='tags',axis=1)
    df['bath'] = df.apply(find_bath,col='tags',axis=1)
    df['available_from'] = df.apply(find_availability,col='tags',axis=1)
    df['pets_allowed'] = df.apply(find_pets,col='tags',axis=1)


    # Rearrange columns
    df = df[['date','domain','lat','long','map_address','location','title','rooms','sqft','bed','bath','price','num_of_images','available_from','pets_allowed','url_in_text']]
    
    if not os.path.exists(dst):
        os.mkdir(dst)
        print('Created directed named processed')

     
    saved_to = os.path.splitext(os.path.basename(filename))[0]
    #prefix  = os.getcwd()
    #filepath = prefix +'/'+ dst + '/' + saved_to + extension,
    filepath = os.path.abspath(dst + '/' + saved_to + extension)
    print('Write to: ' + filepath)
    df.to_csv (filepath, header=True)





# #combine all files in the list
# combined_csv = pd.concat([pd.read_csv(f) for f in all_files ])
# #export to csv
# combined_csv.to_csv( "raw/listings_jan.csv", index=False, encoding='utf-8-sig')

process(filename)