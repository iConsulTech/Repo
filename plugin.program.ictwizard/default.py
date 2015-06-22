import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader #ADDED MYSELF
import zipfile
import plugintools
import ntpath
import tools

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DEFINE GLOBAL VARIABLES
USER_AGENT   =  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' #ADDED MYSELF
base         =  'http://iconsultech.tk/tools/' #ADDED MYSELF
fanart       =  'http://iconsultech.tk/tools/images/fanart.jpg'
ADDON        =  xbmcaddon.Addon(id='plugin.program.ictwizard')
AddonID      =  'plugin.program.ictwizard'
zip          =  ADDON.getSetting('zip')
dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons'))
GUI          =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
USB          =  xbmc.translatePath(os.path.join(zip))
skin         =  xbmc.getSkinDir()
EXCLUDES     =  ['plugin.program.ictwizard'] #ADDED MYSELF
HOME         =  xbmc.translatePath('special://home/') #ADDED MYSELF
GUIFIX       = '#' #ADDED MYSELF

VERSION      = "1.0.0"
PATH         = "iConsulTech Wizard"

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DEFINE MENU ITEMS AND LINKS
def CATEGORIES(localbuildcheck,localversioncheck,id):
#ADDED MYSELF
    #updatecheck = CHECK_FOR_UPDATE(localbuildcheck,localversioncheck,id)
    #if updatecheck == True:
        #addDir('','[COLOR=dodgerblue]'+localbuildcheck+':[/COLOR] [COLOR=lime]NEW VERSION AVAILABLE[/COLOR]',id,'showinfo','icon.png','','','')
    #else:
        #addDir('','[COLOR=lime]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo','icon.png','','','')
    link = tools.OPEN_URL('http://iconsultech.tk/tools/wizard/wizard.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,7,iconimage,fanart,description)
    setView('movies', 'MAIN')
    #addDir('[COLOR dodgerblue]GUI[/COLOR] & Menu Fix','GUIFIX',9,'http://iconsultech.tk/tools/images/gui.jpg','fanart','Fix Your guisettings.xml')
    #addDir('[COLOR dodgerblue]Check For Update[/COLOR] Settings','url',10,'http://iconsultech.tk/tools/images/settings.jpg','fanart','Configure the iConsultech Wizard')
    addDir('[COLOR dodgerblue]Backup[/COLOR] Tools','url',1,'http://iconsultech.tk/tools/images/backup.jpg','fanart','Backup Your Full System')
    addDir('[COLOR dodgerblue]Restore[/COLOR] System','url',5,'http://iconsultech.tk/tools/images/restore.jpg','fanart','Restore Your Full System')
    addDir('[COLOR dodgerblue]Wipe[/COLOR] Device','url',8,'http://iconsultech.tk/tools/images/wipe.jpg','fanart','Wipe Your Entire Kodi Install')
    addDir('[COLOR dodgerblue]Wizard[/COLOR] Settings','url',10,'http://iconsultech.tk/tools/images/settings.jpg','fanart','Configure the iConsultech Wizard')

#---------------------------------------------------------------------------------------------------
#FUNCTION TO CHECK BUILD VERSION
#def CHECK_FOR_UPDATE(localbuildcheck,localversioncheck,id):
    #BaseURL = 'http://#' % (id)
    #link = tools.OPEN_URL(BaseURL).replace('\n','').replace('\r','')
    #if id != 'None':
        #versioncheckmatch = re.compile('version="(.+?)"').findall(link)
        #versioncheck  = versioncheckmatch[0] if (len(versioncheckmatch) > 0) else ''
    #if  localversioncheck < versioncheck:
        #return True
    #else:
        #return False

#---------------------------------------------------------------------------------------------------
def XfinityInstaller():
    path = os.path.join(xbmc.translatePath('special://home'),'userdata', 'sources.xml')
    if not os.path.exists(path):
        f = open(path, mode='w')
        f.write('<sources><files><source><name>.[COLOR blue]X[/COLOR]finity Installer</name><path pathversion="1">http://xfinity.xunitytalk.com</path></source></files></sources>')
        f.close()
        return

    f   = open(path, mode='r')
    str = f.read()
    f.close()
    if not'http://xfinity.xunitytalk.com' in str:
        if '</files>' in str:
            str = str.replace('</files>','<source><name>.[COLOR blue]X[/COLOR]finity Installer</name><path pathversion="1">http://xfinity.xunitytalk.com</path></source></files>')
            f = open(path, mode='w')
            f.write(str)
            f.close()
        else:
            str = str.replace('</sources>','<files><source><name>.[COLOR blue]X[/COLOR]finity Installer</name><path pathversion="1">http://xfinity.xunitytalk.com</path></source></files></sources>')
            f = open(path, mode='w')
            f.write(str)
            f.close()

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DOWNLOAD AND UPDATE KODI BUILD
#ADDED MYSELF
def UPDATE_WIZARD(name,url,description):
    choice = xbmcgui.Dialog().yesno("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", 'This full system update will [COLOR red][B]OVERWRITE[/B][/COLOR] everything on your current install including settings. Would you like to create a [COLOR lime][B]BACKUP[/B][/COLOR]?', yeslabel='YES, BACKUP',nolabel='NO, CONTINUE')
    if choice == 1:
        BACKUP()
    elif choice == 0:
        pass
    dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]', 'Kodi may [COLOR red][B]AUTO FORCE CLOSE[/B][/COLOR] to finish the update or it will prompt you to do it [COLOR lime][B]MANUALLY[/B][/COLOR].','')
    updatepath = xbmc.translatePath(os.path.join('special://home','Update'))
    if not os.path.exists(updatepath):
        os.makedirs(updatepath)
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Downloading Update.. ",'', 'Please Wait')
    lib=os.path.join(updatepath, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(1)
#ZIP UP WIZARD ADDON WIPE ADDONS AND THEN UNZIP ADDON
    ictpath = xbmc.translatePath(os.path.join(ADDONS,AddonID,''))
    icttemp = xbmc.translatePath(os.path.join(HOME,'..','ictwizard.zip'))
    tools.ARCHIVE_FILE(ictpath, icttemp)
    #deppath = xbmc.translatePath(os.path.join(ADDONS,'script.module.addon.common',''))
    #deptemp = xbmc.translatePath(os.path.join(HOME,'..','ictwizarddep.zip'))
    #tools.ARCHIVE_FILE(deppath, deptemp)
    tools.DESTROY_PATH(ADDONS)
    if not os.path.exists(ictpath):
        os.makedirs(ictpath)
    #if not os.path.exists(deppath):
        #os.makedirs(deppath)
    dp.close()
    time.sleep(1)
    dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Extracting Update File.. ",'', 'Please Wait')
    tools.READ_ZIP(icttemp)
    extract.all(icttemp,ictpath,dp)
    #tools.READ_ZIP(deptemp)
    #extract.all(deptemp,deppath,dp)
    print '======================================='
    print addonfolder
    print '======================================='
    tools.READ_ZIP(lib)
    extract.all(lib,addonfolder,dp)
    dp.close()
    #dialog = xbmcgui.Dialog()
    #time.sleep(1)
    #xbmc.executebuiltin('UnloadSkin()')
    #time.sleep(1)
    #xbmc.executebuiltin('ReloadSkin()')
    #time.sleep(1)
    #xbmc.executebuiltin("ActivateWindow(appearancesettings)")
    #while xbmc.executebuiltin("Window.IsActive(appearancesettings)"):
    #    xbmc.sleep(500)
    #try: xbmc.executebuiltin("LoadProfile(Master user)")
    #except:
    #    pass
    #dialog.ok("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", "Update process is almost complete, please [COLOR lime][B]CHANGE THE SKIN[/B][/COLOR] to the one this build was designed for.",'Then to finish the update please [COLOR white]FORCE CLOSE[/COLOR] Kodi','')
    #xbmc.executebuiltin("ActivateWindow(appearancesettings)")
    #time.sleep(1)
    KILLXBMC()

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DOWNLOAD AND UPDATE GUI SETTINGS XML FILE
#ADDED MYSELF
"""
def GUI_WIZARD(name,url,description):
    choice = xbmcgui.Dialog().yesno("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", 'This is [COLOR white]STEP 2[/COLOR] which will [COLOR red]OVERWRITE[/COLOR] your current guisettings.xml. Would you like to [COLOR white][B]BACKUP[/B][/COLOR] your exsisting guisettings.xml?', yeslabel='Yes, Backup',nolabel='No')
    if choice == 1:
        RESTORE_BACKUP_XML(name,url,description)
    elif choice == 0:
        pass
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Downloading GUI Settings.. ",'', 'Please Wait')
    lib=os.path.join(path, 'guifix.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(GUIFIX, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home/userdata'))
    time.sleep(2)
    dp.update(0,"", "Extracting Update File...")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    shutil.copyfile('home/userdata/guifix/guisettings.xml',
                'home/userdata/guisettings.xml')
    dialog = xbmcgui.Dialog()
    dialog.ok("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", "To complete the GUI fix Kodi will now force close.",'','')
    KILLXBMC()
"""
#---------------------------------------------------------------------------------------------------
#FUNCTION TO CREATE A FULL BACKUP AS A ZIP FILE
def BACKUP():
    if zip == '':
        dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','You have not set a location for your backup folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    to_backup = xbmc.translatePath(os.path.join('special://','home'))
    backup_zip = xbmc.translatePath(os.path.join(USB,'Full-Backup.zip'))
    DeletePackages()
    import zipfile

    dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Backup In Progress..",'', 'Please Wait')
    zipobj = zipfile.ZipFile(backup_zip , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(to_backup)
    for_progress = []
    ITEM =[]
    for base, dirs, files in os.walk(to_backup):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(to_backup):
        for file in files:
            for_progress.append(file)
            progress = len(for_progress) / float(N_ITEM) * 100
            dp.update(int(progress),"Backing Up..",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            if not 'temp' in dirs:
                if not 'plugin.program.ictwizard' in dirs:
                   import time
                   CUNT= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > CUNT:
                       zipobj.write(fn, fn[rootlen:])
    zipobj.close()
    dp.close()
    dialog.ok("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", "Backup Completed", '','')

#---------------------------------------------------------------------------------------------------
#FUNCTION TO RESTORE BACKUP ZIP FILE CREATED BY THE WIZARD
def RESTORE():
    import time
    dialog = xbmcgui.Dialog()
    if zip == '':
        dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Backup folder cannot be found.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])

    lib=xbmc.translatePath(os.path.join(zip,'Full-Backup.zip'))
    tools.READ_ZIP(lib)
    dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Checking Backup File.. ",'', 'Please Wait')
    HOME = xbmc.translatePath(os.path.join('special://','home'))

    dp.update(0,"", "Extracting Backup File Contents...")
    extract.all(lib,HOME,dp)
    time.sleep(1)
    XfinityInstaller()
    xbmc.executebuiltin('UpdateLocalAddons ')
    xbmc.executebuiltin("UpdateAddonRepos")
    time.sleep(1)
    xbmc.executebuiltin('UnloadSkin()')
    xbmc.executebuiltin('ReloadSkin()')
    xbmc.executebuiltin("LoadProfile(Master user)")
    dialog.ok("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", "Please Force Close Kodi to Finish the Restore", "","") #NEED TO CHANGE
    KILLXBMC()

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DEFINE THE BACKUP OPTIONS IN THE SYSTEM BACKUP TOOLS MENU
def BACKUP_OPTION():
    addDir('FULL SYSTEM BACKUP','url',3,'','','Backup Your Entire System',)
    addDir('Backup Addons [COLOR blue]ONLY[/COLOR]','addons',6,'','','Backup Your Addons')
    addDir('Backup Addon UserData [COLOR blue]ONLY[/COLOR]','addon_data',6,'','','Backup Your Addon Userdata')
    addDir('Backup Guisettings.xml',GUI,4,'','','Backup Your guisettings.xml')
    if os.path.exists(FAVS):
        addDir('Backup Favourites.xml',FAVS,4,'','','Backup Your favourites.xml')
    if os.path.exists(SOURCE):
        addDir('Backup Source.xml',SOURCE,4,'','','Backup Your sources.xml')
    if os.path.exists(ADVANCED):
        addDir('Backup Advancedsettings.xml',ADVANCED,4,'','','Backup Your advancedsettings.xml')
    if os.path.exists(KEYMAPS):
        addDir('Backup Advancedsettings.xml',KEYMAPS,4,'','','Backup Your keyboard.xml')
    if os.path.exists(RSS):
        addDir('Backup RssFeeds.xml',RSS,4,'','','Backup Your RssFeeds.xml')

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DEFINE THE RESTORE OPTIONS IN THE SYSTEM RESTORE TOOLS MENU
def RESTORE_OPTION():
    if os.path.exists(os.path.join(USB,'Full-Backup.zip')):
        addDir('FULL SYSTEM RESTORE','url',2,'','','Restore Your Entire System')

    if os.path.exists(os.path.join(USB,'addons.zip')):
        addDir('Restore Addons [COLOR blue]ONLY[/COLOR]','addons',6,'','','Restore Your Addons')


    if os.path.exists(os.path.join(USB,'addon_data.zip')):
        addDir('Restore Addon UserData [COLOR blue]ONLY[/COLOR]','addon_data',6,'','','Restore Your Addon UserData')

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        addDir('Restore Guisettings.xml',GUI,4,'','','Restore Your guisettings.xml')

    if os.path.exists(os.path.join(USB,'favourites.xml')):
        addDir('Restore Favourites.xml',FAVS,4,'','','Restore Your favourites.xml')

    if os.path.exists(os.path.join(USB,'sources.xml')):
        addDir('Restore Source.xml',SOURCE,4,'','','Restore Your sources.xml')

    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        addDir('Restore Advancedsettings.xml',ADVANCED,4,'','','Restore Your advancedsettings.xml')

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        addDir('Restore Advancedsettings.xml',KEYMAPS,4,'','','Restore Your keyboard.xml')

    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        addDir('Restore RssFeeds.xml',RSS,4,'','','Restore Your RssFeeds.xml')

#---------------------------------------------------------------------------------------------------
#FUNCTION TO RESTORE ZIP FILES
def RESTORE_ZIP_FILE(url):
    if zip == '':
        dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Backup folder cannot be found.\nPlease update the Wizard Settings and try again.','','')
        ADDON.openSettings(sys.argv[0])

    if 'addons' in url:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addons.zip'))
        DIR = ADDONS
        to_backup = ADDONS

        backup_zip = xbmc.translatePath(os.path.join(USB,'addons.zip'))
    else:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        DIR = ADDON_DATA


    if 'Backup' in name:
        DeletePackages()
        import zipfile
        import sys
        dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Backup In Progress..",'', 'Please Wait')
        zipobj = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen = len(DIR)
        for_progress = []
        ITEM =[]
        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM =len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file)
                progress = len(for_progress) / float(N_ITEM) * 100
                dp.update(int(progress),"Backing Up..",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
                fn = os.path.join(base, file)
                if not 'temp' in dirs:
                    if not 'plugin.program.ictwizard' in dirs:
                       import time
                       CUNT= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       if FILE_DATE > CUNT:
                           zipobj.write(fn, fn[rootlen:])
        zipobj.close()
        dp.close()
        dialog.ok("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", "Backup Completed.", '','')
    else:

        dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Checking Backup File..",'', 'Please Wait')

        import time
        dp.update(0,"", "Extracting Backup File Contents...")
        extract.all(ZIPFILE,DIR,dp)

        time.sleep(1)
        XfinityInstaller()
        xbmc.executebuiltin('UpdateLocalAddons ')
        xbmc.executebuiltin("UpdateAddonRepos")
        dialog.ok("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", "The selected system files have been restored successfully!",'','')
        #xbmc.executebuiltin("ActivateWindow(appearancesettings)")

#---------------------------------------------------------------------------------------------------
#FUNCTION TO RESTORE AND BACKUP XML FILES
def RESTORE_BACKUP_XML(name,url,description):
    if 'Backup' in name:
        TO_READ   = open(url).read()
        TO_WRITE  = os.path.join(USB,description.split('Your ')[1])

        f = open(TO_WRITE, mode='w')
        f.write(TO_READ)
        f.close()

    else:

        if 'guisettings.xml' in description:
            a = open(os.path.join(USB,description.split('Your ')[1])).read()

            r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin

            match=re.compile(r).findall(a)
            print match
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&')
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))
        else:
            TO_WRITE   = os.path.join(url)
            TO_READ  = open(os.path.join(USB,description.split('Your ')[1])).read()

            f = open(TO_WRITE, mode='w')
            f.write(TO_READ)
            f.close()
    dialog.ok("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", "", 'All Done !','')

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DELETE DOWNLOAD PACKAGES/ZIP FILES
def DeletePackages():
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))

    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)

    # Count files and give option to delete
        if file_count > 0:

            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

