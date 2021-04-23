import requests

import json

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


#request = requests.get('http://api.open-notify.org')
#print(request.text)
#
#print(request.status_code)
#
#request2 = requests.get('http://api.open-notify.org/fake-endpoint')
#print(request2.status_code)
#
#people = requests.get('http://api.open-notify.org/astros.json')
#print(people.text)
#
#people_json  = people.json()
#print(people_json)
#
#print("Number of people in space:",people_json['number'])
##To print the names of people in space using a for loop
#for p in people_json['people']:
#    print(p['name'])
#
#jprint(people.json())

API_ENDPOINT = "http://pastebin.com/api/api_post.php"
  
# your API key here
API_KEY = "HoViT_DIFb2DfT1KSQAY27uw0LIGYLs0"
  
# your source code here
source_code = '''
print("Hello, world!")
a = 1
b = 2
print(a + b)
'''
  
# data to be sent to api
data = {'api_dev_key':API_KEY,
        'api_option':'paste',
        'api_paste_code':source_code,
        'api_paste_format':'python'}
  
# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, data = data)
  
# extracting response text
pastebin_url = r.text
print("The pastebin URL is:%s"%pastebin_url)

r = requests.post('https://httpbin.org / post', data ={'key':'value'})
  
# check status code for response recieved
# success code - 200
print(r)
  
# print content of request
print(r.json())
