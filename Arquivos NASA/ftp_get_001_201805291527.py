#
# PPS Python ftp script
#
# Usage:  python <script name>
#

import os, sys, re, hashlib
from getpass import getpass
from ftplib import FTP

downloadCount=0
skipCount=0

def hashfile(filename, blocksize=65536):
    hasher = hashlib.sha1()
    localfile=open(filename, 'rb')
    buf = localfile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = localfile.read(blocksize)
    localfile.close()
    return hasher.hexdigest()

def getFile(filepath,cksum=None):
    global downloadCount,skipCount
    path,filename=os.path.split(filepath)
    connection.cwd(path)
    download=True
    ftpSize=connection.size (filename)
    # determine if file exists in local directory
    if (os.path.exists(filename)):
        # check size and cksum
        if (cksum):
            sha = hashfile(filename)
            if (cksum == sha):
                download=False
        else:
            filesize=os.path.getsize(filename)
            if (ftpSize==filesize):
                download=False

    if (download):
        # if not exists or file checks do not match, get file.
        downloadCount+=1
        sys.stdout.write( str(downloadCount)+') Downloading '+filename+'   '+str(ftpSize)+' bytes  ')
        sys.stdout.flush()
        localfile=open(filename, 'wb')
        connection.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()

        if (cksum):
            sys.stdout.write('cksum ')
            sys.stdout.flush()
            sha = hashfile(filename)
            if (cksum == sha):
                print ('Pass')
            else:
                print ('FAIL')
        else:
            print ('Done')
    else:
            print ('Already downloaded '+filename)
            skipCount+=1


if __name__ == '__main__':
    userinfo=('thaina_lessa@hotmail.com','thaina_lessa@hotmail.com')
    print ('Connecting to PPS')
    connection = FTP('arthurhou.pps.eosdis.nasa.gov')
    print (connection.getwelcome())
    connection.login(*userinfo)
    connection.sendcmd('TYPE i')

#
# The following is the list of PPS files to transfer:
#
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170530.03.7.HDF.gz','05257feca65ef9ea7135ce57186cd33ebe0c73fd')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170530.06.7.HDF.gz','226cf2f577b26dbe6e38ecb9355df029c9b191e6')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170530.09.7.HDF.gz','7c63efb178053eccdd210e951ff6669eebff46c8')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170530.12.7.HDF.gz','a328c1615420408fd9594c80cfb635484a3e3a82')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170530.15.7.HDF.gz','b27dcf3e68d2b072f0cb00376f401c69298a238b')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170530.18.7.HDF.gz','1eee4f16562920effbf5e7a35512339a163af6e4')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170530.21.7.HDF.gz','69c1f046325bb9162e077f3646c44b801ce69aac')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170531.00.7.HDF.gz','77baf737eff469cab862f407075dcc854e7c383d')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170531.03.7.HDF.gz','5d1a7d94a215d55a33b553e904644cf304f2929b')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170531.06.7.HDF.gz','fda593f8a23d020ee0fffc66d95f1fb93bc323eb')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170531.09.7.HDF.gz','06c71d3485f8c7db62938ca96cc9b7b419a1b5e2')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170531.12.7.HDF.gz','86ce8695ebad684906a5c0689641a0843319498e')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170531.15.7.HDF.gz','a414bcdd5d3982e53e615faa7f3daa9517a4f375')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170531.18.7.HDF.gz','cc3f6025adea705955a78960e5f504cbac160c4c')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170531.21.7.HDF.gz','d6093f98a06f74f0204019b325acf628593839e9')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170601.00.7.HDF.gz','aabc4b207ca0eb834df4ec83faa0429a610a195c')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170601.03.7.HDF.gz','cc236c3592ef7729f0feb8b832022e7dd1b32f29')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170601.06.7.HDF.gz','e4d9368540c212ac4a67896dbf2cfb6209eb53a3')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170601.09.7.HDF.gz','514cfd34011a573e0c2e9e908506460e9f9e915d')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170601.12.7.HDF.gz','af21c5f4c602c6bb5be67fab3aa6c5d19903352f')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170601.15.7.HDF.gz','fb55b8fc013a867ec396e13563a3c915b222e3d8')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170601.18.7.HDF.gz','78e1ef40f35849871d3bf424e5129daf50c001bf')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170601.21.7.HDF.gz','b6b4b4efe58281ab95c922fb2fdb76217a960a15')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170602.00.7.HDF.gz','256adf2b5dcca231624786e3d3ddf2b670405080')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170602.03.7.HDF.gz','b38e883622eb0c6667b22b25a12db83a145d0e55')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170602.06.7.HDF.gz','53c95efe07d81bda993bcc999210f723ee2619ba')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170602.09.7.HDF.gz','dda5c6310445d7de07a021e11a47fdb1fa0d1946')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170602.12.7.HDF.gz','273ab4fd128d120b0e633f151dd610fc173964f2')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170602.15.7.HDF.gz','f31517c9acfa27ea8230f546b516768e37b7f7bb')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170602.18.7.HDF.gz','877b1d3f95e3cf9fb45dabb46d927c4c265355dc')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170602.21.7.HDF.gz','e997fa2c54c2d733357d5fc1b9a911eb1c89b273')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170603.00.7.HDF.gz','8bc4701957d5ac08a7ea8c7144d034578c4ef88a')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170603.03.7.HDF.gz','59005babdc141d45a6fc5fe3618583726b424f52')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170603.06.7.HDF.gz','433f6d597a1cfe7c49a395e2e74dd6491127ce37')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170603.09.7.HDF.gz','0d1b9e0ce9b7dc9bd6bc95f9e3197bdcea8966f2')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170603.12.7.HDF.gz','5ade4d6369badfaa7ed43e352b2f4fd76f09a38b')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170603.15.7.HDF.gz','308a5415ed8cc375934cbb1ba1832dc6e26597e6')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170603.18.7.HDF.gz','cd9462ae2a605b3568c3abb7af3bbfad7d6f7bf4')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170603.21.7.HDF.gz','036b220ce0018d935700414b9002c35b69ea3862')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170604.00.7.HDF.gz','b5aa0d3d98f0e39f897491737ee166dc987600fc')
    getFile('/gpmuser/thaina_lessa@hotmail.com/pgs/3B42-SP-36W9S35W10S.20170604.03.7.HDF.gz','384358f1768c397f1e2f465bf5690f5913031af2')
#
# Transfer complete; close connection
#
    connection.quit()
    print ('Number of files downloaded: '+str(downloadCount))
    if (skipCount>0):
        print ('Number of files already downloaded: '+str(skipCount))
