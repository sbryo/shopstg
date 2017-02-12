import json
from pymongo import MongoClient
import dropbox
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import subprocess
import os
import urllib
import urllib2
import requests
import sys
import threading
from multiprocessing.pool import ThreadPool
from amazonproduct import API

#################################################### IOFFER ########################################
def joo_ioffer(username,KEYWORDS):
    items_list5=[]
    C=0
    KEYWORDS=KEYWORDS.replace(' ','%20')
    url = 'http://www.ioffer.com/search/items/'+KEYWORDS
    values = {'name': 'Joo',
              'location': 'Northampton',
              'language': 'Python' }
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}

    data = urllib.urlencode(values)
    req = urllib2.Request(url,data,headers)
    print req
    response = urllib2.urlopen(req)
    print response
    the_page = response.read()
    print the_page
    products_list = the_page.split("<a class='item-wrapper'")
    ioffer_list = []
    for product in products_list:
        print product
        if C==8:
            break
        if product == products_list[0]:
            continue
        try:
            after_split = product.split('href=')[1]
            link = after_split.split(' ')[0]
            item_url = (link[1:-1]).split("'")[0]
            response = requests.get(item_url)
            html_product_page = response.content
            title = str(html_product_page.split('<title>')[1].split('</title>')[0].strip())
            price = str(html_product_page.split('data-original-price="')[1].split('"')[0]).replace('$','')
            img = (html_product_page.split('class="thumbnail" src="')[1]).split('"')[0]
            x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"10","web":"iOffer"}'
            print x
        except:
            continue

joo_ioffer("shaked","diesel watch")

