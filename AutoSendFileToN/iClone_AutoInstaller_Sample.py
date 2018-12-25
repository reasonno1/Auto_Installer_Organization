import sys, os, myshutil, errno, hashlib, datetime, progressbar

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    AdaptiveETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer

a = datetime.datetime.now()
print "start at: "+str(a) + "\n"

################################# Path Setting #################################

productName = "iClone\\"
version = "7.1\\"
previousVersion = ["7.0\\", "7.01\\", "7.02\\"]

localFolder = "D:\\CanPy\\Auto_Installer\\iClone_Program\\7.1\\"
SourceFullPath = localFolder + "Pro\\"
SourceTrialPath = localFolder + "Trial\\"
#
# ServerMainPath = "N:\\Master_Source_Neutral\\iClone 7\\"
# ServerMainPatchPath = "N:\\Master_Source_Neutral\\iClone 7\\Patchs\\"
#
# ServerLangPath = "N:\\Master_Source_Languages\\iClone 7\\Enu\\"
# ServerLangPatchPath = "N:\\Master_Source_Languages\\iClone 7\\Patchs\\Enu\\"

ServerMainPath = "D:\\CanPy\\Auto_Installer\\Master_Source_Neutral\\iClone 7\\"
ServerMainPatchPath = "D:\\CanPy\\Auto_Installer\\Master_Source_Neutral\\iClone 7\\Patchs\\"

ServerLangPath = "D:\\CanPy\\Auto_Installer\\Master_Source_Languages\\iClone 7\\Enu\\"
ServerLangPatchPath = "D:\\CanPy\\Auto_Installer\\Master_Source_Languages\\iClone 7\\Patchs\\Enu\\"

TempMainPath = "D:\\CanPy\\Auto_Installer\\Temp\\Master_Source_Neutral\\iClone\\"
TempMainPatchPath = "D:\\CanPy\\Auto_Installer\\Temp\\Master_Source_Neutral\\iClone\\Patchs\\"

TempLangPath = "D:\\CanPy\\Auto_Installer\\Temp\\Master_Source_Languages\\iClone\\Enu\\"
TempLangPatchPath = "D:\\CanPy\\Auto_Installer\\Temp\\Master_Source_Languages\\iClone\\Patchs\\Enu\\"

common = "Common\\"
full = "Pro\\"
trial = "Trial\\"
iCData = "Data\\"
extraDataPath = "D:\\CanPy\\Auto_Installer\\Extra_iC7\\"

plugin_list_path = "D:\\CanPy\\Auto_Installer\\Extra_iC7\\iC_plugin_list.txt"
plugin_list = []
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

