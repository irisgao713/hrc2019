import glob
import os
import shutil


os.chdir('../results') 
def movefile(dstDir):
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


movefile("../results/raw_html/roo/2020-02")