#---------------------------------------------------------------------------------------------------
#FUNCTION TO FORCE CLOSE XBMC/KODI
#ADDED MYSELF
def KILLXBMC():
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
#ADDED MYSELF
#Could possibly do away with this and use xbmc.getInfoLabel("System.BuildVersion") in the killxbmc function
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

#---------------------------------------------------------------------------------------------------
#FUNCTION TO WIPE ENTIRE XBMC/KODI BUILD - FRESH START - EXCLUDES THE ICT WIZARD
#ADDED MYSELF
def WIPEXBMC():
    if skin!= "skin.confluence":
        dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Please switch to the default Confluence skin','before performing a wipe.','')
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
        return
    else:
        choice = xbmcgui.Dialog().yesno("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", '[COLOR red]VERY IMPORTANT[/COLOR]: This will completely wipe your install.', 'Would you like to create a [COLOR lime][B]BACKUP[/B][/COLOR] before proceeding?', '', yeslabel='YES, BACKUP',nolabel='NO, CONTINUE')
        if choice == 1:
            BACKUP()
        choice = xbmcgui.Dialog().yesno("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", 'Are you [COLOR lime][B]Absolutely Certain[/B][/COLOR] you want to wipe this install?', '', 'All addons and settings will be completely wiped!', yeslabel='YES, WIPE',nolabel='NO, CANCEL')
        if choice == 0:
            return
        elif choice == 1:
            dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Wiping Install",'', 'Please Wait')
            try:
                for root, dirs, files in os.walk(HOME,topdown=True):
                    dirs[:] = [d for d in dirs if d not in EXCLUDES]
                    for name in files:
                        try:
                            os.remove(os.path.join(root,name))
                            os.rmdir(os.path.join(root,name))
                        except: pass

                    for name in dirs:
                        try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                        except: pass
 #               if not failed:
 #                   print"community.builds.WIPEXBMC All user files removed, you now have a clean install"
 #                   dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Wipe Successful, please restart Kodi for changes to take effect.','','')
 #               else:
 #                   print"community.builds.WipeXBMC User files partially removed"
 #                   dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Wipe Successful, please restart Kodi for changes to take effect.','','')
            except: pass
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Wipe Successful, please restart Kodi for changes to take effect.','','')

