#main.py
import uvicorn
import json
from mysqlCnx import MysqlCnx
from typing import Optional
from fastapi import FastAPI,Request
from pydantic import BaseModel;
from fastapi.responses import RedirectResponse,HTMLResponse

with open('/var/www/html/Database/.config.json') as f:
    config = json.loads(f.read())

cnx = MysqlCnx(**config)

class teacher(BaseModel):
    id:int
    name:str
    dept: Optional[int]= None
    phone:Optional[str]= None
    mobile:Optional[str]= None

class world(BaseModel):
    name:str
    continent:Optional[str]= None
    area: Optional[float]= None
    population:Optional[float]= None
    gdp:Optional[float]= None
    capital:Optional[str]= None
    tld:Optional[str]= None
    flag:Optional[str]= None
app = FastAPI()

@app.get("/routes")
def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list

@app.get("/",response_class=HTMLResponse)
async def root():
    test ="""
        <a href= basics>basics</a><br>
        <a href= basics/1>basics individual</a><br>
        <a href= world>world</a><br>
        <a href= world/1>world individual</a><br>
        <a href= nobel>nobel</a><br>
        <a href= nobel/1>nobel individual</a><br>
        <a href= within>within</a><br>
        <a href= within/1>within individual</a><br>
        <a href= aggregate>aggregate</a><br>
        <a href= aggregate/1>aggregate individual</a><br>
        <a href= joins>joins</a><br>
        <a href= joins/1>joins individual</a><br>
        <a href= all>all</a><br>
    """
    return test


