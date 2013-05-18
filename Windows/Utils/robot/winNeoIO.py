class NeoClicker(l, w, pos):
    def __init__(self, l, w, pos):
        gameLen = l
        gameWidth = w
        gamePos = pos

    import urllib, urllib2, cookielib
    import re

    def login(self, usr, pwd):
        loginData = {'username': usr,
                     'password': pwd}
        login_data = urllib.urlencode(loginData)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        try:
            page = urllib2.urlopen('http://www.neopets.com/login.phtml', login_data)
            page = page.read()
            if len(re.findall('Welcome, <a href=', page)) > 0:
                print 'Logged in as: '+usr
                return opener
        except urllib2.HTTPError:
            print 'Could not log in.'
            return False
        print 'Could not login as: '+usr
        return False




    
