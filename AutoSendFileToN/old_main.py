import sys, os, myshutil, errno, hashlib, datetime, progressbar

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    AdaptiveETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer

a = datetime.datetime.now()
print "start at: "+str(a) + "\n"

productName = "iClone Character Creator\\"
version = "2.1\\"
previousVersion = "2.0\\"

localFolder = "D:\\d\\(Projects)\\CC\\2.1\\Installer\\"

mainFolderPath = "N:\\Master_Source_Neutral\\iClone Character Creator\\"
mainPatchFolderPath = "N:\\Master_Source_Neutral\\iClone Character Creator\\Patchs\\"

langFolderPath = "N:\\Master_Source_Languages\\iClone Character Creator\\Enu\\"
langPatchFolderPath = "N:\\Master_Source_Languages\\iClone Character Creator\\Patchs\\Enu\\"

localSourceFullPath = localFolder + "Full\\"
localSourceTrialPath = localFolder + "Lite\\"

localMainPath = localFolder + "Temp\\Master_Source_Neutral\\iClone Character Creator\\"
localMainPatchPath = localFolder + "Temp\\Master_Source_Neutral\\iClone Character Creator\\Patchs\\"

localLangPath = localFolder + "Temp\\Master_Source_Languages\\iClone Character Creator\\Enu\\"
localLangPatchPath = localFolder + "Temp\\Master_Source_Languages\\iClone Character Creator\\Patchs\\Enu\\"

common = "Common\\"
full = "Full\\"
trial = "Lite\\"

userData = "Data\\"
customData = "Data\\Custom Common\\"
templateCommonData = "Data\\Template Common\\"
templateFullData = "Data\\Template Full\\"
templateTrialData = "Data\\Template Lite\\"

extraData = "Extra\\"

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
        #print src.split( "\\", len(src.split("\\")) )[len(src.split("\\"))-1] + " created"
    #else:
        #print src.split( "\\", len(src.split("\\")) )[len(src.split("\\"))-1] + " exists"

def initMainInstaller():
    try:
        createFolder( mainFolderPath+version+common )
        createFolder( mainFolderPath+version+full )
        createFolder( mainFolderPath+version+trial )
        createFolder( mainPatchFolderPath+version+common )
        createFolder( mainPatchFolderPath+version+full )
        createFolder( mainPatchFolderPath+version+trial )
    except:
        print "except"

def initLangInstaller():
    try:
        createFolder( langFolderPath+version+common )
        createFolder( langFolderPath+version+full )
        createFolder( langFolderPath+version+trial )
        createFolder( langPatchFolderPath+version+common )
        createFolder( langPatchFolderPath+version+full )
        createFolder( langPatchFolderPath+version+trial )
    except:
        print "except"

def initTemp():
    try:
        myshutil.rmtree(localMainPath+version)
        myshutil.rmtree(localMainPatchPath+version)
        myshutil.rmtree(localLangPath+version)
        myshutil.rmtree(localLangPatchPath+version)
    except:
        print "not find folders"

    createFolder( localMainPath+version+common )
    createFolder( localMainPath+version+full )
    createFolder( localMainPath+version+trial )
    createFolder( localMainPatchPath+version+common )
    createFolder( localMainPatchPath+version+full )
    createFolder( localMainPatchPath+version+trial )
    
    createFolder( localLangPath+version+common )
    createFolder( localLangPath+version+full )
    createFolder( localLangPath+version+trial )
    createFolder( localLangPatchPath+version+common )
    createFolder( localLangPatchPath+version+full )
    createFolder( localLangPatchPath+version+trial )

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
                        noneCommonPath = aFile.replace( _a, _noneCommon )
                        if not os.path.exists(os.path.dirname(noneCommonPath)):
                            os.makedirs(os.path.dirname(noneCommonPath))
                        myshutil.copyfile(aFile, noneCommonPath)
                except:
                    diff_count += 1
                    noneCommonPath = aFile.replace( _a, _noneCommon )
                    if not os.path.exists(os.path.dirname(noneCommonPath)):
                        os.makedirs(os.path.dirname(noneCommonPath))
                    myshutil.copyfile(aFile, noneCommonPath)
                
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
            except:
                print "Unknown Error"
    print " same_count:" + str(same_count)
    print " diff_count:" + str(diff_count) + "\n"

def moveFiles( _src, _dst ):
    for src_dir, dirs, files in os.walk(_src):
        dst_dir = src_dir.replace(_src, _dst, 1)
        if not os.path.exists(dst_dir):
            #print dst_dir
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            myshutil.move(src_file, dst_dir)

