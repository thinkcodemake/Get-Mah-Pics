import http.client
import json
import urllib.request
import urllib.error
import os

def getFileType(link):
    file_type = link.split('.')[-1]
    file_type = file_type[:3]
    if file_type == '.jpe':
        file_type = '.jpeg'
    return file_type

def downloadImage(link):
    try:
        urllib.request.urlretrieve(link, './pics/' + subreddit + '/' + pdata['id'] + '.' + getFileType(link))
    except urllib.error.HTTPError as err:
        print(link + ' : ' + str(err.code) + ' : ' + err.reason)
        

file_types = ['jpg','gif','png']
subreddits = ['funny','pics','AdviceAnimals']

for subreddit in subreddits:

    print('')
    print('Downloading ' + subreddit + ':')
    
    if not os.path.exists('./pics/' + subreddit):
        os.makedirs('./pics/' + subreddit)

    hdr = {'User-Agent' : 'Testing some jazz'}
    conn = http.client.HTTPConnection('www.reddit.com')
    conn.request('GET', '/r/' + subreddit + '/.json?limit=100', headers=hdr)
    response = conn.getresponse().readall().decode('utf-8')
    json_dict = json.loads(response)

    for post in json_dict['data']['children']:
        pdata = post['data']
        if pdata['is_self']:
            continue
        elif pdata['url'].split('.')[-1][:3] in file_types:
            link = pdata['url']
            downloadImage(link)
        else:
            print('Not Downloaded:' + pdata['domain'])
        '''
        elif pdata['domain'] == 'imgur.com':
            #Replace with better imgur downloading, for example .gif's are wrong
            link = pdata['url'] + '.jpg'
            print(link)
            urllib.request.urlretrieve(link, './pics/' + subreddit + '/' + pdata['id'] + '.' + getFileType(link))
        '''
conn.close()
