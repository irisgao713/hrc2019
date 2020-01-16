import shutil, os, glob
 
srcDir = ''
dstDir = '../results/raw_html/2020-01-16'
path = srcDir + '*.{}'
if os.path.isdir(dstDir) :
        # Iterate over all the files in source directory
    for filePath in glob.glob(path.format('html')):
            # Move each file to destination Directory
        shutil.move(filePath, dstDir)
else:
    print("sdstDir should be Directories")