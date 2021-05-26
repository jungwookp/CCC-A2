import json
import requests
import itertools
import os
DB_ADDR =  "http://admin:admin@172.26.134.68:5984/twitter"

with open("./geo_brief.json", encoding='utf8') as fd:
    l = fd.readline()
    tweets = []
    i = 1
    while l!="]}":
        l = fd.readline()[:-2]
        tweets.append(json.loads(l))
        if len(tweets) == 20000:
            data = json.dumps({
                "docs": [{"_id": tw['id'], **tw['value']} for tw in tweets]
            })
            if (i > 170):
                res = requests.post(f"{DB_ADDR}/_bulk_docs", data=data, headers={"Content-type": "application/json"})
            tweets = []
            print(i)
            i+=1
    if tweets:
        data = json.dump({
            "docs": [{"_id": tw['id']}.update(tw['value']) for tw in tweets]
        })
        res = requests.post(f"{DB_ADDR}/_bulk_docs", data=data)
        print(i)
