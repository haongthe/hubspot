from json import dumps
import json
from pymongo import MongoClient
from flask import Flask, request
from flask_restful import Resource, Api
import config
import requests
import urllib
import urllib.request

client = MongoClient('localhost', 27017)
db = client.test2
querystring = {"hapikey":"demo"}

mylist =[{'link_api' : 'https://api.hubapi.com/contacts/v1/lists/all/contacts/all', 'col' : 'get_contacts'},
         {'link_api' : 'https://api.hubapi.com/deals/v1/deal/paged', 'col' : 'get_deals'},
        {'link_api' : 'https://api.hubapi.com/crm-pipelines/v1/pipelines/tickets', 'col' : 'get_pipelines'},
        {'link_api' : 'https://api.hubapi.com/content/api/v2/site-maps', 'col' : 'site_maps'},
        {'link_api' : 'https://api.hubapi.com/hubdb/api/v2/tables', 'col' : 'get_table'},
        {'link_api' : 'https://api.hubapi.com/marketing-emails/v1/emails', 'col' : 'get_mar_email'},
        {'link_api' : 'https://api.hubapi.com/automation/v3/workflows', 'col' : 'get_workflows'},
        #{'link_api' : 'https://api.hubapi.com/crm-objects/v1/objects/tickets/paged?hapikey=demo&properties=subject&properties=content&properties=hs_pipeline&properties=hs_pipeline_stage', 'col' : 'get_tickets', 'id_check' : 'TICKET'},
        {'link_api' : 'https://api.hubapi.com/email/public/v1/subscriptions', 'col' : 'get_email_sub'},
        {'link_api' : 'https://api.hubapi.com/comments/v3/comments', 'col' : 'get_comment'},
        {'link_api' : 'https://api.hubapi.com/engagements/v1/engagements/paged', 'col' : 'get_engagements'}]
     
for item in mylist:

    url = item['link_api']
    collection_name = item['col']

    res = requests.get(url, params = querystring)
    data = json.loads(res.text)

    hasMore = data.get('hasMore')
    hasmore = data.get('has-more')

    offset = data.get('offset')   
    offset_cts = data.get('vid-offset')
    
    db[collection_name].insert(data)
    print('dang insert ' + collection_name)

    while True:

        if str(hasMore) == 'True' or str(hasmore) == 'True': 
            querystring = {    
                "hapikey":"demo",
                "offset" : offset
            }
            querystring_cts = {
                "hapikey":"demo",
                "vidOffset" : offset_cts
            }
            if str(collection_name) == 'get_contacts':
                res = requests.get(url, params = querystring_cts)
                data = json.loads(res.text)
                hasMore = data.get('hasMore')
                hasmore = data.get('has-more')
                offset_cts = data.get('vid-offset')

                db[collection_name].insert(data) 
                print('dang insert ' + collection_name)

            else:
                res = requests.get(url, params = querystring)
                data = json.loads(res.text)
                hasMore = data.get('hasMore')
                hasmore = data.get('has-more')

                offset = data.get('offset')

                db[collection_name].insert(data) 
                print('dang insert ' + collection_name)
        else:
            break
    
    '''if id_check in res.text: 
        if collection_name not in db.collection_names():
            db[collection_name].insert(all_data)
        else:
            db[collection_name].update_one({'id_check': id_check}, {"$set":all_data})'''

