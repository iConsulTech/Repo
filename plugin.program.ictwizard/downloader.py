import xbmcgui
import urllib, urllib2

def _pbhook(percent, filesize, url, dp):
    try:
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)

    if dp.iscanceled():
        raise StopDownloading('Stopped Downloading')
        dp.close()

#
# new download def
# req: urllib2
#
def download(url, dest, dp = None, session = None):

    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("[COLOR dodgerblue][B]i[/COLOR][COLOR white]ConsulTech Wizard[/B][/COLOR]","Downloading & Copying File",' ', ' ')
    dp.update(0)

    #
    # update requests cookies
    # cookies get from ICT_LOGIN()
    # must have loggen in
    if session:
        cookies = urllib2.HTTPCookieProcessor(session.cookies)
        opener = urllib2.build_opener(cookies)
    #
    # downlad without cookies
    else:
        opener = urllib2.build_opener()

    u = opener.open(url)

    #
    # open output
    f = open(dest, 'wb')

    #
    # read meta (for filesize)
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])

    #
    # manage downloading progress
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        #
        # break when missing buffer
        if not buffer:
            break
        #
        # write file
        file_size_dl += len(buffer)
        f.write(buffer)
        #
        # progress update
        downloaded_percent = int(file_size_dl * 100. / file_size)
        _pbhook(downloaded_percent, file_size, url, dp)

    f.close()
