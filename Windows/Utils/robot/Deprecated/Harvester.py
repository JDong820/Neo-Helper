import Neo2
import Freebies, FF2, Tug2
import webbrowser
import time
import obfu

p1 = [479346, 504798, 428442, 483588, 492072, 513282, 207858, 212100, 216342]
p2 = [207858, 212100, 475104, 445410, 462378, 475104, 458136, 428442]
openSetting = 0
ffurl = 'http://www.neopets.com/games/play_flash.phtml?va=&game_id=805&nc_referer=&age=1&hiscore=300&sp=0&questionSet=&r=1879695&&width=909&height=660&quality=low'
tugurl = 'http://www.neopets.com/games/play_flash.phtml?va=&game_id=909&nc_referer=&age=1&hiscore=4200&sp=0&questionSet=&r=8436508&&width=909&height=546&quality=low'

def links():
    Freebies.getFreebies('jdong42', obfu.decrypt(p1, 4242))
    Freebies.getFreebies('the_tzar', obfu.decrypt(p2, 4242))

def games():
    webbrowser.open(ffurl, new=openSetting)
    time.sleep(10)
    FF2.play()
    webbrowser.open(tugurl, new=openSetting)
    time.sleep(10)
    Tug2.play()
 
