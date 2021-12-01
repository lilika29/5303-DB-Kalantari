from mysqlCnx import MysqlCnx
import json
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI

""""""
with open('.config.json') as f:
    config = json.loads(f.read())
cnx = MysqlCnx(**config)
app = FastAPI()
# LOCAL DB
basics = {
    1 : {"sql":"SELECT population FROM worldrrrrr WHERE name = 'Germany'","question":"Modify it to show the population of Germany."},
    2 : {"sql":"SELECT name, population FROM world WHERE name IN ('Brazil', 'Russia', 'India', 'China');","question":"Modify it to show the population FROM 'Brazil', 'Russia', 'India', 'China'"},
    3 : {"sql":"SELECT name, area FROM world WHERE area BETWEEN 250000 AND 300000" ,"question":"Modify it to show the name, area FROM world WHERE area BETWEEN 250000 AND 300000\n"}
    }
world = {
    1 : {"sql":"SELECT name, continent, population FROM world","question":"Modify it to show the  name, continent, population FROM world."},
    2 : {"sql":"SELECT name FROM world WHERE population = 64105700","question":"Modify it to show the population = 64105700"},
    3 : {"sql":"SELECT name, population/1000000 FROM world WHERE continent = 'South America'" ,"question":"Modify it to show thename, population/1000000 FROM world WHERE continent = 'South America"}
    }

class teacher(BaseModel):
    id:int
    name:str
    dept: Optional[int]= None
    phone:Optional[str]= None
    mobile:Optional[str]= None

## the class world is used for updating world table:
class world(BaseModel):
    
    name:str
    continent:Optional[str]= None
    area: Optional[float]= None
    population:Optional[float]= None
    gdp:Optional[float]= None
    capital:Optional[str]= None
    tld:Optional[str]= None
    flag:Optional[str]= None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/basics/")
async def read_item():
    response =[]
    for item in basics:
        sql = basics[item]['sql']
        question = basics[item]['question']
        answer = cnx.query(sql)
        result = {
            'result':answer['data'],
            'question':question,
            'sql':sql
        }
        response.append(result)
    return response
@app.get("/basics/{item}")    
async def read_item(item:int):
    sql = basics[item]['sql']
    question = basics[item]['question']
    answer = cnx.query(sql)
    result = {
        'result':answer['data'],
        'question':question,
        'sql':sql
    }

@app.get("/world/")
async def read_item():
    response =[]
    for item in world:
        sql = world[item]['sql']
        question = world[item]['question']
        answer = cnx.query(sql)
        result = {
            'result':answer['data'],
            'question':question,
            'sql':sql
        }
        response.append(result)
    return response
@app.get("/world/{item}")    
async def read_item(item:int):
    sql = world[item]['sql']
    question = world[item]['question']
    answer = cnx.query(sql)
    result = {
        'result':answer['data'],
        'question':question,
        'sql':sql
    }

## Insert a new row into the teachers table.
@app.post("/teacher")
async def postteachers(item:teacher):
    sql = f"""
    INSERT INTO teacher (id, dept,name,phone,mobile)
    VALUES ('{item.id}', '{item.dept}','{item.name}','{item.phone}', '{item.mobile}');"""
    res = cnx.query(sql)
    return res

'''
##Update the world table. so I should have a class:
@app.post("/world/")
async def create_world(world):
    world_dict = world.dict()
    if world.gdp:
        p_with_gdp = 300 + world.gdp
        word_dict.update({"p_with_gdp": p_with_gdp})
    return world_dict 

'''
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
        
    
    
    
    




    
