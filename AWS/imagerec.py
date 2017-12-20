# encoding:utf-8
import base64
import urllib
import urllib2
import json


def imagerec(imagefile):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant"
    
    
    f = open(imagefile, 'rb')
    img = base64.b64encode(f.read())
    
    params = {"image":img}
    params = urllib.urlencode(params)
    
    access_token = '24.f1cab95fd4b050bccc10b881d9ca32d0.2592000.1515572403.282335-10514939'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(request)
    #return response
    content = response.read()
    if content:
        print content
    
    content = json.loads(content)
    leafname = content["result"]
    leafname = leafname[0]
    print leafname['name']
    if leafname['name'] == "油麦菜".decode("utf8") or leafname['name'] == "生菜".decode("utf8"):
        return "lettuce"
    else:
        return "unkown species"

#print  imagerec("image3.jpg")
