#main.py
import uvicorn
import json
from mysqlCnx import MysqlCnx
from typing import Optional
from fastapi import FastAPI,Request
from pydantic import BaseModel;
from fastapi.responses import RedirectResponse,HTMLResponse
import locale
locale.setlocale(locale.LC_ALL, '')

app = FastAPI()

with open('/var/www/html/Database/.config.json') as f:
    config = json.loads(f.read())


cnx = MysqlCnx(**config)
@app.get("/movies")
async def root(skip: int = 0, limit: int = 100):
    sql = "SELECT `Title` FROM `Movies`"
    result = cnx.query(sql)
    todisplay = result['data']
    return todisplay[skip : skip + limit]

@app.get("/movies/{title}")
async def root(title:str):
    formatedtitle = title.lower() + '%'
    sql2 =f'SELECT Count(Title) AS count FROM `Movies`WHERE `Title` LIKE  "{formatedtitle}" '
    result2 = cnx.query(sql2)
    value = result2['data'][0]['count']
    counted ='{:,}'.format(value)
    if(value !=0):
        sql = f'SELECT * FROM `Movies` WHERE `Title` LIKE  "{formatedtitle}" '
        result = cnx.query(sql)
        resultcount ="total number of movies with title like  " +str(title) +" is " + "= "+str(counted)
        todisplay = { 
            "note":resultcount,
            "movies":result['data']}
        return todisplay
    else:
        note =f"No movie with this {title} title"
        return note

@app.get("/movies/year/{yr}")
async def movieyear(yr:int):
    sql =f"SELECT Count(Title) AS count FROM `Movies` WHERE `Year` = {yr}"
    resultcount = cnx.query(sql)
    value = resultcount['data'][0]['count']
    counted ='{:,}'.format(value)
    answer ="total number of movies in year " +str(yr) +" = "+ str(counted)
    response ={}
    if(value !=0):
        sql2 = f"SELECT `Title`,`Year` FROM `Movies` WHERE `Year` ={yr} LIMIT 100"
        result = cnx.query(sql2)
        response = {
            "note": answer,
            "Titles":result['data']
        }
        return response
    else:
        note =f"No movie Made in {yr}"
        return note
@app.get("/movies/run/{time}")
async def run(time:int, end:Optional[int] = None):
    if end:
        sqlcount =f'SELECT Count(Title) AS count FROM `Movies` WHERE `runtimeMinutes` > {time} AND `runtimeMinutes` < {end}'
        result2 = cnx.query(sqlcount)
        value = result2['data'][0]['count']
        if(value!=0):
            sql =f'SELECT `Title`,`runtimeMinutes` FROM `Movies` WHERE `runtimeMinutes` > {time} AND `runtimeMinutes` < {end} ORDER BY `Movies`.`runtimeMinutes` ASC LIMIT 100'
            result = cnx.query(sql)
            resultcount ="total number of movies with runtime greater than " +str(time) + "And less than "+str(end)
            response ={
                "note":resultcount,
                "Titles":result['data']
            }
            return response
        else:
            note = f"no movies between {start} and {end} time"
            return note

    else:
        sqlcount =f'SELECT Count(Title) AS count FROM `Movies` WHERE `runtimeMinutes` > {time}'
        result2 = cnx.query(sqlcount)
        value = result2['data'][0]['count']
        if(value !=0):
            sql =f'SELECT `Title`,`runtimeMinutes` FROM `Movies` WHERE `runtimeMinutes` > {time}  ORDER BY `Movies`.`runtimeMinutes` ASC LIMIT 100'
            result = cnx.query(sql)
            resultcount ="total number of movies with runtime greater than " +str(time)
            response ={
                "note":resultcount,
                "Titles":result['data']
            }
            return response
        else:
            note = f"no movie runtime  {time}"
            return note
@app.get("/movies/actor/{actorid}")
async def actor(actorid:str):
    sql =f'SELECT Movies.Title,Movies.runtimeMinutes,Movies.Year ,Actors.firstname,Actors.Lastname FROM Movies JOIN knownForTitles On knownForTitles.mid = Movies.mID JOIN Actors ON Actors.pid = knownForTitles.pid WHERE knownForTitles.pid ="{actorid}"' 
    result = cnx.query(sql)
    if(len(result['data']) != 0):
        actor ={"name" :""}
        name =""
        finalresult =[]
        finalresult.append(actor)
        for value in result['data'] :
            response ={}
            name = value['firstname'] + " " + value ['Lastname']
            value.pop("firstname")
            value.pop("Lastname") 
            finalresult.append(value)
        actor['name']=name
        return finalresult
    else:
        note = f"no Actor with  id {actorid}"
        return note
    
   
