import http.client
import json
import urllib.request
import urllib.error
import os

def get_file_type(link):
    file_type = link.split('.')[-1]
    file_type = file_type[:3]
    return file_type

def download_image(link):
    try:
        urllib.request.urlretrieve(link, './pics/' + subreddit + '/' + pdata['id'] + '.' + get_file_type(link))
    except urllib.error.HTTPError as err:
        print(link + ' : ' + str(err.code) + ' : ' + err.reason)

def get_imgur_id(link):
    return link.split('/')[-1]

file_limit = 100
nsfw = False
file_types = ['jpg','gif','png']
subreddits = ['funny', 'pics']

conn = http.client.HTTPConnection('www.reddit.com')
iconn = http.client.HTTPSConnection('api.imgur.com')

for subreddit in subreddits:

    print('')
    print('Downloading ' + subreddit + ':')

    if not os.path.exists('./pics/' + subreddit):
        os.makedirs('./pics/' + subreddit)

    hdr = {'User-Agent' : 'Testing some jazz'}
    conn.request('GET', '/r/' + subreddit + '/.json?limit=' + str(file_limit), headers=hdr)
    response = conn.getresponse().readall().decode('utf-8')
    json_dict = json.loads(response)

    for post in json_dict['data']['children']:
        pdata = post['data']
        link = pdata['url']
        if pdata['is_self']:
            continue
        if  pdata['over_18'] == True and not nsfw:
            print('Skipping nsfw content.')
            continue
        elif pdata['url'].split('.')[-1][:3] in file_types:
            download_image(link)
        elif pdata['domain'] == 'imgur.com':

            img_id = get_imgur_id(pdata['url'])
            
            ihdr = {'Authorization' : 'Client-ID 454fb76af7e09f2'}
            iconn.request('GET', '/3/image/' + img_id + '.json', headers=ihdr)
            iresponse = iconn.getresponse().readall().decode('utf-8')
            ijson_dict = json.loads(iresponse)
            if ijson_dict['success']:
                download_image(ijson_dict['data']['link'])
            else:
                print('Imgur Issue: ' + pdata['url'])
        else:
            print('Not Downloaded: ' + link)
conn.close()