@app.get("/basics",name ="basics") 
async def getallbasic():
    result = cnx.query(f"SELECT * FROM sqlzoo WHERE groupname ='basics'") 
    finalresult =[]
    dictoparse = result['data']
    for item in result['data']:
        sql = item['query']
        quest = item['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        finalresult.append(response)
    return finalresult

@app.get("/basics/{count}")
async def getonebasic(count:int):
    
    result = cnx.query(f"SELECT * FROM sqlzoo WHERE groupname ='basics' AND count ={count}")
    if  len(result['data']) == 0 :
        return result
    else:
        sql = result['data'][0]['query']
        quest = result['data'][0]['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        return response

@app.get("/world",name ="world")
async def getworldall():
    result = cnx.query(f"SELECT * FROM sqlzoo WHERE groupname ='world'") 
    finalresult =[]
    dictoparse = result['data']
    for item in result['data']:
        sql = item['query']
        quest = item['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        finalresult.append(response)
    return finalresult

@app.get("/world/{count}")
async def getonworld(count:int):
    result = cnx.query(f"SELECT * FROM sqlzoo WHERE groupname ='world' AND count ={count}")
    if  len(result['data']) == 0 :
        return result
    else:
        sql = result['data'][0]['query']
        quest = result['data'][0]['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        return response

@app.get("/nobel",name ="nobel")
async def getnobelall():
    result = cnx.query(f"SELECT * FROM sqlzoo WHERE groupname ='nobel'") 
    finalresult =[]
    dictoparse = result['data']
    for item in result['data']:
        sql = item['query']
        quest = item['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        finalresult.append(response)
    return finalresult

@app.get("/nobel/{count}")
async def getnobelone(count:int):
    result = cnx.query(f"SELECT * FROM sqlzoo WHERE groupname ='nobel' AND count ={count}")
    if  len(result['data']) == 0 :
        return result
    else:
        sql = result['data'][0]['query']
        quest = result['data'][0]['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        return response

@app.get("/within",name="within")
async def getwithinall():
    result = cnx.query(f"SELECT * FROM `sqlzoo` WHERE groupname LIKE 'SELECT%'") 
    finalresult =[]
    dictoparse = result['data']
    for item in result['data']:
        sql = item['query']
        quest = item['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        finalresult.append(response)
    return finalresult

@app.get("/within/{count}")
async def getwithinone(count:int):
    result = cnx.query(f"SELECT * FROM sqlzoo WHERE groupname LIKE 'SELECT%' AND count ={count}")
    if  len(result['data']) == 0 :
        return result
    else:
        sql = result['data'][0]['query']
        quest = result['data'][0]['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        return response

@app.get("/aggregate", name="aggregate")
async def getaggregateall():
    result = cnx.query(f"SELECT * FROM `sqlzoo` WHERE groupname ='SUMndCOUNT'") 
    finalresult =[]
    dictoparse = result['data']
    for item in result['data']:
        sql = item['query']
        quest = item['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        finalresult.append(response)
    return finalresult

@app.get("/aggregate/{count}")
async def getaggregateone(count:int):
    result = cnx.query(f"SELECT * FROM `sqlzoo` WHERE groupname ='SUMndCOUNT' AND count ={count}")
    if  len(result['data']) == 0 :
        return result
    else:
        sql = result['data'][0]['query']
        quest = result['data'][0]['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        return response

@app.get("/joins",name ="joins")
async def getjoinsall():
    result = cnx.query(f"SELECT * FROM `sqlzoo` WHERE groupname ='JOIN'") 
    finalresult =[]
    dictoparse = result['data']
    for item in result['data']:
        sql = item['query']
        quest = item['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        finalresult.append(response)
    return finalresult

@app.get("/joins/{count}")
async def getjoinsone(count:int):
    result = cnx.query(f"SELECT * FROM `sqlzoo` WHERE groupname ='JOIN' AND count ={count}")
    if  len(result['data']) == 0 :
        return result
    else:
        sql = result['data'][0]['query']
        quest = result['data'][0]['Question']
        answer = cnx.query(sql)
        response ={
            'result':answer['data'],
            'question':quest,
            'sql':sql
        }
        return response
        
@app.get("/all")
async def getall():
    response =[]
    basic ={
        "route":"/basics",
        "Questions":[]
    }
    world ={
        "route":"/world",
        "Questions":[]
    }
    nobel ={
        "route":"/nobel",
        "Questions":[]
    }
    within ={
        "route":"/within",
        "Questions":[]
    }
    aggregate ={
        "route":"/aggregate",
        "Questions":[]
    }
    joins ={
        "route":"/joins",
        "Questions":[]
    }
    sql =f"""
    SELECT Question, groupname FROM `sqlzoo`
    GROUP BY groupname, Question
    """
    res = cnx.query(sql)
    for item in res['data']:
        if(item['groupname'] == 'basics'):
            basic['Questions'].append(item['Question'])
        elif(item['groupname'] == 'world'):
            world['Questions'].append(item['Question'])
        elif(item['groupname'] == 'nobel'):
            nobel['Questions'].append(item['Question'])
        elif(item['groupname'] == 'SELECTwithin' or item['groupname'] == 'SELECTwithin '):
            within['Questions'].append(item['Question'])
        elif(item['groupname'] == 'SUMndCOUNT'):
            aggregate['Questions'].append(item['Question'])
        elif(item['groupname'] == 'JOIN'):
            joins['Questions'].append(item['Question'])
    
    response.append(basic)
    response.append(world) 
    response.append(nobel)   
    response.append(within) 
    response.append(aggregate) 
    response.append(joins) 
    return response

    
@app.post("/teacher")
async def postteachers(item:teacher):
    sql = f"""
    INSERT INTO teacher (id, dept,name,phone,mobile)
    VALUES ('{item.id}', '{item.dept}','{item.name}','{item.phone}', '{item.mobile}');"""
    res = cnx.query(sql)
    return res
@app.patch("/worldpatch")
async def patchworld(item:world):
    response ={}
    sql ="UPDATE `world` SET"
    if(item.continent!=None):
        response['continent'] = item.continent
    if(item.area!=None):
        response['area'] = item.area
    if(item.population!=None):
        response['population'] = item.population
    if(item.gdp!=None):
        response['gdp'] = item.gdp
    if(item.capital!=None):
        response['capital'] = item.capital
    if(item.tld!=None):
        response['tld'] = item.tld
    if(item.flag!=None):
        response['flag'] = item.flag

    sql = sql+" "
    for x,y in response.items():
        sql = sql + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"  + ","
    sql =sql[:-1]
    sql = sql + " WHERE `world`.`name` = "
    sql = sql + "'"+str(item.name)+"'"
    sql = sql + ";"
    res = cnx.query(sql)
    return res
    
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
    




    
