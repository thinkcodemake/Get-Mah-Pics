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
nsfw_filter = True
file_types = ['jpg','gif','png']
subreddits = ['pics']

conn = http.client.HTTPConnection('www.reddit.com')
iconn = http.client.HTTPSConnection('api.imgur.com')

try:
    store_file = open('./data.txt', 'r')
except FileNotFoundError:
    new_file = open('./data.txt', 'w')
    new_file.write('{}')
    new_file.close()
    store_file = open('./data.txt', 'r')
store_json = json.load(store_file)
store_file.close()

for subreddit in subreddits:

    if subreddit not in store_json:
        store_json[subreddit] = []
    
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

        if pdata['id'] in store_json[subreddit]:
            print('Already Downloaded')
            continue
        
        link = pdata['url']
        if pdata['is_self']:
            continue
        if  pdata['over_18'] and nsfw_filter:
            print('Skipping nsfw content.')
            continue
        elif pdata['url'].split('.')[-1][:3] in file_types:
            download_image(link)
            store_json[subreddit].append(pdata['id'])
        elif pdata['domain'] == 'imgur.com':

            img_id = get_imgur_id(pdata['url'])
            
            ihdr = {'Authorization' : 'Client-ID 454fb76af7e09f2'}
            iconn.request('GET', '/3/image/' + img_id + '.json', headers=ihdr)
            try:
                iresponse = iconn.getresponse().readall().decode('utf-8')
            except Exception as err:
                print('Problem with ' + pdata['url'] + \
                      '\n' + str(err))
                continue
            ijson_dict = json.loads(iresponse)
            if ijson_dict['success']:
                download_image(ijson_dict['data']['link'])
                store_json[subreddit].append(pdata['id'])
            elif '/a/' in pdata['url']:
                iconn.request('GET', '/3/album/' + img_id + '.json', headers=ihdr)
                try:
                    iresponse = iconn.getresponse().readall().decode('utf-8')
                except Exception as err:
                    print('Problem with ' + pdata['url'] + \
                      '\n' + str(err))
                    continue
                ijson_dict = json.loads(iresponse)
                for image in ijson_dict['data']['images']:
                    download_image(image['link'])
            else:
                print('Imgur Issue: ' + pdata['url'])
        else:
            print('Not Downloaded: ' + link)
iconn.close()
conn.close()

store_file = open('./data.txt', 'w')
json.dump(store_json, store_file)
store_file.close()
