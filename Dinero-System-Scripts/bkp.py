#DropBox Login

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

######################### Connect Results DB ####################################
client = MongoClient('ds019254.mlab.com',19254)
client.results.authenticate('shakedinero','a57821688')
db_results = client.results

######################## Connect Search DB ################################
client2 = MongoClient('ds139425.mlab.com',39425)
client2.search.authenticate('shakedinero','a57821688')
db_search = client2.search

########################## Connect History DB ########################
client3 = MongoClient('ds019254.mlab.com',19254)
client3.history.authenticate('shakedinero','a57821688')
db_history = client3.history

############## get KEYWORDS from Search DB #################################
cursor = db_search.search.shaked.find()
for document in cursor:
    KEYWORDS=document['search']

########################################################### EBAY ########################################################
ebay_list = []
try:
    api = Connection(appid='Shaked-B-976d-45bc-a23a-71ab251884fb',config_file=None)
#response details:
    response = api.execute('findItemsAdvanced',{'keywords':KEYWORDS})

    assert(response.reply.ack == 'Success')
    assert(type(response.reply.timestamp) == datetime.datetime)
    assert(type(response.reply.searchResult.item) == list)

    item = response.reply.searchResult.item[0]
    assert(type(item.listingInfo.endTime) == datetime.datetime)
    assert(type(response.dict()) == dict)

    for ITEM in response.reply.searchResult.item:
        try:
            LIST = str(ITEM).split("'value':")
            SHIPPING_PRICE = (LIST[1].split("'"))[1]
            if SHIPPING_PRICE == '0.0':
                SHIPPING_PRICE = 'Free'

            LIST = str(ITEM).split("'title':")
            TITLE = (LIST[1].split("'"))[1]

            LIST = str(ITEM).split("'viewItemURL':")
            URL = (LIST[1].split("'"))[1]

            LIST = str(ITEM).split("'galleryURL':")
            IMG = (LIST[1].split("'"))[1]
            LIST = (str(ITEM).split("'currentPrice':"))[1].split("'value':")
            PRICE = (LIST[1].split("'"))[1]

            #if SHIPPING_PRICE == 'Free':
            #    S = 0
            #    TOTAL = float(PRICE)+float(S)
            #else:
            #    TOTAL = float(PRICE)+float(SHIPPING_PRICE)

            x='{"title":"'+TITLE+'","url":"'+URL+'","image":"'+IMG+'","price":"'+PRICE+'","shipping":"'+SHIPPING_PRICE+'","web":"Ebay"}'
            j=json.loads(x)
            ebay_list.append(j)
            #RESULTS_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')
            #HISTORY_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')

        except:
            continue


except ConnectionError as e:
    print(e)
    print(e.response.dict())

################################################ DX ######################################################
url = 'http://www.dx.com/s/'+KEYWORDS
values = {'name': 'Dinero',
          'location': 'Northampton',
          'language': 'Python' }
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

data = urllib.urlencode(values)
req = urllib2.Request(url,data,headers)
response = urllib2.urlopen(req)
the_page = response.read()
products_list = the_page.split("id='c_list'")
dx_list = []
for product in products_list:
    if product == products_list[0]:
        continue
    after_split = product.split('href=')[1]
    link = after_split.split(' ')[0]
    item_url = link[1:-1]
    try:
        response = requests.get(item_url)
        html_product_page = response.content
        title = str(html_product_page.split('<title>')[1].split('</title>')[0].strip())
        title = title.split('-')[0]
        shipping = str(html_product_page.split('<span class="f_shipping">')[1].split('</span>')[0])
        price = str(html_product_page.split('<span id="price" class="fl" itemprop="price">')[1].split('</span>')[0])
        product_photo = html_product_page.split("product_photo")[1]
        link_href = product_photo.split('href=')[1]
        img = link_href.split(" ")[0]
        img = img[1:-1]
        #RESULTS_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
        #HISTORY_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
        x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"'+shipping+'","web":"DealExtreme"}'
        j=json.loads(x)
        dx_list.append(j)
    except:
        continue

########################################################### Amazon ##############################3
url = 'http://www.amazon.com/s/field-keywords='+KEYWORDS
values = {'name': 'Dinero',
          'location': 'Northampton',
          'language': 'Python' }
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

data = urllib.urlencode(values)
data = urllib.urlencode(values)
req = urllib2.Request(url,data,headers)
response = urllib2.urlopen(req)
the_page = response.read()
#products_list=the_page.split('id="atfResults')[1]
products_list = the_page.split('result_')
amazon_list=[]
for i in products_list:
    try:
        item_url = ((i.split('normal" href="')[1]).split('"'))[0]
        title = ((i.split('title="')[1]).split('"')[0])
        if KEYWORDS in title:
            img = ((i.split('img src="')[1]).split('"')[0])
            price = ((i.split('class="a-size-base a-color-price s-price a-text-bold">')[1].split('<')[0]))
            shipping = "-"
            x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"'+shipping+'","web":"Amazon"}'
            j=json.loads(x)
            amazon_list.append(j)
        #RESULTS_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
        #HISTORY_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
    except:
        continue

########################################################### AliExpress ###################################33
url = 'http://aliexpress.com/wholesale?catId=0&initiative_id=AS_20160721045815&SearchText='+KEYWORDS
values = {'name': 'Dinero',
          'location': 'Northampton',
          'language': 'Python' }
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

data = urllib.urlencode(values)
req = urllib2.Request(url,data,headers)
response = urllib2.urlopen(req)
the_page = response.read()
products_list=the_page.split('<a class="history-item product "')
ali_results = []
ali_history = []
ali_list = []

for i in products_list:
    try:
        item_url = ((i.split('href="')[1]).split('"'))[0]
        title = ((i.split('title="')[1]).split('"'))[0]
        img = ((i.split('image-src="')[1]).split('"'))[0]
        price = (((i.split('<span class="value" itemprop="price">')[1]).split('<'))[0])[3:-1]
        shipping = "-"
        #ali_results.append(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img)
        #ali-history.append(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img)
        x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"'+shipping+'","web":"AliExpress"}'
        j=json.loads(x)
        ali_list.append(j)
    except:
        continue

############################################################ Close files & Sync #################################################################
results_array = '{"ebay":"'+str(ebay_list)+'","dx":"'+str(dx_list)+'","amazon":"'+str(amazon_list)+'","ali":"'+str(ali_list)+'"}'
print "ARRAY: "+results_array

result = db_results.results.shaked.delete_many({})
db_results.results.shaked.insert(ebay_list)
db_results.results.shaked.insert(dx_list)
db_results.results.shaked.insert(ali_list)
db_results.results.shaked.insert(amazon_list)

db_history.history.shaked.insert(ebay_list)
db_history.history.shaked.insert(dx_list)
db_history.history.shaked.insert(ali_list)
db_history.history.shaked.insert(amazon_list)
