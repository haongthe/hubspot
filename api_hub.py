from json import dumps
import json
from pymongo import MongoClient
from flask import Flask, request
from flask_restful import Resource, Api
import config
import requests
from bson import ObjectId

def init():

    global client, db, querystring, mylist, url, collection_name, res, data, hasMore, hasmore, offset, offset_cts
    client = MongoClient('localhost', 27017)
    db = client.test3

    mylist =[{'link_api' : 'https://api.hubapi.com/contacts/v1/lists/all/contacts/all', 'col' : 'get_contacts'},
            {'link_api' : 'https://api.hubapi.com/companies/v2/companies/paged', 'col' : 'get_company'},
            {'link_api' : 'https://api.hubapi.com/deals/v1/deal/paged?hapikey=demo', 'col' : 'get_deals'},
            {'link_api' : 'https://api.hubapi.com/crm-pipelines/v1/pipelines/tickets', 'col' : 'get_pipelines'},
            {'link_api' : 'https://api.hubapi.com/content/api/v2/site-maps', 'col' : 'site_maps'},
            {'link_api' : 'https://api.hubapi.com/hubdb/api/v2/tables', 'col' : 'get_table'},
            {'link_api' : 'https://api.hubapi.com/marketing-emails/v1/emails', 'col' : 'get_mar_email'},
            {'link_api' : 'https://api.hubapi.com/automation/v3/workflows', 'col' : 'get_workflows'},
            {'link_api' : 'https://api.hubapi.com/email/public/v1/subscriptions', 'col' : 'get_email_sub'},
            {'link_api' : 'https://api.hubapi.com/comments/v3/comments', 'col' : 'get_comment'},
            {'link_api' : 'https://api.hubapi.com/content/api/v2/blogs', 'col' : 'get_blogs'},
            {'link_api' : 'https://api.hubapi.com/cos-domains/v1/domains', 'col' : 'get_domains'},
            {'link_api' : 'https://api.hubapi.com/filemanager/api/v2/files', 'col' : 'get_files'},
            {'link_api' : 'https://api.hubapi.com/content/api/v2/layouts', 'col' : 'get_layouts'},
            {'link_api' : 'https://api.hubapi.com/content/api/v2/pages', 'col' : 'get_pages'},
            {'link_api' : 'https://api.hubapi.com/content/api/v2/templates', 'col' : 'get_tempates'},
            {'link_api' : 'https://api.hubapi.com/url-mappings/v3/url-mappings', 'col' : 'get_urlmappings'},
            {'link_api' : 'https://api.hubapi.com/extensions/ecomm/v2/settings', 'col' : 'get_ecommerceSettings'}]

def main():
    init()
    querystring = {"hapikey":"0525e7b4-90e9-4e7a-a04c-22ef0de711ba"}
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
                    "hapikey":"0525e7b4-90e9-4e7a-a04c-22ef0de711ba",
                    "offset" : offset
                }
                querystring_cts = {
                    "hapikey":"0525e7b4-90e9-4e7a-a04c-22ef0de711ba",
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
if __name__ == "__main__":
    main()
