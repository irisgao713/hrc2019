
import glob
import os
import shutil

def movefile(dstDir):
    srcDir = ''
    path = srcDir + '*.{}'
    if os.path.isdir(dstDir) :
        # Iterate over all the files in source directory
        for filePath in glob.glob(path.format('html')):
            # Move each file to destination Directory
            shutil.move(filePath, dstDir)
    else:
        'Can not move htmls to designated folder'


movefile("../results/raw_html/apa/")