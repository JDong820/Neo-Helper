import requests
import re
dictURL = 'http://www.crosswordman.com/download/UK%20Advanced%20Cryptics%20Dictionary.txt'
wordList = requests.get(dictURL).text
print 'Dictionary downloaded'
wordList = re.split('-+\n', wordList)[1]
print 'Dictonary loaded'