def copyFiles( _src, _dst ):
    for src_dir, dirs, files in os.walk(_src):
        dst_dir = src_dir.replace(_src, _dst, 1)
        if not os.path.exists(dst_dir):
            #print dst_dir
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            myshutil.copy(src_file, dst_dir)

def move_to_lang():
    moveFiles(localMainPath+version+common+"\\Resource\\",localLangPath+version+common+"\\Resource\\" )
    moveFiles(localMainPath+version+full+"\\Resource\\",localLangPath+version+full+"\\Resource\\")
    moveFiles(localMainPath+version+trial+"\\Resource\\",localLangPath+version+trial+"\\Resource\\")
    
    copyFiles( localFolder+userData, localLangPath+version+userData)
    copyFiles( localFolder+extraData, localLangPath+version+"Common\\" )
    
    #moveFiles(localMainPath+version+trial+"\\Resource\\",localLangPath+version+trial+"\\Resource\\")
    
    

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
        
        myshutil.rmtree(mainFolderPath+version)
        myshutil.rmtree(mainPatchFolderPath+version)
        myshutil.rmtree(langFolderPath+version)
        myshutil.rmtree(langPatchFolderPath+version)
        
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unknown Error"
        
    start_to_copy(localMainPath+version,mainFolderPath+version, "copy to master")
    start_to_copy(localMainPatchPath+version,mainPatchFolderPath+version, "copy to master patch")
    start_to_copy(localLangPath+version,langFolderPath+version, "copy to lang")
    start_to_copy(localLangPatchPath+version,langPatchFolderPath+version, "copy to lang patch")
    
    '''
    start_to_copy( localFolder+userData, langFolderPath+version+userData, "copy to user data" )
    start_to_copy( localFolder+userData, langPatchFolderPath+version+userData, "copy to user data" )
    
    start_to_copy( localFolder+extraData, langFolderPath+version+"Common\\", "copy to info data" )
    start_to_copy( localFolder+extraData, langPatchFolderPath+version+"Common\\", "copy to info data" )
    '''

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

    
def renameFolder():
    try:
        os.remove( localSourceFullPath+"\\Bin64\\ccprcustombuild.bin" )
    except:
        print "No ccprcustombuild.bin detected in Full."
    try:
        os.remove( localSourceTrialPath+"\\Bin64\\ccprcustombuild.bin" )
    except:
        print "No ccprcustombuild.bin detected in Lite."
    try:
        myshutil.copyfile( localSourceFullPath+"\\Program\\Default\\filemap.ini", localFolder+extraData+"\\Program\\Default\\filemap.ini" )
    except:
        print "Error filemap.ini."

def copyEmptyFolder():
    try:
        myshutil.copytree ( localFolder+templateCommonData+"Character Creator 2 for iClone Template\\Motion", localLangPatchPath+version+"Data\\Template Common\\Character Creator 2 for iClone Template\\Motion" )
    except:
        print "already exist."
    try:
        myshutil.copytree ( localFolder+templateCommonData+"Character Creator 2 for iClone Template\\Texture", localLangPatchPath+version+"Data\\Template Common\\Character Creator 2 for iClone Template\\Texture" )
    except:
        print "already exist."
    try:
        myshutil.copytree ( localFolder+customData+"Character Creator 2 for iClone Custom\\Motion", localLangPatchPath+version+"Data\\Custom Common\\Character Creator 2 for iClone Custom\\Motion" )
    except:
        print "already exist."
    try:
        myshutil.copytree ( localFolder+customData+"Character Creator 2 for iClone Custom\\Texture", localLangPatchPath+version+"Data\\Custom Common\\Character Creator 2 for iClone Custom\\Texture" )
    except:
        print "already exist."

renameFolder()
initMainInstaller()
initLangInstaller()
initTemp()
copyEmptyFolder()
compare_two_folders( localSourceFullPath, localSourceTrialPath, localMainPath+version+common, localMainPath+version+full  )
compare_two_folders( localSourceTrialPath, localSourceFullPath, localMainPath+version+common, localMainPath+version+trial  )

move_to_lang()
makePatch( localMainPath+version, localMainPath+previousVersion, localMainPatchPath+version )
makePatch( localLangPath+version, localLangPath+previousVersion, localLangPatchPath+version )
copy_to_server()


b = datetime.datetime.now()
print "end at:"+str(b) + "\n"

print "total cost:"+str((b-a))