@app.get("/movies/genre/{genre}")
async def genres(genre:str):
    sqlp = f'SELECT * FROM `Genre` WHERE `genre` LIKE "{genre}"'
    result = cnx.query(sqlp)
    response ={}
    if(len(result['data']) ==0):
        sqlc ='SELECT `genre`FROM `Genre`'
        res = cnx.query(sqlc)
        note ="All posssible genre are "
        response['note'] = note
        genres =[]
        submited ="All posssible genre are <br>"
        for g in res['data']:
            path = g
            answr = f'<a href= {g["genre"]}>{g["genre"]}</a><br>'
            submited = submited + answr
            
        response['genres'] =genres 
        return HTMLResponse(content=submited, status_code=200)
    
    else:
        sql =f'SELECT Movies.Title FROM Movies JOIN MovieGenres ON Movies.mID = MovieGenres.mid JOIN Genre ON Genre.gid = MovieGenres.genre WHERE Genre.genre LIKE "{genre}" LIMIT 100'   
        result = cnx.query(sql)
        sql3 =f'SELECT COUNT(Movies.Title)  AS count FROM Movies JOIN MovieGenres ON Movies.mID = MovieGenres.mid JOIN Genre ON Genre.gid = MovieGenres.genre WHERE Genre.genre LIKE "{genre}"'
        resultCount = cnx.query(sql3)
        value = resultCount['data'][0]['count']
        response ={}
        titles =[]
        counted ='{:,}'.format(value)
        count = f"total number of movies in {genre} genre is  "+str(counted)
        response['count'] = count
        for value in result['data']:
            titles.append(value['Title'])
        response['titles'] =titles 
        return response

@app.get("/Actors")
async def Actors():
    sql =f'SELECT * FROM `Actors` ORDER BY `Actors`.`pid` ASC LIMIT 100'
    result =cnx.query(sql)
    sql2 = f'SELECT COUNT(`pid`) AS count FROM `Actors`'
    resultcount = cnx.query(sql2)
    value = resultcount['data'][0]['count']
    counted ='{:,}'.format(value)
    note = "total number of actors = " +str(counted)
    response ={
        "note":note,
        " actors":result['data']
    }
    return response
@app.get("/Actors/{name}")
async def Actorsname(name:str):
    newname = '%'+name +'%'
    sql2 =f'SELECT COUNT(`pid`) AS count FROM `Actors` WHERE Actors.firstname LIKE "{newname}" or Actors.Lastname LIKE "{newname}"'
    resultcount = cnx.query(sql2)
    value = resultcount['data'][0]['count']
    counted ='{:,}'.format(value)
    if(value >0):
        sql =f'SELECT * FROM `Actors` WHERE Actors.firstname LIKE "{newname}" or Actors.Lastname LIKE "{newname}"'
        result = cnx.query(sql)
        answer = result['data']
        note ="Total number of  actors with name Like " +str(name)+ "="+str(counted)
        response ={
            "count":note,
            " actors":result['data']
        }
    else:
        note =f'No Actor named "{name}"'
@app.get("/Actors/movie/{Movieid}")
async def Acted(Movieid:str):
    sql2 =f'SELECT COUNT(Actors.pid) as count FROM Actors JOIN knownForTitles ON Actors.pid = knownForTitles.pid JOIN Movies ON Movies.mID =knownForTitles.mid WHERE knownForTitles.mid ="{Movieid}"'
    resultcount = cnx.query(sql2)
    value = resultcount['data'][0]['count']
    counted ='{:,}'.format(value)
    
    if(value >0):
        sql =f'SELECT Actors.firstname,Actors.Lastname, Movies.Title FROM Actors JOIN knownForTitles ON Actors.pid = knownForTitles.pid JOIN Movies ON Movies.mID =knownForTitles.mid WHERE knownForTitles.mid ="{Movieid}"'
        result = cnx.query(sql)
        answer = result['data']
        actors =[]
        Title =""
        for movies in answer:
            Title = movies['Title'] 
            name =movies['firstname'] + " " + movies['Lastname']
            actors.append(name)
        note =f'Total number of  Actors in "{Title}"  is "{counted}"'
        response ={
            "note":note,
            " actors":actors
        }
        return response
    else:
        note ="either movie id is invalid or no actors worked on this movie"
        return note
