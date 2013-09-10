import http.client
import json
import urllib.request
import os

def getFileType(link):
    file_type = link.split('.')[-1]
    file_type = file_type[:3]
    if file_type == '.jpe':
        file_type = '.jpeg'
    return file_type

def downloadImage(link):
    print(link)
    urllib.request.urlretrieve(link, './pics/' + subreddit + '/' + pdata['id'] + '.' + getFileType(link))

file_types = ['.jpg','.gif','.png']
subreddit = 'funny'

if not os.path.exists('./pics/' + subreddit):
    os.makedirs('./pics/' + subreddit)

hdr = {'User-Agent' : 'Testing some jazz'}
conn = http.client.HTTPConnection('www.reddit.com')
conn.request('GET', '/r/' + subreddit + '/.json', headers=hdr)
response = conn.getresponse().readall().decode('utf-8')
json_dict = json.loads(response)

#print(json_dict)

for post in json_dict['data']['children']:
    pdata = post['data']
    if pdata['domain'] == 'i.imgur.com':
        downloadImage(pdata['url'])
    elif pdata['url'][-4:] in file_types:
        downloadImage(pdata['url'])
    '''
    elif pdata['domain'] == 'imgur.com':
        #Replace with better imgur downloading, for example .gif's are wrong
        link = pdata['url'] + '.jpg'
        print(link)
        urllib.request.urlretrieve(link, './pics/' + subreddit + '/' + pdata['id'] + '.' + getFileType(link))
    '''
conn.close()
