import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import zipfile
import ntpath

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

#-----------------------------------------------------------------------------------------------------------------
#Function to do a full wipe.
def DESTROY_PATH(path):
    #dp.create("[COLOR=dodgerblue][B]i[/COLOR][COLOR=white]ConsulTech Wizard[/B][/COLOR]","Wiping...",'', 'Please Wait')
    shutil.rmtree(path, ignore_errors=True)

#---------------------------------------------------------------------------------------------------
#ADDED MYSELF
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    link.replace('\r','').replace('\n','').replace('\t','')