def remove_useless_files():

    file = open(plugin_list_path)
    for line in file:
        line = line.replace("\n", "")
        plugin_list.append(line)

    print "Pulg-ins Count : " + str(len(plugin_list))

    ## Delete at Pro ##
    try:
        os.remove(SourceFullPath + "\\Program\\Thumb\\iClone\\QuickSave.png")
    except:
        print ("No QuickSave.png in Pro")
    try:
        ## Plugin  ##
        os.remove(SourceFullPath + "Bin64\\NeuronDataReader.dll")
    except:
        print ("No NeuronDataReader.dll in Pro")

    ## Pro Plugin ##
    for p in plugin_list:
        try:
            createFolder(TempMainPath + "temp_plugin\\" + full + "\\Bin64\\Plugin\\")
            myshutil.copy2(SourceFullPath + "Bin64\\Plugin\\" + p + ".dll",
                          TempMainPath + "temp_plugin\\" + full + "Bin64\\Plugin\\" + p + ".dll")

            createFolder(TempLangPath + "temp_plugin\\" + full + "Resource\\" + p + "\\")
            copyFiles(SourceFullPath + "\\Resource\\" + p + "\\",
                      TempLangPath + "temp_plugin\\" + full + "Resource\\" + p + "\\")

            print "Moving Pro Pulg-in : " + p

            os.remove(SourceFullPath + "Bin64\\Plugin\\" + p + ".dll")
            myshutil.rmtree(SourceFullPath + "\\Resource\\" + p + "\\")

            print "Deleting Pro Pulg-in : " + p
        except:
            print "No Plug-in " + p + " in Pro"

    ## Delete at Trial ##
    try:
        os.remove(SourceTrialPath + "\\Program\\Thumb\\iClone\\QuickSave.png")
    except:
        print ("No QuickSave.png in Trial")
    try:
        ## Plugin  ##
        os.remove(SourceTrialPath + "Bin64\\NeuronDataReader.dll")
    except:
        print ("No NeuronDataReader.dll in Trial")

    ## Trial Plugin ##
    for p in plugin_list:
        try:
            createFolder(TempMainPath + "temp_plugin\\" + trial + "\\Bin64\\Plugin\\")
            myshutil.copy2(SourceTrialPath + "Bin64\\Plugin\\" + p + ".dll",
                           TempMainPath + "temp_plugin\\" + trial + "Bin64\\Plugin\\" + p + ".dll")

            createFolder(TempLangPath + "temp_plugin\\" + trial + "Resource\\" + p + "\\")
            copyFiles(SourceTrialPath + "\\Resource\\" + p + "\\",
                      TempLangPath + "temp_plugin\\" + trial + "Resource\\" + p + "\\")

            print "Moving Trial Pulg-in : " + p

            os.remove(SourceTrialPath + "Bin64\\Plugin\\" + p + ".dll")
            myshutil.rmtree(SourceTrialPath + "\\Resource\\" + p + "\\")

            print "Deleting Trial Pulg-in : " + p
        except:
            print "No Plug-in " + p + " in Trial"

## Create Main and Patch folder in Master_Source_Neutral ##
def initMainInstaller():
    try:
        createFolder(ServerMainPath+version+common)
        createFolder(ServerMainPath+version+full)
        createFolder(ServerMainPath+version+trial)
        createFolder(ServerMainPatchPath+version+common)
        createFolder(ServerMainPatchPath+version+full)
        createFolder(ServerMainPatchPath+version+trial)
    except:
        print "initMainInstaller Folder Exist. \n"

## Create Main and Patch folder in Master_Source_Languages ##
def initLangInstaller():
    try:
        createFolder(ServerLangPath + version + common)
        createFolder(ServerLangPath + version + iCData)
        createFolder(ServerLangPath + version + full)
        createFolder(ServerLangPath + version + trial)

        createFolder(ServerLangPatchPath + version + common)
        createFolder(ServerLangPatchPath + version + iCData)

    except:
        print "initLangInstaller Folder Exist. \n"

## Create Main and Patch folder in Local Temp ##
def initTemp():
    try:
        myshutil.rmtree(TempMainPath+version)
        myshutil.rmtree(TempMainPatchPath+version)
        myshutil.rmtree(TempLangPath+version)
        myshutil.rmtree(TempLangPatchPath+version)
        myshutil.rmtree(TempMainPath + "temp_plugin\\")
        myshutil.rmtree(TempLangPatchPath + "temp_plugin\\")

    except:
        print "Didn't found folders in Temp. \n"

    createFolder(TempMainPath + version + common)
    createFolder(TempMainPath + version + full)
    createFolder(TempMainPath + version + trial)
    createFolder(TempMainPath + "temp_plugin\\" + full)
    createFolder(TempMainPath + "temp_plugin\\" + trial)

    createFolder(TempMainPatchPath+version+common)
    createFolder(TempMainPatchPath+version+full)
    createFolder(TempMainPatchPath+version+trial)

    createFolder(TempLangPath + version + common)
    createFolder(TempLangPath + version + iCData)
    createFolder(TempLangPath + version + full)
    createFolder(TempLangPath + version + trial)
    createFolder(TempLangPath + "temp_plugin\\" + full)
    createFolder(TempLangPath + "temp_plugin\\" + trial)

    createFolder(TempLangPatchPath + version + common)
    createFolder(TempLangPatchPath + version + iCData)

