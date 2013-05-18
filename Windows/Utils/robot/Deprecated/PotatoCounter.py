import urllib, urllib2, cookielib
import re

usr = 'the_tzar'
pwd = '12pimple'

if raw_input('Use default login? ') == "no":
    usr = raw_input('Username: ')
    pwd = raw_input('Password: ')

loginData = {'username': usr, 'password': pwd}

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
login_data = urllib.urlencode(loginData)
print "Logging in..."
urllib2.urlopen('http://www.neopets.com/login.phtml', login_data)

try:
    print "Opening potato counter page..."
    page = urllib2.urlopen('http://www.neopets.com/medieval/potatocounter.phtml?')
    potatoCount = len(re.findall('potato\d\.gif', page.read()))
except:
    print "Failed."


