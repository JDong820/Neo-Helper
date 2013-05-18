import NeoLogger
import urllib2

opener = NeoLogger.login('jdong42', 'qwerty123')
urllib2.install_opener(opener)

gameURL = 'http://www.neopets.com/games/hidenseek/1.phtml?xfn='
print urllib2.urlopen(gameURL).read()

a = 'http://www.neopets.com/games/process_hideandseek.phtml?p=4&game=1'
print urllib2.urlopen(a).read()
##
##for n in range(1, 3):#11):
##    a = urllib2.urlopen('http://www.neopets.com/games/process_hideandseek.phtml?p='+str(n)+'&game=1')
##    print a.read()
