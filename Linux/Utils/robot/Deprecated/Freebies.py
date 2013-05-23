import NeoLogger
import re
import urllib2

freebies = [("http://www.neopets.com/prehistoric/omelette.phtml?type=get_omelette", "Omelette", 'and manage to take a slice!!!'),
            ("http://www.neopets.com/jelly/jelly.phtml?type=get_jelly", "Jelly", 'Congratulations!'),
            ("http://www.neopets.com/magma/quarry.phtml", "Obsidian Quarry", 'has been added to your'),
            ("http://www.neopets.com/halloween/applebobbing.phtml?bobbing=1", "Apple Bobbing", 'prize\S'),
            ("http://www.neopets.com/desert/fruitmachine2.phtml", "Fruit Machine", ''),
            ("http://www.neopets.com/worlds/geraptiku/process_tomb.phtml", "Geraptiku", 'You slowly make your way through the opening and into the awaiting darkness. The door slams shut behind you. How unexpected.'),
            ("http://www.neopets.com/faerieland/springs.phtml?type=heal", "Healing Springs", ''),
            ("http://www.neopets.com/desert/shrine.phtml?type=approach", "Coltzan", ''),
            ("http://www.neopets.com/altador/council.phtml?prhv=18af1a7eb9cd3c2e3c5f42483d11def8&collect=1", "Altador", ''),
            #("http://www.neopets.com/process_bank.phtml?type=interest", "Bank", ''),
            #("http://www.neopets.com/process_market.phtml?type=withdraw&amount="+str(shopMoney), "Shop Till", r''),
            ("http://www.neopets.com/freebies/index.phtml", "Monthly Freebee", '')]

def getFreebies(usr, pwd):
    global freebies

    NeoLogger.login(usr, pwd)
    shopMoney = 0#re.findall(r'You currently have <b>(\d+) NP</b> in your till.', opener.open('http://www.neopets.com/market.phtml?type=till').read())[0]
    for url in freebies:
        try:
            page = urllib2.urlopen(url[0], None, 5)
            if(re.findall(url[2], page.read())):
                print url[1], "get!"
##            else:
##                print "Derped up during", url[1], ":"
        except urllib2.HTTPError:
            print url[1], "request failed!"

def stock():
    stock = urllib2.urlopen('http://www.neopets.com/quickstock.phtml')
    stock = re.findall('</TR>.+</TR>', stock.read())
    print stock
    #return stock
    
if __name__ == '__main__':
    NeoLogger.login()
#    getFreebies()
