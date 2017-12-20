import flask
from flask import Flask
from flask import jsonify
from flask import request,Response
from flask import send_from_directory
from flask_pymongo import PyMongo
import json
import time
import math
import numpy as np
import skimage
from bson import json_util
from skimage import transform
from scipy import misc
import leafseg
import imagerec

app = Flask(__name__)
mongo= PyMongo(app)



app.config['MONGO_DBNAME']= 'efarm2'


@app.route('/getdata',methods = ['GET'])
def show_data():
    #data =  request.get_json()
    #print request.values #json.loads(data)#request.get_json() 
    #data = json
    #print data
    coor_coll = mongo.db.efarm2
    data = dict()
    dataid= 1

    datal = []
    datah1 = []
    datah2 = []
    datat  = []

    for i in range(10):
        _data = coor_coll.find_one({'id': dataid})
        #datal.append(i)
        #datah1.append(i)
        #datah2.append(i)
        #datat.append(i)
        datal.append(_data['i'])
        datah1.append(_data['h1'])
        datah2.append(_data['h2'])
        datat.append(_data['t'])
        print datal
        print datah1
        print datah2
        print datat
        ataid = dataid + 1
        
    #for debug
    data = list(range(10))
    #data['l'] = [1.1,1.2,1.3,1.4,1.5]
    

    ret = json_util.dumps({'l':datal,'h1':datah1,'h2':datah2,'t':datat },default = json_util.default)
    
 
    print ret
    
    return Response(response = ret,
                    status   = 200,
                    headers  = None,
                    content_type = 'application/json',
                    direct_passthrough = False
                   )

@app.route('/val',methods=['POST'])
def receive_val():
    coor_coll = mongo.db.efarm2
    data =  request.get_data()
    print data
    data = json.loads(data)
    print data

    print "id:"
    dataid =  data['id']
    print dataid


    print 'temperature:'
    temp =  data["t"]
    print temp

    print "humidity1:"
    h1 =  data["h1"]
    print h1   

    print "humidity2:"
    h2 =  data["h2"]
    print h2

    print "intensity:"
    iten =  data["i"]    
    print iten

    #test 2:
    #insert db:
    
    coor_coll.insert( {'id':dataid,'t':temp,'h1':h1,'h2':h2,'i':iten} )

    return jsonify({'windranger':'u r a elegent lady, i love u~'})

#@app.route('/data',methods=['GET'])
#def get_data():
#    coor_coll = mongo.db.efarm
#    _data = coor_coll.find_one({'id': 1})
#    print _data['id']
#    
#    print _data['t']
#    
#    print _data['h1']
#
#    print _data['h2']
#    return jsonify({'windranger':'u r a elegent lady, i love u~'})



@app.route('/imageshow',methods=['GET'])
def show_im():
    return flask.render_template('./hahaha.html')



@app.route('/imagedrec',methods=['GET'])
def rec_img():
    global imageid    
    
    #read image
    imagename =  "imagebase/image{:d}.jpg".format(imageid)
    im = misc.imread(imagename)
    


    imsize = im.shape
    resizefactor = 5
    imsize = (np.floor(imsize[0]/resizefactor),\
              np.floor(imsize[1]/resizefactor),\
              3)
    
    imrec = transform.resize(im,imsize)
    misc.imsave("imagerec.jpg",imrec)
    species = imagerec.imagerec("imagerec.jpg")
    print species


    

    ret = dict()
    ret['s'] = species

    ret = json_util.dumps(ret)
    return Response(response = ret,
                    status   = 200,
                    headers  = None,
                    content_type = 'application/json',
                    direct_passthrough = False
                   )

imageid = 1
@app.route('/imagedisease',methods=['GET'])
def analyze_img():
    global imageid
    print 'id',imageid
    #imageid += 1
    #read image
    print imageid
    imagename =  "imagebase/image{:d}.jpg".format(imageid)
    im = misc.imread(imagename)
    print im.shape 


    #imsize = im.shape
    #resizefactor = 5
    #imsize = (np.floor(imsize[0]/resizefactor),\
    #          np.floor(imsize[1]/resizefactor),\
    #          3)
    #
    #imrec = transform.resize(im,imsize)
    #misc.imsave("imagerec.jpg",imrec)
    #species = imagerec.imagerec("imagerec.jpg")
    #print species


    imleaf = leafseg.captureleaf(im,0)
    holenums = leafseg.countholes(imleaf)
    sptnum   = leafseg.countspt(imleaf)
    
    print sptnum
    print holenums

    ret = dict()
    #ret['s'] = species
    ret['d'] = 0
    print ret
    #do threshold judgment:
   
    if sptnum > 4:
        ret['d'] =  2
    if holenums > 3:
        ret['d'] =  1
    
    ret = json_util.dumps(ret)
    del im
    del imleaf

    im = misc.imread(imagename)
    imleaf = leafseg.captureleaf(im,1)
    print imleaf.shape
    imsize = imleaf.shape
    print imsize
    resizefactor = 2
    imsize = (np.floor(imsize[0]/resizefactor),\
              np.floor(imsize[1]/resizefactor),\
              3)
    
    imleaf = transform.resize(imleaf,imsize)

    #writeimage
    misc.imsave("./static/imageres.jpg",imleaf)
         
    return Response(response = ret,
                    status   = 200,
                    headers  = None,
                    content_type = 'application/json',
                    direct_passthrough = False
                   )
    

@app.route('/img/<string:fname>',methods=['GET','POST'])
def get_img(fname):
    print "in fnction"
    global imageid
    imageid = int(fname)
    imagename =  "imagebase/image{:s}.jpg".format(fname)
    print imagename
    acc_data = request.get_data()
    filegotten = request.files['file1']   
    
    print type(filegotten)
    filegotten.save(imagename)
  
    return jsonify({'windranger':'u r a elegent lady, i love u~'})





#send values to phone

