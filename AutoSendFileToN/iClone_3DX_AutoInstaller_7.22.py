import sys, os, myshutil, errno, hashlib, datetime, progressbar

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    AdaptiveETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer

a = datetime.datetime.now()
print "start at: "+str(a) + "\n"

################################# Path Setting #################################

productName = "iClone 3DXchange7\\"
version = "7.21\\"
previousVersion = ["7.2\\"]

SourcePath = "D:\\CanPy\\Auto_Installer\\iClone_3DX_Program\\" + version

ServerMainPath = "N:\\Master_Source_Neutral\\iClone 3DXchange7\\"
ServerMainPatchPath = "N:\\Master_Source_Neutral\\iClone 3DXchange7\\Patchs\\"

ServerLangPath = "N:\\Master_Source_Languages\\iClone 3DXchange7\\Enu\\"
ServerLangPatchPath = "N:\\Master_Source_Languages\\iClone 3DXchange7\\Patchs\\Enu\\"

# ServerMainPath = "D:\\CanPy\\Auto_Installer\\Master_Source_Neutral\\iClone 3DXchange7\\"
# ServerMainPatchPath = "D:\\CanPy\\Auto_Installer\\Master_Source_Neutral\\iClone 3DXchange7\\Patchs\\"
#
# ServerLangPath = "D:\\CanPy\\Auto_Installer\\Master_Source_Languages\\iClone 3DXchange7\\Enu\\"
# ServerLangPatchPath = "D:\\CanPy\\Auto_Installer\\Master_Source_Languages\\iClone 3DXchange7\\Patchs\\Enu\\"

TempMainPath = "D:\\CanPy\\Auto_Installer\\Temp\\Master_Source_Neutral\\iClone 3DXchange7\\"
TempMainPatchPath = "D:\\CanPy\\Auto_Installer\\Temp\\Master_Source_Neutral\\iClone 3DXchange7\\Patchs\\"

TempLangPath = "D:\\CanPy\\Auto_Installer\\Temp\\Master_Source_Languages\\iClone 3DXchange7\\Enu\\"
TempLangPatchPath = "D:\\CanPy\\Auto_Installer\\Temp\\Master_Source_Languages\\iClone 3DXchange7\\Patchs\\Enu\\"

common = "Common\\"
common_rea = "Common_Reallusion\\"
binFolder = "Bin\\"

pipeline = "Pipeline\\"
full = "Pro\\"
trial = "Trial\\"
extraDataPath = "D:\\CanPy\\Auto_Installer\\Extra_3DX7\\"
#########################################################################

def copyDirectory(src, dest):
    try:
        myshutil.copytree(src, dest)
    # Directories are the same
    except myshutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

def makePatch( _currentVersionPath, _previousVersionPath, _currentVersionPatchPath ):
    patchCount = 0
    for dirPath, dirNames, fileNames in os.walk(_currentVersionPath):
        for f in fileNames:
            newerFile = os.path.join(dirPath, f)
            olderFile = os.path.join(dirPath.replace( _currentVersionPath, _previousVersionPath ), f)
            tempPath = newerFile.replace( _currentVersionPath, _currentVersionPatchPath )
            try:
                if hashlib.md5(open(newerFile, 'rb').read()).hexdigest() != hashlib.md5(open(olderFile, 'rb').read()).hexdigest():
                    patchCount += 1
                    if not os.path.exists(os.path.dirname(tempPath)):
                        os.makedirs(os.path.dirname(tempPath))
                    myshutil.copyfile(newerFile, tempPath)
            #except IOError as e:
                #print "I/O error({0}): {1}".format(e.errno, e.strerror)     
            except:
                patchCount += 1
                if not os.path.exists(os.path.dirname(tempPath)):
                    os.makedirs(os.path.dirname(tempPath))
                myshutil.copyfile(newerFile, tempPath)
                #t = 1
                #print "Unknown"
    print _currentVersionPatchPath + "\n" + " have " + str(patchCount ) + " files are diff" + "\n"
                
def createFolder( src ):
    if not os.path.exists(src):
        os.makedirs(src)

