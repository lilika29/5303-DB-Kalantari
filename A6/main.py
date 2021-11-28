import pymongo
import pprint
import random
import json
from typing import Optional,List
from fastapi import FastAPI
from fastapi.responses import RedirectResponse,HTMLResponse
from pydantic import BaseModel,Field
import uvicorn
import shutil 
from bson.objectid import ObjectId
from geojson import Feature, Point
from turfpy.transformation import circle
from turfpy.measurement import points_within_polygon


app = FastAPI()
# connect to mongodb
with open('/var/www/html/Database/mongoconfig.json') as f:
    config = json.loads(f.read())
cnx = pymongo.MongoClient(**config)

# use businessData
db = cnx["restaurants"]
# choose collection
coll = db['restaurantlist']

class Resturant(BaseModel):
    address: dict 
    borough: str 
    cuisine: str 
    grades: list 
    name: str  
    restaurant_id: str 

def idlimit(page_size, last_id=None):
        """Function returns `page_size` number of documents after last_id
        and the new last_id.
        """
        if last_id is None:
            # When it is first page
            cursor = coll.find().limit(page_size)
        else:
            cursor = coll.find({'_id': {'$gt': last_id}}).limit(page_size)

        # Get the data      
        data = [x for x in cursor]

        if not data:
            # No documents left
            return None, None

        # Since documents are naturally ordered with _id, last document will
        # have max id.
        last_id = data[-1]['_id']

        # Return data and last_id
        return data, last_id

@app.get("/resturants")
async def findAllRestaurants():
    """
    Description: 
        Find all restaurants in collection
    Params:
        None
    Returns: 
        dict : {"result":list,"size":int}
    """
    """ terminal_size = shutil.get_terminal_size()
    maxLine = terminal_size[1]
    response_rest_list = []
    data, idlast = idlimit(maxLine)
    while(idlast!=None):
        data, idlast = idlimit(maxLine)
        for rest in data:
            response_rest_list.append(Resturant(**rest))
        print(response_rest_list) """
    response_rest_list = []
    res = list(coll.find().skip(100).limit(100))
    for rest in res:
            response_rest_list.append(Resturant(**rest))
    return {"count":len(res),"result":response_rest_list}

@app.get("/categories")
async def findAllcategories():
    res = list(coll.distinct('cuisine'))
    return {"result":res,"count":len(res)}

@app.get("/categories/{cuisine}")
async def findAllccuisine(cuisine:str):
    myquery ={'cuisine':cuisine}
    res = coll.find(myquery)
    count = res.count()
    response_rest_list = []
    toadd = f'<a href= /categories> click for cuisine list</a>'
    if(count ==0):
        note =f"{cuisine} is not in the list of genre.<br> " + toadd
        return HTMLResponse(content=note, status_code=200)
    else:
        for rest in res:
            response_rest_list.append(Resturant(**rest))
        return response_rest_list

@app.get("/zipcode",)
async def findAllZip(Zips:list):
    zipcodes =[]
    for zip in Zips:
        zipcodes.append(str(zip))
    stuff = { "address.zipcode": {"$in":zipcodes}}
    res = coll.find(stuff)
    response_rest_list = []
    for rest in res:
        response_rest_list.append(Resturant(**rest))
    return response_rest_list

@app.get("/location")
async def findAlllocation(latlong:list):
    response_rest_list = []
    res= coll.find({'address.coord':
                                    {'$near':latlong,
                                     '$minDistance':10,
                                     '$maxDistance':100
                                    }
                    })
    for rest in res:
        response_rest_list.append(Resturant(**rest))
    return response_rest_list

    """  stuff = { "address.coord": latlong}
    qu = coll.find(stuff)
    broug = qu[0]['borough']
    zip = qu[0]['address']['zipcode']
    center = Feature(geometry=Point(((latlong))))
    cc = circle(center, radius=5)
    cd = cc["geometry"]["coordinates"][0]
    stuff2 = {"$and":[{"borough":broug,"address.zipcode":zip}]}
    res= coll.find(stuff2)
    countt =0
    response_rest_list = []
    for rest in res:
        coords = rest['address']['coord']
        pointin = Feature(geometry=Point(((coords))))
        result = points_within_polygon(pointin, cc)
        if(len(result['features']) >0):
            response_rest_list.append(Resturant(**rest))
            countt+=1
    return {"count":len(response_rest_list) , "result":response_rest_list   }  """
    """ if(countt >8):
                return response_rest_list """
    
        
@app.get("/rating/{rate}")
async def findAllrating(rate:int):
    response_rest_list = []
    stuff ={"grades.score":{"$gte":rate}}
    res= coll.find(stuff)
    counted = res.count()
    for rest in res:
        response_rest_list.append(Resturant(**rest))
    return response_rest_list








""" if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info") """

