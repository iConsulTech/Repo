import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import zipfile
import plugintools
import ntpath
import tools
import cache
import requests
#import beautifulsoup

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DEFINE GLOBAL VARIABLES
USER_AGENT   =  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base         =  'http://iconsultech.uk/tools/'
fanart       =  'http://iconsultech.uk/tools/images/fanart.jpg'
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
ADDON        =  xbmcaddon.Addon(id='plugin.program.ictwizard')
AddonID      =  'plugin.program.ictwizard'
ICTADDONPATH  =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'default.py'))
zip          =  ADDON.getSetting('zip')
dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
userdatafolder = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID))
THUMBNAILS   =  xbmc.translatePath(os.path.join(USERDATA,'Thumbnails'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons'))
GUI          =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
GUIFIX       =  xbmc.translatePath(os.path.join(USERDATA,'guifix.xml'))
GUINEW       =  xbmc.translatePath(os.path.join(userdatafolder,'guinew.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
USB          =  xbmc.translatePath(os.path.join(zip))
skin         =  xbmc.getSkinDir()
EXCLUDES     =  ['plugin.program.ictwizard', 'script.module.requests']
HOME         =  xbmc.translatePath('special://home/')
tempfile     =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'temp.xml'))
guitemp      =  xbmc.translatePath(os.path.join(userdatafolder,'guitemp',''))
idfile       =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'id.xml'))

VERSION      = "1.0.1"
PATH         = "iConsulTech Wizard"

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DEFINE MENU ITEMS AND LINKS
def CATEGORIES(localbuildcheck,localversioncheck,id):
#    response = tools.ICT_LOGIN()

