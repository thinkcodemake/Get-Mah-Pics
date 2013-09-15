import http.client
import json
import urllib.request
import urllib.error
import os

def get_file_type(link):
    file_type = link.split('.')[-1]
    file_type = file_type[:3]
    return file_type

def download_image(link, num):
    try:
        urllib.request.urlretrieve(link, './pics/' + subreddit + '/' + pdata['id'] + num + '.' + get_file_type(link))
    except urllib.error.HTTPError as err:
        print(link + ' : ' + str(err.code) + ' : ' + err.reason)

def get_imgur_id(link):
    return link.split('/')[-1]

#Settings
file_limit = 100
nsfw_filter = True
file_types = ['jpg','gif','png']
subreddits = ['pics']

#Setup connections to Reddit and Imgur
conn = http.client.HTTPConnection('www.reddit.com')
iconn = http.client.HTTPSConnection('api.imgur.com')

try:
    #Try to open the storage file of data.txt
    store_file = open('./data.txt', 'r')
except FileNotFoundError:
    #If the file isn't found, create it & write empty data
    new_file = open('./data.txt', 'w')
    new_file.write('{}')
    new_file.close()
    store_file = open('./data.txt', 'r')

#Load storage json from file, close file
store_json = json.load(store_file)
store_file.close()

#For all the Subreddits listed
for subreddit in subreddits:

    #If no records of Subreddit found in store file, add it.
    if subreddit not in store_json:
        store_json[subreddit] = []

    #Console output
    print('')
    print('Downloading ' + subreddit + ':')

    #Check for storage folder. If it doesn't exist, make it.
    if not os.path.exists('./pics/' + subreddit):
        os.makedirs('./pics/' + subreddit)

    #Connection to Reddit created
    hdr = {'User-Agent' : 'Testing some jazz'}
    conn.request('GET', '/r/' + subreddit + '/.json?limit=' + str(file_limit), headers=hdr)

    #Get json response & load to dictionary
    response = conn.getresponse().readall().decode('utf-8')
    json_dict = json.loads(response)

    #For each Reddit Post
    for post in json_dict['data']['children']:
        pdata = post['data']

        #check if file has already been downloaded
        if pdata['id'] in store_json[subreddit]:
            print('Already Downloaded')
            continue

        link = pdata['url']

        #If post is a "Self Post", skip it.
        if pdata['is_self']:
            continue

        #Check for NSFW Filtering, if nsfw_filter is True and post is listed
        #as over_18, skip it.
        if  pdata['over_18'] and nsfw_filter:
            print('Skipping nsfw content.')
            continue

        #Check to see if link is a direct link to an image listed in
        #file_types. If so, Download it.
        elif link.split('.')[-1][:3] in file_types:
            download_image(link, '')
            store_json[subreddit].append(pdata['id'])

        #Imgur specific code
        elif pdata['domain'] == 'imgur.com':

            #Get the Imgur specific ID from the link.
            img_id = get_imgur_id(pdata['url'])

            #Connecting to Imgur.
            ihdr = {'Authorization' : 'Client-ID 454fb76af7e09f2'}

            #Get json response & load into ijson_dict
            try:
                iconn.request('GET', '/3/image/' + img_id + '.json', headers=ihdr)
                iresponse = iconn.getresponse().readall().decode('utf-8')
            except Exception as err:
                print('Problem with ' + pdata['url'] + \
                      '\n' + str(err))
                iconn.close()
                iconn = http.client.HTTPSConnection('api.imgur.com')
                continue
            ijson_dict = json.loads(iresponse)

            #If a successful 'GET' from Imgur, download the link.
            if ijson_dict['success']:
                download_image(ijson_dict['data']['link'], '')
                store_json[subreddit].append(pdata['id'])

            #If not successful, check if link is an Imgur Album
            elif '/a/' in pdata['url']:

                #Get response from Imgur
                try:
                    iconn.request('GET', '/3/album/' + img_id + '.json', headers=ihdr)
                    iresponse = iconn.getresponse().readall().decode('utf-8')
                except Exception as err:
                    print('Problem with ' + pdata['url'] + \
                      '\n' + str(err))
                    continue
                ijson_dict = json.loads(iresponse)

                #Download each image.

                count = 0
                for image in ijson_dict['data']['images']:
                    download_image(image['link'], '-' + str(count))
                    count += 1

            #Imgur problems.
            else:
                print('Imgur Issue: ' + pdata['url'])

        #General problems
        else:
            print('Not Downloaded: ' + link)

#Closing the connections
iconn.close()
conn.close()

#Storing the updated list of downloaded posts.
store_file = open('./data.txt', 'w')
json.dump(store_json, store_file)
store_file.close()
