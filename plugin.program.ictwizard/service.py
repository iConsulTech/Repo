#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import subprocess
import urllib, urllib2, time
import addon, tools

__addon__        = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__      = __addon__.getAddonInfo('id')
__addonname__    = 'ICT Service'

version_url     = 'http://iconsultech.uk/tools/version.txt'
addons_path     = xbmc.translatePath(os.path.join('special://home','addons',''))
userdata_path   = xbmc.translatePath(os.path.join('special://home/userdata','addon_data'))
ictwizard_path  = xbmc.translatePath(os.path.join(addons_path,'plugin.program.ictwizard'))
version_file    = xbmc.translatePath(os.path.join(userdata_path,'plugin.program.ictwizard','version.txt'))
notifyart       = xbmc.translatePath(os.path.join(addons_path,'plugin.program.ictwizard','resources/'))

def log(txt):
    message = '[XST] %s: %s' % (__addonname__, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)


class Main:

    def __init__(self):
        log("Going to execute script...")


    def get_installed_version(self):
        currently_installed = {}
        try:
            f = open(version_file, 'r')
            current = f.read()
            log(current)

            x = current.split('=')
            if x:
                currently_installed.update({'type':x[0],'version':x[1]})
            else:
                log("Version file doesn't contain versions info! [%s]" % version_file)
        except:
            log("Version file doesn't exists. [%s]" % version_file)

        return currently_installed


    def open_url(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link


    def convert_version(self, v):
        return tuple(map(int, (v.split("."))))


    def get_released_version(self):
        relased_versions_remote = self.open_url(version_url)
        relased_versions = {}

        for v in relased_versions_remote.split('\n'):
            if v:
                x = v.split('=')
                relased_versions.update({x[0]:x[1]})

        return relased_versions


    def notify(self, title,message,times,icon):
        icon = notifyart+icon
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


    def check_update(self):

        current = self.get_installed_version()

        if not current:
            log("Currently installed version information are missing.")
            return

        release = self.get_released_version()

        if not release:
            log("New release version information are missing.")
            return

        check_version = release.get( current.get('type') )

        log("installed build: %s" % current.get('type') )
        log("installed version: %s" % current.get('version') )
        log("check version: %s" % check_version)

        if  self.convert_version(current.get('version')) < self.convert_version(check_version):
            log("New version available: %s" % check_version)
            self.notify('[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]',
                        '[COLOR white]NEW[/COLOR] [COLOR=lime]UPDATE[/COLOR] [COLOR white]AVAILABLE[/COLOR] [COLOR=dodgerblue]v'+str(check_version)+'[/COLOR]','20000','update.png')

            if current.get('type') == 'vertigo_version':
                if current.get('type') == 'stealth_version':
                    if current.get('type') == 'ruyaflix_version':

                        auto_update_enabled = (xbmcaddon.Addon(id='plugin.program.ictwizard').getSetting('auto-update') == "true" )
                        log("auto_update_enabled: %s" % auto_update_enabled)
                if auto_update_enabled == True:
                    self.run_auto_update()
                else:
                    log("Automatic update disabled!")


        else:
            log("You are on latest version: %s" % check_version)


    def run_auto_update(self):

        #delay
        time.sleep(10)
        log("Auto update started.")

        premium_params = {}
        premium_build_data = self.open_url('http://iconsultech.uk/tools/wizard/wizard-sub.txt')
        for v in premium_build_data.split('\n'):
            if v:
                x = v.split('=')
                premium_params.update({x[0]:str(x[1]).replace('"','')})

        name = None
        url  = None
        description = None

        try:
            url=urllib.unquote_plus(premium_params["url"])
            log("Update url: %s" % url)
        except:
            log("Update 'url' are missing!")
            pass

        try:
            name=urllib.unquote_plus(premium_params["name"])
            log("Update name: %s" % name)
        except:
            log("Update 'name' are missing!")
            pass

        try:
            description=urllib.unquote_plus(premium_params["description"])
            log("Update description: %s" % description)
        except:
            log("Update 'description' are missing!")
            pass

        try:
            addon.PREMIUM_UPDATE_WIZARD(name,url,description)
        except Exception as e:
            log("Update error: %s" % e)
            pass



if (__name__ == "__main__"):
    log('update check %s started' % __addonversion__)
    service = Main()
    service.check_update()
    del Main
    log('update check %s stopped' % __addonversion__)