def moveFiles(_src, _dst):
    for src_dir, dirs, files in os.walk(_src):
        dst_dir = src_dir.replace(_src, _dst, 1)
        if not os.path.exists(dst_dir):
            # print dst_dir
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            myshutil.move(src_file, dst_dir)

def copyFiles(_src, _dst):
    for src_dir, dirs, files in os.walk(_src):
        dst_dir = src_dir.replace(_src, _dst, 1)
        if not os.path.exists(dst_dir):
            # print dst_dir
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            myshutil.copy(src_file, dst_dir)

#########################################################################

## Create Main and Patch folder in Master_Source_Neutral ##
def initMainInstaller():
    try:
        createFolder(ServerMainPath + version + common)
        createFolder(ServerMainPath + version + pipeline)
        createFolder(ServerMainPath + version + full)
        createFolder(ServerMainPath + version + trial)

        createFolder(ServerMainPatchPath + version + common)
        createFolder(ServerMainPatchPath + version + pipeline)
        createFolder(ServerMainPatchPath + version + full)
        createFolder(ServerMainPatchPath + version + trial)
    except:
        print "initMainInstaller Folder Exist. \n"

## Create Main and Patch folder in Master_Source_Languages ##
def initLangInstaller():
    try:
        createFolder(ServerLangPath + version + common)
        createFolder(ServerLangPath + version + common_rea)
        createFolder(ServerLangPath + version + pipeline)
        createFolder(ServerLangPath + version + full)
        createFolder(ServerLangPath + version + trial)

        createFolder(ServerLangPatchPath + version + common)
        createFolder(ServerLangPatchPath + version + common_rea)

    except:
        print "initLangInstaller Folder Exist. \n"

## Create Main and Patch folder in Local Temp ##
def initTemp():
    try:
        myshutil.rmtree(TempMainPath + version)
        myshutil.rmtree(TempMainPatchPath + version)
        myshutil.rmtree(TempLangPath + version)
        myshutil.rmtree(TempLangPatchPath + version)
    except:
        print "Didn't found folders in Temp. \n"

    createFolder(TempMainPath + version + common)
    createFolder(TempMainPath + version + pipeline)
    createFolder(TempMainPath + version + full)
    createFolder(TempMainPath + version + trial)

    createFolder(TempMainPatchPath + version + common)
    createFolder(TempMainPatchPath + version + pipeline)
    createFolder(TempMainPatchPath + version + full)
    createFolder(TempMainPatchPath + version + trial)

    createFolder(TempLangPath + version + common)
    createFolder(TempLangPath + version + common_rea)
    createFolder(TempLangPath + version + pipeline)
    createFolder(TempLangPath + version + full)
    createFolder(TempLangPath + version + trial)

    createFolder(TempLangPatchPath + version + common)
    createFolder(TempLangPatchPath + version + common_rea)

def make_local_version():
    global SourcePath
    local_bin = TempMainPath + version + common + binFolder

    copyFiles(SourcePath + binFolder, local_bin)

    for f in os.listdir(local_bin):
        if os.path.isfile(local_bin + "\\" + f):
            if f == "iClone3DXchangePipeline.exe":
                myshutil.move(local_bin + "\\" + f, TempMainPath + version + pipeline + "iClone3DXchange.exe")
                print ("Move " + f)
            elif f == "iClone3DXchangePro.exe":
                myshutil.move(local_bin + "\\" + f, TempMainPath + version + full + "iClone3DXchange.exe")
                print ("Move " + f)
            elif f == "iClone3DXchangePipelineEx.exe":
                myshutil.move(local_bin + "\\" + f, TempMainPath + version + trial + "iClone3DXchange.exe")
                print ("Move " + f)
            elif f == "iClone3DXchangeStd.exe":
                os.remove(local_bin + "\\" + f)
                print ("Delete " + f)
            elif f == "3DXchangeRes.dll":
                createFolder(TempLangPath + version + common_rea + binFolder)
                myshutil.move(local_bin + "\\" + f,
                              TempLangPath + version + common_rea + "Bin\\" + f)
                print ("Move " + f)

    copyFiles(SourcePath + "3DX template", TempLangPath + version + common + "3DX template")
    copyFiles(SourcePath + "Config", TempLangPath + version + common + "Config")
    # copyFiles(SourcePath + "Content", TempLangPath + version + common + "Content")
    copyFiles(SourcePath + "Image", TempLangPath + version + common + "Image")
    print ("Copy 3DX template/Config/Content/Image folders to local Languages. \n")

    copyFiles(extraDataPath + "Languages\\Common\\", TempLangPath + version + common)
    copyFiles(extraDataPath + "Languages\\Pro\\", TempLangPath + version + full)
    copyFiles(extraDataPath + "Languages\\Trial\\", TempLangPath + version + trial)
    copyFiles(extraDataPath + "Languages\\Pipeline\\", TempLangPath + version + pipeline)
    copyFiles(extraDataPath + "Neutral\\Common\\", TempMainPath + version + common)
    print ("Copy Extra Data to local Languages. \n")