#---------------------------------------------------------------------------------------------------
#FUNCTION TO REMOVE ANY EMPTY FOLDER LEFT BEHIND AFTER WIPE
#ADDED MYSELF
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
#FUNCTION TO OPEN ADDON/WIZARD SETTINGS
#ADDED MYSELF
def ADDON_SETTINGS():
    ADDON.openSettings(sys.argv[0])

#---------------------------------------------------------------------------------------------------
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DEFINE THE ARGUMENTS AVAILABLE IN THE MENU ITEMS
def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==None or mode==5 or mode==1 or mode==6 or url==None or len(url)<1:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

#---------------------------------------------------------------------------------------------------
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None
localbuildcheck=None
localversioncheck=None

#---------------------------------------------------------------------------------------------------
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass

#---------------------------------------------------------------------------------------------------
#ADDED MYSELF
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)

#---------------------------------------------------------------------------------------------------
#ADDED MYSELF
def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )

#---------------------------------------------------------------------------------------------------
if mode==None or url==None or len(url)<1:
        CATEGORIES(localbuildcheck,localversioncheck,id)

elif mode==1:
        BACKUP_OPTION()

elif mode==2:
        print "############   RESTORE  #################"
        RESTORE()

elif mode==3:
        print "############   BACKUP  #################"
        BACKUP()

elif mode==4:
        print "############   RESTORE_BACKUP_XML #################"
        RESTORE_BACKUP_XML(name,url,description)

elif mode==5:
        print "############   RESTORE_OPTION   #################"
        RESTORE_OPTION()

elif mode==6:
        print "############   RESTORE_ZIP_FILE   #################"
        RESTORE_ZIP_FILE(url)

#ADDED MYSELF
elif mode==7:
        print "############   UPDATE_WIZARD   #################"
        UPDATE_WIZARD(name,url,description)

# ADDED MYSELF
elif mode==8:
        print "############   WIPE_XBMC   #################"
        WIPEXBMC()

#ADDED MYSELF
#elif mode==9:
        #print "############   GUI_WIZARD   #################"
        #GUI_WIZARD(name,url,description)

#ADDED MYSELF
elif mode==10:
        print "############   OPEN_ADDON_SETTINGS   #################"
        ADDON_SETTINGS()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