@app.get("/Actors/genre/{genre}")
async def Actorgenre(genre:str):
    sql0 =f'SELECT * FROM `Genre` WHERE `genre` ="{genre}"'
    result = cnx.query(sql0)
    toadd = f'<a href= /genre> click for genre list</a>'
    
    if(len(result['data']) ==0):
        note =f"{genre} is not in th elist of genre.<br> " + toadd
        return HTMLResponse(content=note, status_code=200)
    else:
        sql =f'SELECT Actors.firstname,Actors.Lastname,Movies.Title,Genre.genre FROM Actors JOIN knownForTitles ON knownForTitles.pid = Actors.pid JOIN Movies ON Movies.mID = knownForTitles.mid JOIN MovieGenres ON knownForTitles.mid = MovieGenres.mid JOIN Genre ON Genre.gid = MovieGenres.genre WHERE Genre.genre Like "{genre}" LIMIT 100' 
        result = cnx.query(sql)
        sql2 =f'SELECT COUNT(Movies.Title) As count FROM Actors JOIN knownForTitles ON knownForTitles.pid = Actors.pid JOIN Movies ON Movies.mID = knownForTitles.mid JOIN MovieGenres ON knownForTitles.mid = MovieGenres.mid JOIN Genre ON Genre.gid = MovieGenres.genre WHERE Genre.genre ="{genre}"'
        resultCount = cnx.query(sql2)
        value = resultCount['data'][0]['count']
        counted ='{:,}'.format(value)
        note =f'Total number of  Actors in "{genre}"  is "{counted}"'
        response ={
            "count":note,
            " actors":result['data']
        }
        return response
@app.get("/Actors/workedwith/{Actorid}")
async def Actorgenre(Actorid:str):
    sql0 =f'SELECT `firstname` ,`Lastname`FROM `Actors` WHERE `pid` ="{Actorid}"'
    resulted = cnx.query(sql0)
    if(len(resulted['data'] )!=0):
        actorname = resulted['data'][0]['firstname'] + " " + resulted['data'][0]['Lastname'] 
        sql =f'SELECT Actors.firstname,Actors.Lastname FROM Actors WHERE Actors.pid IN (SELECT knownForTitles.pid FROM knownForTitles WHERE knownForTitles.mid IN (SELECT knownForTitles.mid FROM knownForTitles WHERE knownForTitles.pid ="{Actorid}")) AND Actors.pid <> "{Actorid}" LIMIT 100'
        result = cnx.query(sql)
        response = {
        "Actor":actorname,
        "worked with":result['data']
        }
        return response
    else:
        note = f'Actorid "{Actorid}" Does not exist'
        return note
@app.get("/Actors/profession/{profession}")
async def Actorprofession(profession:str):
    sql0 =f'SELECT `ProfessionID` FROM `Profession` WHERE `Job` LIKE "{profession}"'
    resulted = cnx.query(sql0)
    print(len(resulted['data']))
    toadd = f'<a href= /profession> click for profession list</a>'
    if(len(resulted['data']) ==0):
        note =f"{profession} is not in the list of profession.<br> " + toadd
        return HTMLResponse(content=note, status_code=200)
    else:
        sql =f'SELECT Actors.firstname,Actors.Lastname,Profession.Job FROM Actors JOIN ActorProfession ON Actors.pid =ActorProfession.Pid JOIN Profession ON Profession.ProfessionID =ActorProfession.ProfessionID WHERE Profession.Job LIKE "{profession}" LIMIT 100'
        result = cnx.query(sql)
        sql2 =f'SELECT Count(Profession.Job) AS count FROM Actors JOIN ActorProfession ON Actors.pid =ActorProfession.Pid JOIN Profession ON Profession.ProfessionID =ActorProfession.ProfessionID WHERE Profession.Job LIKE "{profession}"'
        resultCount = cnx.query(sql2)
        value = resultCount['data'][0]['count']
        counted ='{:,}'.format(value)
        note =f'Total number of  People in "{profession}"  is "{counted}"'
        People =[]
        for pep in result['data']:
            name = pep['firstname'] +" "+pep['Lastname']
            People.append(name)

        response ={
            "count":note,
            " People":People
        }
        return response      

@app.get("/profession")
async def profession():
    sql ="SELECT `Job` FROM `Profession`"
    result = cnx.query(sql)
    professions =[]
    for p in result['data']:
        professions.append(p['Job'])
    return professions 


@app.get("/genre")
async def genre():
    sql = 'SELECT `genre`FROM `Genre`'
    result = cnx.query(sql)
    genre =[]
    for g in result['data']:
        genre.append(g['genre'])
    
    return genre
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")
