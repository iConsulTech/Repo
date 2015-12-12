import xbmc, xbmcaddon, xbmcgui, xbmcplugin,sys
import urllib
import addon

#---------------------------------------------------------------------------------------------------
params=addon.get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None
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
print str(addon.PATH)+': '+str(addon.VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)

#---------------------------------------------------------------------------------------------------
if mode==None or url==None or len(url)<1:
        addon.CATEGORIES(id)

elif mode==1:
        addon.BACKUP_OPTION()

elif mode==2:
        print "############   RESTORE_UNIVERSAL_BACKUP  #################"
        addon.RESTORE_UNIVERSAL_BACKUP()

elif mode==3:
        print "############   FULL_UNIVERSALL_BACKUP  #################"
        addon.FULL_UNIVERSAL_BACKUP()

elif mode==4:
        print "############   RESTORE_BACKUP_XML #################"
        addon.RESTORE_BACKUP_XML(name,url,description)

elif mode==5:
        print "############   RESTORE_OPTION   #################"
        addon.RESTORE_OPTION()

elif mode==6:
        print "############   RESTORE_ZIP_FILE   #################"
        addon.RESTORE_ZIP_FILE(url)

elif mode==7:
        print "############   UPDATE_WIZARD   #################"
        addon.UPDATE_WIZARD(name,url,description)

elif mode==8:
        print "############   WIPE_XBMC   #################"
        addon.WIPE_XBMC()

#elif mode==9:
        #print "############   GUI_WIZARD   #################"
        #GUI_WIZARD(name,url,description)

elif mode==10:
        print "############   OPEN_ADDON_SETTINGS   #################"
        addon.ADDON_SETTINGS()

elif mode==11:
        print "############   KODI_CLEANER   #################"
        addon.KODI_CLEANER()

elif mode==12:
        print "############   RESTORE_LOCAL_GUI   #################"
        addon.RESTORE_LOCAL_GUI()

elif mode==13:
        print "############   FREE_UPDATE_WIZARD   #################"
        addon.FREE_UPDATE_WIZARD(name,url,description)

elif mode==14:
        print "############   PREMIUM_UPDATE_WIZARD   #################"
        addon.PREMIUM_UPDATE_WIZARD(name,url,description)

xbmcplugin.endOfDirectory(int(sys.argv[1]))