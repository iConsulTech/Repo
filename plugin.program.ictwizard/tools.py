import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import zipfile
import ntpath
import requests
#import beautifulsoup

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DEFINE GLOBAL VARIABLES
base         =  'http://iconsultech.uk/tools/'
ADDON        =  xbmcaddon.Addon(id='plugin.program.ictwizard')
dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons'))
AddonID      =  'plugin.program.ictwizard'
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
skin         =  xbmc.getSkinDir()
HOME         =  xbmc.translatePath('special://home/')
notifyart    =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))


VERSION      = "1.0.1"
PATH         = "iConsulTech Wizard"

#---------------------------------------------------------------------------------------------------
#FUNCTION TO LOGIN INTO ICONSULTECH
def ICT_LOGIN():
    URL     = 'http://iconsultech.uk/wp-login.php'
    USER    = ADDON.getSetting('username')
    PASS    = ADDON.getSetting('password')
    PAYLOAD = { 'log' : USER, 'pwd' : PASS, 'wp-submit' : 'Log In'}

    request  = requests.post(URL, data=PAYLOAD)
    response = request.content

    return response

    soup = BeautifulSoup(response)
    soup.find_all('no active subscription')

'''def USER_STATUS():
    site = requests.get("http://www.iconsultech.uk/my-account")
'''
#---------------------------------------------------------------------------------------------------
#FUNCTION TO CREATE A SHORTCUT TO NOTIFICATION
def NOTIFY(title,message,times,icon):
    icon = notifyart+icon
    xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

#---------------------------------------------------------------------------------------------------
#FUNCTION TO ZIP UP TREE
def ARCHIVE_FILE(sourcefile, destfile):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp.create("[COLOR=dodgerblue][B]i[/COLOR][COLOR=white]ConsulTech Wizard[/B][/COLOR]","Archiving...",'', 'Please Wait')
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            for_progress.append(file)
            progress = len(for_progress) / float(N_ITEM) * 100
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            if not 'temp' in dirs:
                if not 'plugin.program.ictwizard' in dirs:
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])
    zipobj.close()
    dp.close()

#---------------------------------------------------------------------------------------------------
#FUCNTION TO READ A ZIP FILE AND EXTRA RELEVANT DATA
def READ_ZIP(url):
    z = zipfile.ZipFile(url, "r")
    for filename in z.namelist():

        if 'guisettings.xml' in filename:
            a = z.read(filename)
            r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            match=re.compile(r).findall(a)
            print match
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&')
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))

        if 'favourites.xml' in filename:
            a = z.read(filename)
            f = open(FAVS, mode='w')
            f.write(a)
            f.close()

        if 'sources.xml' in filename:
            a = z.read(filename)
            f = open(SOURCE, mode='w')
            f.write(a)
            f.close()

        if 'advancedsettings.xml' in filename:
            a = z.read(filename)
            f = open(ADVANCED, mode='w')
            f.write(a)
            f.close()

        if 'RssFeeds.xml' in filename:
            a = z.read(filename)
            f = open(RSS, mode='w')
            f.write(a)
            f.close()

        if 'keyboard.xml' in filename:
            a = z.read(filename)
            f = open(KEYMAPS, mode='w')
            f.write(a)
            f.close()

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DO A FULL WIPE
def DESTROY_PATH(path):
    #dp.create("[COLOR=dodgerblue][B]i[/COLOR][COLOR=white]ConsulTech Wizard[/B][/COLOR]","Wiping...",'', 'Please Wait')
    shutil.rmtree(path, ignore_errors=True)

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DELETE DOWNLOADED PACKAGES/ZIP FILES
def DELETE_PACKAGES():
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    update_cache_path = xbmc.translatePath(os.path.join('special://home/Update', ''))

    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)

    for root, dirs, files in os.walk(update_cache_path):
        file_count = 0
        file_count += len(files)

    # Count files and give option to delete
        if file_count > 0:

            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

#---------------------------------------------------------------------------------------------------
#FUNCTION TO REMOVE ANY EMPTY FOLDER LEFT BEHIND AFTER WIPE
def REMOVE_EMPTY_FOLDERS():
#initialize the counters
    print"########### Start Removing Empty Folders #########"
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
        if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
            empty_count += 1 #increment empty_count
            os.rmdir(curdir) #delete the directory
            print "successfully removed: "+curdir
        elif len(subdirs) > 0 and len(files) > 0: #check for used directories
            used_count += 1 #increment used_count

#---------------------------------------------------------------------------------------------------
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    link.replace('\r','').replace('\n','').replace('\t','')

#---------------------------------------------------------------------------------------------------
#FUNCTION TO CONVERT PHYSICAL PATHS TO SPECIAL PATHS
def FIX_SPECIAL(url):
    dp.create("[COLOR=dodgerblue]i[/COLOR][COLOR=white]ConsulTech Wizard[/COLOR][/B]","Renaming paths...",'', 'Please Wait')
    for root, dirs, files in os.walk(url):  #Search all xml files and replace physical with special
        for file in files:
            if file.endswith(".xml"):
                 dp.update(0,"Fixing",file, 'Please Wait')
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(USERDATA, 'special://profile/').replace(ADDONS,'special://home/addons/')
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()

#---------------------------------------------------------------------------------------------------
#FUNCTION TO BRING UP THE KEYBOARD
def GET_KEYBOARD( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default

#---------------------------------------------------------------------------------------------------
#FUNCTION TO ZIP UP TREE
def ARCHIVE_TREE(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            for_progress.append(file)
            progress = len(for_progress) / float(N_ITEM) * 100
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            if not 'temp' in dirs:
                if not 'plugin.program.TotalRevolution' in dirs:
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])
    zipobj.close()
    dp.close()

#---------------------------------------------------------------------------------------------------
#FUNCTION TO FORCE CLOSE XBMC/KODI
def KILL_XBMC():
    dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]', 'To finish you will need to  [COLOR lime][B]RELAUNCH KODI[/B][/COLOR] once it has force closed','') #'We will now attempt to force close Kodi, this is', 'to be used if having problems with guisettings.xml', 'sticking. Would you like to continue?'
    myplatform = PLATFORM()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close Kodi [COLOR red]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close Kodi [COLOR red]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass
        dialog.ok("[COLOR red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close Kodi. [COLOR red]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close Kodi [COLOR red]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close Kodi [COLOR red]DO NOT[/COLOR] exit cleanly via the menu.","Your platform could not be detected so just pull the power cable.")

#---------------------------------------------------------------------------------------------------
#Could possibly do away with this and use xbmc.getInfoLabel("System.BuildVersion") in the KILL_XBMC function
def PLATFORM():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
