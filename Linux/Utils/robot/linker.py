import re
import urllib2

def allLinks(page):
    return re.match('a href=\"(.*)\" ', page)

    
def getPage(url):
    return urllib2.urlopen(url).read()

d = 'http://www.jellyneo.net/?go=festivalofneggs#plastic'
a = getPage(d)
print allLinks(a)