#    if 'login_error' in response:
#        tools.NOTIFY('Not Logged In!', 'Please go to [COLOR lime]Wizard Settings[/COLOR] and login to download updates','10000','cross.png')
#        addDir('[COLOR dodgerblue]Backup[/COLOR] Tools','url',1,'http://iconsultech.uk/tools/images/backup.jpg','fanart','Backup Your Full System')
#        addDir('[COLOR dodgerblue]Restore[/COLOR] System','url',5,'http://iconsultech.uk/tools/images/restore.jpg','fanart','Restore Your Full System')
#        addDir('[COLOR dodgerblue]Kodi[/COLOR] Cleaner','url',11,'http://iconsultech.uk/tools/images/cleaner.jpg','fanart','Delete Downloaded Zip Files')
#        addDir('[COLOR dodgerblue]Wipe[/COLOR] Device','url',8,'http://iconsultech.uk/tools/images/wipe.jpg','fanart','Wipe Your Entire Kodi Install')
#        addDir('[COLOR dodgerblue]Wizard[/COLOR] Settings','url',10,'http://iconsultech.uk/tools/images/settings.jpg','fanart','Configure the iConsultech Wizard')

    #updatecheck = CHECK_FOR_UPDATE(localbuildcheck,localversioncheck,id)
    #if updatecheck == True:
        #addDir('','[COLOR=dodgerblue]'+localbuildcheck+':[/COLOR] [COLOR=lime]NEW VERSION AVAILABLE[/COLOR]',id,'showinfo','icon.png','','','')
    #else:
        #addDir('','[COLOR=lime]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo','icon.png','','','')

    #addDir('[COLOR dodgerblue]GUI[/COLOR] & Menu Fix','GUIFIX',9,'http://iconsultech.uk/tools/images/gui.jpg','fanart','Fix Your guisettings.xml')
    #addDir('[COLOR dodgerblue]Check For Update[/COLOR] Settings','url',10,'http://iconsultech.uk/tools/images/settings.jpg','fanart','Configure the iConsultech Wizard')
    #else:
    #    username = ADDON.getSetting('username')
    #    tools.NOTIFY('Login Successful', 'Welcome back '+username,'4000','tick.png')
        link = tools.OPEN_URL('http://iconsultech.uk/tools/wizard/wizard.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addDir(name,url,13,iconimage,fanart,description)
        setView('movies', 'MAIN')
        addDir('[COLOR dodgerblue]Backup[/COLOR] Tools','url',1,'http://iconsultech.uk/tools/images/backup.jpg',fanart,'Backup Your Full System')
        addDir('[COLOR dodgerblue]Restore[/COLOR] System','url',5,'http://iconsultech.uk/tools/images/restore.jpg',fanart,'Restore Your Full System')
        addDir('[COLOR dodgerblue]Kodi[/COLOR] Cleaner','url',11,'http://iconsultech.uk/tools/images/cleaner.jpg',fanart,'Delete Downloaded Zip Files')
        addDir('[COLOR dodgerblue]Wipe[/COLOR] Device','url',8,'http://iconsultech.uk/tools/images/wipe.jpg',fanart,'Wipe Your Entire Kodi Install')
        addDir('[COLOR dodgerblue]Wizard[/COLOR] Settings','url',10,'http://iconsultech.uk/tools/images/settings.jpg',fanart,'Configure the iConsultech Wizard')
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
def ICONSULTECH():
    path = os.path.join(xbmc.translatePath('special://home'),'userdata', 'sources.xml')
    if not os.path.exists(path):
        f = open(path, mode='w')
        f.write('<sources><files><source><name>.iConsulTech</name><path pathversion="1">http://repo.iconsultech.uk</path></source></files></sources>')
        f.close()
        return

    f   = open(path, mode='r')
    str = f.read()
    f.close()
    if not'http://repo.iconsultech.uk' in str:
        if '</files>' in str:
            str = str.replace('</files>','<source><name>.iConsulTech</name><path pathversion="1">http://repo.iconsultech.uk</path></source></files>')
            f = open(path, mode='w')
            f.write(str)
            f.close()
        else:
            str = str.replace('</sources>','<files><source><name>.iConsulTech</name><path pathversion="1">http://repo.iconsultech.uk</path></source></files></sources>')
            f = open(path, mode='w')
            f.write(str)
            f.close()

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DOWNLOAD AND UPDATE PREMIUM KODI BUILD
def FREE_UPDATE_WIZARD(name,url,description):
    choice = xbmcgui.Dialog().yesno("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", 'This full system update will [COLOR red][B]OVERWRITE[/B][/COLOR] everything on your current install including settings. Would you like to create a [COLOR lime][B]BACKUP[/B][/COLOR]?', yeslabel='YES, BACKUP',nolabel='NO, CONTINUE')
    if choice == 1:
        FULL_UNIVERSAL_BACKUP()
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
    requestspath = xbmc.translatePath(os.path.join(ADDONS,'script.module.requests',''))
    requeststemp = xbmc.translatePath(os.path.join(HOME,'..','requestsmodule.zip'))
    tools.ARCHIVE_FILE(requestspath, requeststemp)
    tools.DESTROY_PATH(ADDONS)
    if not os.path.exists(ictpath):
        os.makedirs(ictpath)
    if not os.path.exists(requestspath):
        os.makedirs(requestspath)
    dp.close()
    time.sleep(1)
    dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Extracting Update File.. ",'', 'Please Wait')
    tools.READ_ZIP(icttemp)
    extract.all(icttemp,ictpath,dp)
    tools.READ_ZIP(requeststemp)
    extract.all(requeststemp,requestspath,dp)
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
    tools.KILL_XBMC()

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DOWNLOAD AND UPDATE PREMIUM KODI BUILD
def UPDATE_WIZARD(name,url,description):
    username = ADDON.getSetting('username')
    password = ADDON.getSetting('password')
    if username == '':
        if password == '':
            tools.NOTIFY('Not Logged In!', 'Please go to [COLOR lime]Wizard Settings[/COLOR] and login to download updates','10000','cross.png')
            return
    response = tools.ICT_LOGIN()
    if 'login_error' in response:
        tools.NOTIFY('Not Logged In!', 'Please go to [COLOR lime]Wizard Settings[/COLOR] and login to download updates','10000','cross.png')
        return
    else:
        choice = xbmcgui.Dialog().yesno("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", 'This full system update will [COLOR red][B]OVERWRITE[/B][/COLOR] everything on your current install including settings. Would you like to create a [COLOR lime][B]BACKUP[/B][/COLOR]?', yeslabel='YES, BACKUP',nolabel='NO, CONTINUE')
        if choice == 1:
            FULL_UNIVERSAL_BACKUP()
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
    requestspath = xbmc.translatePath(os.path.join(ADDONS,'script.module.requests',''))
    requeststemp = xbmc.translatePath(os.path.join(HOME,'..','requestsmodule.zip'))
    tools.ARCHIVE_FILE(requestspath, requeststemp)
    tools.DESTROY_PATH(ADDONS)
    if not os.path.exists(ictpath):
        os.makedirs(ictpath)
    if not os.path.exists(requestspath):
        os.makedirs(requestspath)
    dp.close()
    time.sleep(1)
    dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Extracting Update File.. ",'', 'Please Wait')
    tools.READ_ZIP(icttemp)
    extract.all(icttemp,ictpath,dp)
    tools.READ_ZIP(requeststemp)
    extract.all(requeststemp,requestspath,dp)
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
    tools.KILL_XBMC()

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DOWNLOAD AND UPDATE GUI SETTINGS XML FILE
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
    tools.KILL_XBMC()
"""

#---------------------------------------------------------------------------------------------------
#FUNCTION TO CREATE A FULL SYSTEM UNIVERSAL BACKUP - THIS RENAMES PATHS TO SPECIAL:// AND REMOVES UNWATNED FOLDERS
def FULL_UNIVERSAL_BACKUP():
    guisuccess=1
    if zip == '':
        dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','You have not set a location for your backup folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    vq = tools.GET_KEYBOARD( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'_backup.zip'))
    exclude_dirs_full =  ['plugin.program.ictwizard']
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf']
    exclude_dirs =  ['plugin.program.ictwizard','cache', 'system', 'Thumbnails', "peripheral_data",'library','keymaps']
    exclude_files = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db",'.DS_Store','.setup_complete','XBMCHelper.conf', 'advancedsettings.xml']
    message_header = "Checking and Preparing Files"
    message_header2 = "Creating Full System Backup"
    message1 = "Archiving..."
    message2 = ""
    message3 = "Please Wait"
    tools.FIX_SPECIAL(HOME)
    tools.DELETE_PACKAGES()
    tools.ARCHIVE_TREE(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)
    time.sleep(1)
    GUIname = xbmc.translatePath(os.path.join(USB, title+'_guisettings.zip'))
    zf = zipfile.ZipFile(GUIname, mode='w')
    try:
        zf.write(GUI, 'guisettings.xml', zipfile.ZIP_DEFLATED) #Copy guisettings.xml
    except: guisuccess=0
    try:
        zf.write(xbmc.translatePath(os.path.join(HOME,'userdata','profiles.xml')), 'profiles.xml', zipfile.ZIP_DEFLATED) #Copy profiles.xml
    except: pass
    zf.close()
    if guisuccess == 0:
        dialog.ok("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", '[COLOR red][B]FAILED![/B][/COLOR] The guisettings.xml file could not be found on your', 'system, please reboot and try again.', '')
    else:
        dialog.ok("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", 'Full System Backup was [COLOR lime][B]SUCCESSFUL[/B][/COLOR]!')
        dialog.ok("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", 'You can find your backup plus the GUI settings here: [COLOR dodgerblue]'+backup_zip+'[/COLOR] [COLOR dodgerblue]'+GUIname+'[/COLOR]')

#---------------------------------------------------------------------------------------------------
#FUNCTION TO RESTORE LOCAL UNIVERSAL BACKUP
def RESTORE_UNIVERSAL_BACKUP():
    exitfunction=0
    choice4=0
    if zip == '':
        dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Backup folder cannot be found.\nPlease update the Wizard Settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to restore', 'files', '.zip', False, False, USB)
    if filename == '':
        return
    if os.path.exists(GUINEW):
        if os.path.exists(GUI):
            os.remove(GUINEW)
        else:
            os.rename(GUINEW,GUI)
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
    if not os.path.exists(tempfile): #Function for debugging, creates a file that was created in previous call and subsequently deleted when run
        localfile = open(tempfile, mode='w+')
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
    try: os.rename(GUI,GUINEW) #Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    except:
        dialog.ok("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]",'No guisettings.xml file has been found.', 'Please exit Kodi and try again','')
        return
    else:
        time.sleep(1)
        readfile = open(ICTADDONPATH, mode='r')
        default_contents = readfile.read()
        readfile.close()
        tools.READ_ZIP(filename)
        dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Checking..",'', 'Please Wait')
        dp.update(0,"", "Extracting Backup File...")
        extract.all(filename,HOME,dp)
        time.sleep(1)
        clean_title = ntpath.basename(filename)
        writefile = open(idfile, mode='w+')
        writefile.write('id="none"\nname="'+clean_title+' [COLOR=yellow](Partially installed)[/COLOR]"\nversion="none"')
        writefile.close()
        cbdefaultpy = open(ICTADDONPATH, mode='w+')
        cbdefaultpy.write(default_contents)
        cbdefaultpy.close()
        try:
            os.rename(GUI,GUIFIX)
        except:
            print"NO GUISETTINGS DOWNLOADED"
        time.sleep(1)
        localfile = open(GUINEW, mode='r') #Read the original skinsettings tags and store in memory ready to replace in guinew.xml
        content = file.read(localfile)
        file.close(localfile)
        skinsettingsorig = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
        skinorig  = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
        skindefault = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
        skindefaultorig  = skindefault[0] if (len(skindefault) > 0) else ''
        lookandfeelorig = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
        lookandfeel  = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''
        try:
            localfile2 = open(GUIFIX, mode='r')
            content2 = file.read(localfile2)
            file.close(localfile2)
            skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
            skinsettingstext  = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
            skindefaultcontent = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
            skindefaulttext  = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
            lookandfeelcontent = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
            lookandfeeltext  = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
            replacefile = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)
            writefile = open(GUINEW, mode='w+')
            writefile.write(str(replacefile))
            writefile.close()
        except:
            print"NO GUISETTINGS DOWNLOADED"
        if os.path.exists(GUI):
            os.remove(GUI)
        os.rename(GUINEW,GUI)
        try:
            os.remove(GUIFIX)
        except:
            pass
        os.makedirs(guitemp)
        time.sleep(1)
        xbmc.executebuiltin('UnloadSkin()')
        time.sleep(1)
        xbmc.executebuiltin('ReloadSkin()')
        time.sleep(1)
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
        while xbmc.executebuiltin("Window.IsActive(appearancesettings)"):
            xbmc.sleep(500)
        try: xbmc.executebuiltin("LoadProfile(Master user)")
        except: pass
        dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Step 1 complete. Now please change the skin to','the one this build was designed for. Once done come back','to this wizard and restore the guisettings.zip')
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")

#---------------------------------------------------------------------------------------------------
#FUNCTION TO RESTORE LOCAL COPY OF GUISETTINGS_FIX
def RESTORE_LOCAL_GUI():
    import time
    if zip == '':
        dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Backup folder cannot be found.\nPlease update the Wizard Settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    guifilename = xbmcgui.Dialog().browse(1, 'Select the guisettings zip file you want to restore', 'files', '.zip', False, False, USB)
    if guifilename == '':
        return
    else:
        local=1
        GUI_Settings_Fix(guifilename,local)

#---------------------------------------------------------------------------------------------------
#FUNCTION TO DEFINE THE BACKUP OPTIONS IN THE SYSTEM BACKUP TOOLS MENU
def BACKUP_OPTION():
    addDir('[COLOR blue]FULL SYSTEM BACKUP[/COLOR] + [COLOR blue]GUI SETTINGS[/COLOR]','url',3,'','','Backup Your Entire System',)
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
    addDir('1. Select the [COLOR blue]BACKUP FILE[/COLOR] you want to restore..','url',2,'','','Restore Your Entire System')
    addDir('2. Select the [COLOR blue]GUI SETTINGS ZIP FILE[/COLOR] you want to restore..','url',12,'','','Restore Your GUI Settings')

#    for file in os.listdir(USB):
#        if file.endswith("_backup.zip"):
#            addDir('1. Select the [COLOR blue]BACKUP FILE[/COLOR] you want to restore..','url',2,'','','Restore Your Entire System')

#    for file in os.listdir(USB):
#        if file.endswith("_guisettings.zip"):
#            addDir('2. Select the [COLOR blue]GUI SETTINGS ZIP FILE[/COLOR] you want to restore..','url',12,'','','Restore Your GUI Settings')

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
        tools.DELETE_PACKAGES()
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
#FUNCTION TO DELETE DOWNLOADED PACKAGES/ZIP FILES
def KODI_CLEANER():
    choice = xbmcgui.Dialog().yesno('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]', 'This will free up space by deleting the zip install files of your addons, clear your textures13.db file and remove your thumbnails folder. Thumbnails will automatically be repopulated after a restart. Do you want to continue?', nolabel='NO, CANCEL',yeslabel='YES, DELETE')
    if choice == 1:
        tools.DELETE_PACKAGES()
        cache.Remove_Textures()
        tools.DESTROY_PATH(THUMBNAILS)
        choice = xbmcgui.Dialog().yesno('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]', 'All Packages and Cache have been deleted successfully.', 'You must now restart Kodi, would you like to quit now?','', nolabel='NO, RESTART LATER',yeslabel='YES, QUIT')
        if choice == 1:
            tools.KILL_XBMC()

#---------------------------------------------------------------------------------------------------
#FUNCTION TO WIPE ENTIRE XBMC/KODI BUILD - FRESH START - EXCLUDES THE ICT WIZARD
def WIPE_XBMC():
    if skin!= "skin.confluence":
        dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Please switch to the default Confluence skin','before performing a wipe.','')
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
        return
    else:
        choice = xbmcgui.Dialog().yesno("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]", '[COLOR red]VERY IMPORTANT[/COLOR]: This will completely wipe your install.', 'Would you like to create a [COLOR lime][B]BACKUP[/B][/COLOR] before proceeding?', '', yeslabel='YES, BACKUP',nolabel='NO, CONTINUE')
        if choice == 1:
            FULL_UNIVERSAL_BACKUP()
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
 #                   print"community.builds.WIPE_XBMC All user files removed, you now have a clean install"
 #                   dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Wipe Successful, please restart Kodi for changes to take effect.','','')
 #               else:
 #                   print"community.builds.WIPE_XBMC User files partially removed"
 #                   dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Wipe Successful, please restart Kodi for changes to take effect.','','')
            except: pass
        tools.REMOVE_EMPTY_FOLDERS()
        tools.REMOVE_EMPTY_FOLDERS()
        tools.REMOVE_EMPTY_FOLDERS()
        tools.REMOVE_EMPTY_FOLDERS()
        tools.REMOVE_EMPTY_FOLDERS()
        tools.REMOVE_EMPTY_FOLDERS()
        tools.REMOVE_EMPTY_FOLDERS()
        dialog.ok('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]','Wipe Successful, please restart Kodi for changes to take effect.','','')

#---------------------------------------------------------------------------------------------------
#FUNCTION TO OPEN ADDON/WIZARD SETTINGS
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
unlocked=None

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
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)

#---------------------------------------------------------------------------------------------------
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
        print "############   RESTORE_UNIVERSAL_BACKUP  #################"
        RESTORE_UNIVERSAL_BACKUP()

elif mode==3:
        print "############   FULL_UNIVERSALL_BACKUP  #################"
        FULL_UNIVERSAL_BACKUP()

elif mode==4:
        print "############   RESTORE_BACKUP_XML #################"
        RESTORE_BACKUP_XML(name,url,description)

elif mode==5:
        print "############   RESTORE_OPTION   #################"
        RESTORE_OPTION()

elif mode==6:
        print "############   RESTORE_ZIP_FILE   #################"
        RESTORE_ZIP_FILE(url)

elif mode==7:
        print "############   UPDATE_WIZARD   #################"
        UPDATE_WIZARD(name,url,description)

elif mode==8:
        print "############   WIPE_XBMC   #################"
        WIPE_XBMC()

#elif mode==9:
        #print "############   GUI_WIZARD   #################"
        #GUI_WIZARD(name,url,description)

elif mode==10:
        print "############   OPEN_ADDON_SETTINGS   #################"
        ADDON_SETTINGS()

elif mode==11:
        print "############   KODI_CLEANER   #################"
        KODI_CLEANER()

elif mode==12:
        print "############   RESTORE_LOCAL_GUI   #################"
        RESTORE_LOCAL_GUI()

elif mode==13:
        print "############   FREE_UPDATE_WIZARD   #################"
        FREE_UPDATE_WIZARD(name,url,description)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
