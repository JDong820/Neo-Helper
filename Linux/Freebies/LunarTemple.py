import re
import requests
import json
import getpass

puzzleURL = 'http://www.neopets.com/shenkuu/lunar/?show=puzzle'
submitURL = 'http://www.neopets.com/shenkuu/lunar/results.phtml'

def redeem(session):
    lunarPage = session.get(puzzleURL)
    angle = int(re.findall('Kreludor=([\d\.]+)', lunarPage.content)[0])
    answer = int(round(angle/22.5)%16)
    if answer > 7:
        answer -= 8
    else:
        answer += 8
    answer = {'submitted':'true','phase_choice':answer}
    print answer
    if(re.findall('correct', session.post(submitURL, answer))):
        return True
    return False

if __name__ == '__main__':
    session = requests.session()
    login = {'username':raw_input('Username: '),'password':getpass.getpass()}
    session.post('http://www.neopets.com/login.phtml', login).content
    redeem(session)


