import http.client
import json
import urllib.request
import urllib.error
import os

def getFileType(link):
    file_type = link.split('.')[-1]
    file_type = file_type[:3]
    return file_type

def downloadImage(link):
    try:
        urllib.request.urlretrieve(link, './pics/' + subreddit + '/' + pdata['id'] + '.' + getFileType(link))
    except urllib.error.HTTPError as err:
        print(link + ' : ' + str(err.code) + ' : ' + err.reason)
        
file_limit = 100
nsfw = False
file_types = ['jpg','gif','png']
subreddits = ['funny','pics','AdviceAnimals']

conn = http.client.HTTPConnection('www.reddit.com')

for subreddit in subreddits:

    print('')
    print('Downloading ' + subreddit + ':')

    if not os.path.exists('./pics/' + subreddit):
        os.makedirs('./pics/' + subreddit)

    hdr = {'User-Agent' : 'Testing some jazz'}
    conn.request('GET', '/r/' + subreddit + '/.json?limit=' + str(file_limit), headers=hdr)
    response = conn.getresponse().readall().decode('utf-8')
    json_dict = json.loads(response)

    print(json_dict)

    for post in json_dict['data']['children']:
        pdata = post['data']
        link = pdata['url']
        if pdata['is_self'] or pdata['over_18'] != nsfw:
            continue
        elif pdata['url'].split('.')[-1][:3] in file_types:
            downloadImage(link)
        else:
            print('Not Downloaded: ' + link)
conn.close()