def compare_two_folders( _a, _b, _common, _noneCommon ):
    same_count = 0
    diff_count = 0
    print _a + "\n" + "compare to" + "\n" + _b
    for dirPath, dirNames, fileNames in os.walk(_a):
        #print dirPath
        for f in fileNames:
            try:
                #print f
                aFile = os.path.join(dirPath, f)
                try:
                    bFile = os.path.join(dirPath.replace( _a, _b ), f)
                    if hashlib.md5(open(aFile, 'rb').read()).hexdigest() == hashlib.md5(open(bFile, 'rb').read()).hexdigest():
                        same_count += 1
                        commonPath = aFile.replace( _a, _common )
                        if not os.path.exists(os.path.dirname(commonPath)):
                            os.makedirs(os.path.dirname(commonPath))
                        myshutil.copyfile(aFile, commonPath)
                    else:
                        diff_count += 1
                        noneCommonPath = aFile.replace( _a, _noneCommon)
                        if not os.path.exists(os.path.dirname(noneCommonPath)):
                            os.makedirs(os.path.dirname(noneCommonPath))
                        myshutil.copyfile(aFile, noneCommonPath)
                except:
                    diff_count += 1
                    noneCommonPath = aFile.replace( _a, _noneCommon)
                    if not os.path.exists(os.path.dirname(noneCommonPath)):
                        os.makedirs(os.path.dirname(noneCommonPath))
                    myshutil.copyfile(aFile, noneCommonPath)
                
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
            except:
                print "Unknown Error"
    print " same_count:" + str(same_count)
    print " diff_count:" + str(diff_count) + "\n"

def move_to_lang():
    ## Main Common/Image/Program/Resource folders ##
    moveFiles(TempMainPath + version + "Common\\Common\\",
                  TempLangPath + version + "Common\\Common\\")
    moveFiles(TempMainPath + version + "Common\\Image\\",
                  TempLangPath + version + "Common\\Image\\")
    moveFiles(TempMainPath + version + "Common\\Program\\",
                  TempLangPath + version + "Common\\Program\\")
    moveFiles(TempMainPath + version + "Common\\Resource\\",
                  TempLangPath + version + "Common\\Resource\\")
    try:
        myshutil.rmtree(TempMainPath + version + "Common\\Common\\")
        myshutil.rmtree(TempMainPath + version + "Common\\Image\\")
        myshutil.rmtree(TempMainPath + version + "Common\\Program\\")
        myshutil.rmtree(TempMainPath + version + "Common\\Resource\\")
    except:
        None

    print ("Move main Common/Image/Program/Resource folders to Lang.\n")
    copyFiles(extraDataPath + "Common\\", TempLangPath + version + "Common\\")
    copyFiles(extraDataPath + "Pro\\", TempLangPath + version + "Pro\\")
    copyFiles(extraDataPath + "Trial\\", TempLangPath + version + "Trial\\")
    copyFiles(extraDataPath + "Data\\", TempLangPath + version + "Data\\")


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

def lang_patch_content_merge():
    res_folder = TempLangPatchPath + version + iCData + "Resource for PRO Trial\\iClone Template\\"
    template_full = TempLangPatchPath + version + iCData + "Template Full\\iClone Template\\"
    moveFiles(res_folder, template_full)
    myshutil.rmtree(res_folder)
    print ("Merge Patch Content.")


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

################################# Main #################################


initMainInstaller()
initLangInstaller()
initTemp()
remove_useless_files()

compare_two_folders(SourceFullPath, SourceTrialPath,
                    TempMainPath+version+common, TempMainPath+version+full)
compare_two_folders(SourceTrialPath, SourceFullPath,
                    TempMainPath+version+common, TempMainPath+version+trial)

move_to_lang()

for p in previousVersion:
    makePatch(TempMainPath+version, TempMainPath+p, TempMainPatchPath+version)
    makePatch(TempLangPath+version, TempLangPath+p, TempLangPatchPath+version)

lang_patch_content_merge()

# copy_to_server()

b = datetime.datetime.now()
print "end at:"+str(b) + "\n"

print "total cost:"+str((b-a))