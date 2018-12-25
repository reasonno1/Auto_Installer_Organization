import sys, os, myshutil, errno, hashlib, datetime, progressbar

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    AdaptiveETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer

a = datetime.datetime.now()
print "start at: "+str(a) + "\n"

def compare_two_folders( _a, _b ):
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
                    #print os.path.isfile(os.path.abspath(bFile))
                    if (not os.path.isfile(os.path.abspath(bFile))):
                        print (os.path.abspath(bFile))
                        diff_count += 1

                except:
                    diff_count += 1
                    #print (os.path.split(aFile)[1])
                
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
            except:
                print "Unknown Error"
    print " same_count:" + str(same_count)
    print " diff_count:" + str(diff_count) + "\n"

#compare_two_folders( "D:\\d\\(Projects)\\CC\\2.1\\Installer\\Full", "D:\\d\\(Projects)\\CC\\2.01\\Installer\\Full\\" )
compare_two_folders( "D:\\d\\(Projects)\\CC\\2.0\\Installer\\Full\\", "D:\\d\\(Projects)\\CC\\2.1\\Installer\\Full\\" )


b = datetime.datetime.now()
print "end at:"+str(b) + "\n"

print "total cost:"+str((b-a))