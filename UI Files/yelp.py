from os import error
import requests
import json
import sys
import boto3
from decimal import Decimal
import time
from collections import defaultdict
API_KEY = "ueSaG54dzEo5zQeM8aI2LT5C4krMvCYm5HJiNWuh13viiwEgh-Zl3qk3Te1ZOfYK6l4kWDIQzaL4O0sezTPUejlxXv_4-v0DDcguHQjazqPClbvOhTclNpJXOe6YXXYx"
cuisines = ['chinese', 'japanese', 'italian', 'korean', 'french', 'american', 'mexican', 'indian']
client = boto3.resource('dynamodb')
table = client.Table("check1")
def detail(api_key, id):
    url = 'https://api.yelp.com/v3/businesses/' + id
    headers = {'Authorization': 'Bearer %s' % api_key}
    req = requests.get(url, headers = headers)
    return req.json()
    

def request(api_key, terms, location = "NY", limit = 50):
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer %s' % api_key}
    response = []
    id_set = set()
    for term in terms:  
        offset = 0  
        for i in range(20):
            print(i)
            offset += 50
            params = {'term':term+" restaurant",'location': "NYC",'limit': limit}
            req = requests.get(url, params = params, headers = headers)
            parsed = req.json()
            try:
                print(parsed["total"])
                if "businesses" not in parsed.keys():
                    print("qwerty")
                businesses = parsed["businesses"]
                for business in businesses:
                    dct = defaultdict(dict)
                    id = business['id']
                    if id not in id_set:
                        dct['id'] = id
                        dct['name'] = business['name'] 
                        dct['category'] = term    # cuisine type
                        dct['rating'] = business['rating'] if business['rating'] != '' else 0
                        dct['review_count'] = business['review_count'] if business['review_count'] != '' else 0
                        dct['coordinates'] = business['coordinates'] if business['coordinates'] != '' else 'None'
                        dct['address'] = ", ".join(business['location']['display_address']) if business['location']['display_address'] != '' else 'None'
                        dct['phone'] = business["display_phone"] if business["display_phone"] != '' else 'None'
                        dct['zip_code'] = business['location']['zip_code'] if business['location']['zip_code'] != '' else 'None'
                        dct['coordinates']['latitude']=str(dct['coordinates']['latitude'])
                        dct['coordinates']['longitude']=str(dct['coordinates']['longitude'])
                        
                        dct['insertedAtTimestamp']['time']=time.strftime("%X")
                        dct['insertedAtTimestamp']['date']=time.strftime("%x")
                        ddb_data = json.loads(json.dumps(dct), parse_float=Decimal)
                        #print(ddb_data)
                        table.put_item(Item=ddb_data)
                        #print(1)
                        response.append(dct)
                        id_set.add(id)
            except error:
                print(error)
                continue
    
    print(len(response))
    with open('data.json', 'w') as openfile:
        json.dump(response, openfile, indent = 4)
    
def main():         
    request(API_KEY, cuisines)


if __name__ == '__main__':
    main()