def recursive_delete_if_empty(path):
    """Recursively delete empty directories; return True
    if everything was deleted."""

    if not os.path.isdir(path):
        # If you also want to delete some files like desktop.ini, check
        # for that here, and return True if you delete them.
        return False

    # Note that the list comprehension here is necessary, a
    # generator expression would shortcut and we don't want that!
    if all([recursive_delete_if_empty(os.path.join(path, filename))
            for filename in os.listdir(path)]):
        # Either there was nothing here or it was all deleted
        os.rmdir(path)
        return True
    else:
        return False

file_copy_progress_count = 0
        
def recursive_overwrite(src, dest, pbar,ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            try:
                os.makedirs(dest)
            except:
                pass
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), pbar,
                                    ignore)
    else:
        global file_copy_progress_count
        file_copy_progress_count = file_copy_progress_count + 1
        myshutil.copyfile(src, dest)
        pbar.update(file_copy_progress_count)
        
def copy_to_server():
    try:
        print "delete server files"
        
        myshutil.rmtree(ServerMainPath+version)
        myshutil.rmtree(ServerMainPatchPath+version)
        myshutil.rmtree(ServerLangPath+version)
        myshutil.rmtree(ServerLangPatchPath+version)
        
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unknown Error"
        
    start_to_copy(TempMainPath+version, ServerMainPath+version, "Copy to Neutral")
    start_to_copy(TempMainPatchPath+version, ServerMainPatchPath+version, "Copy to Neutral Patch")

    start_to_copy(TempLangPath+version, ServerLangPath+version, "Copy to Lang")
    start_to_copy(TempLangPatchPath+version, ServerLangPatchPath+version, "Copy to Lang Patch")
    
def start_to_copy( src, dest, msg ):
    global file_copy_progress_count
    file_copy_progress_count = 0
    tempCount = 0
    for dirPath, dirNames, fileNames in os.walk(src):
        for f in fileNames:
            tempCount += 1

    print msg
    pbar = ProgressBar(widgets=[SimpleProgress()], maxval=tempCount).start()
    recursive_overwrite(src,dest, pbar)
    pbar.finish()

def remove_empty_folder(src, msg):
    path, dirs, files = os.walk(src).next()
    if len(files) == 0 and len(dirs) == 0:
        print msg
        myshutil.rmtree(src)



################################# Main #################################


initMainInstaller()
initLangInstaller()
initTemp()
make_local_version()

for p in previousVersion:
    makePatch(TempMainPath + version, TempMainPath + p, TempMainPatchPath + version)
    makePatch(TempLangPath + version, TempLangPath + p, TempLangPatchPath + version)

remove_empty_folder(TempLangPatchPath + version + common,
                    "No files in Languages/Patchs/Common. Delete it now.")
remove_empty_folder(TempLangPatchPath + version + common_rea,
                    "No files in Languages/Patchs/Common_Reallusion. Delete it now.")

copy_to_server()



b = datetime.datetime.now()
print "end at:"+str(b) + "\n"

print "total cost:"+str((b-a))