import http.client
import json
import urllib.request

hdr = {'User-Agent' : 'Testing some jazz'}
conn = http.client.HTTPConnection('www.reddit.com')
conn.request('GET', '/r/funny/.json', headers=hdr)
response = conn.getresponse().readall().decode('utf-8')
json_dict = json.loads(response)

count = 0

for post in json_dict['data']['children']:
    link = post['data']['url']
    if link[-4:] == '.jpg':
        print(link)
        urllib.request.urlretrieve(link, str(count) + '.jpg')
        count += 1
conn.close()
