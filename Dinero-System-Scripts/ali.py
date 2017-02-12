import subprocess
import os
import urllib
import urllib2
import requests
import json


def joo_ali(username,KEYWORDS):
    items_list1=[]
    APP_KEY='21503'
    KEYWORDS=KEYWORDS.replace(' ','%20')
    C=0
    ########################################################### AliExpress ###################################33
    url = 'http://gw.api.alibaba.com/openapi/param2/2/portals.open/api.listPromotionProduct/'+APP_KEY+'?fields=productTitle,salePrice,productUrl,imageUrl&keywords='+KEYWORDS
    values = {'name': 'Joo',
              'location': 'Northampton',
              'language': 'Python' }
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}

    data = urllib.urlencode(values)
    req = urllib2.Request(url,data,headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    j=json.loads(str(the_page))
    products_list=j['result']['products']
    #print products_list
    for product in products_list:
        title=product['productTitle'].split('</font>')[1].split('<font>')[0]
        item_url=product['productUrl']
        price=product['salePrice']
        img=product['imageUrl']
        shipping='-'
        x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"'+shipping+'","web":"AliExpress"}'
        j=json.loads(x)
        items_list1.append(j)


    command="db_results.results."+username+".insert_many(items_list1)"
    exec command
    return items_list1



joo_ali('shaked','diesel watch')
