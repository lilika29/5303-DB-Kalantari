#main.py
import uvicorn
import json
from mysqlCnx import MysqlCnx
from typing import Optional
from fastapi import FastAPI,Request
from pydantic import BaseModel;
from fastapi.responses import RedirectResponse,HTMLResponse
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#helper function
# 24 -12
def Timetwelve(converted):
    in_time = datetime.strptime(converted, "%H:%M:%S")
    out_time = datetime.strftime(in_time, "%I:%M:%p" )
    return out_time
#12-24
def Timetwenty(converted):
    in_time = datetime.strptime(converted, "%I:%M%p")
    out_time = datetime.strftime(in_time, "%H:%M")
    return out_time

def justUpfate(converted):
    in_time = datetime.strptime(converted, "%H:%M:%S")
    out_time = datetime.strftime(in_time, "%H:%M")
    return out_time
def update(converted):
    in_time = datetime.strptime(converted, "%H:%M")
    out_time = datetime.strftime(in_time, "%H:%M")
    return out_time

def formatResult(res):
    result = res['data']
    if(len(result) ==0):
        return 'invalid subject'
    else:
        response =[]
        for courses in result:
            if('Begin' in courses):
                courses['Begin'] = Timetwelve(str(courses['Begin']))
            if('End' in courses):
                courses['End'] = Timetwelve(str(courses['End']))
            response.append(courses)
        return response



class Time(BaseModel):
    Begin:str
    End: Optional[str] = None

""" select """
class filter(BaseModel):
        Col:  Optional[str] = None
        Crn: Optional[str] = None
        Subj: Optional[str] = None
        Crse: Optional[str] = None
        Sect:  Optional[str] = None
        Title: Optional[str] = None
        PrimaryInstructor:  Optional[str] = None
        Max: Optional[int] = None
        Curr: Optional[int] = None
        Aval:  Optional[int] = None
        Days:  Optional[str] = None
        Begin: Optional[str] = None
        End: Optional[str] = None
        Bldg:  Optional[str] = None
        Room: Optional[str] = None
        year: Optional[str] = None
        Season:Optional[str] = None
        Display:Optional[int] = 25
        Offset:Optional[int] = 0
""" insert """
class Addcourse(BaseModel):
    Col:  str
    Crn: str
    Subj: str 
    Crse: str 
    Sect:  str
    Title: str
    PrimaryInstructor:  str
    Max: Optional[int] = -1
    Curr: Optional[int] = -1
    Aval:  Optional[int] = -1
    Days:  Optional[str] = None
    Begin: Optional[str] = None
    End: Optional[str] = None
    Bldg:  Optional[str] = None
    Room: Optional[str] = None
    year:int
    Season:str
""" update """ 
class patchcourse(BaseModel):
    Col:  Optional[str] = None
    Crn: str
    Subj: Optional[str] = None 
    Crse: Optional[str] = None
    Sect:  Optional[str] = None
    Title: Optional[str] = None
    PrimaryInstructor:  Optional[str] = None
    Max: Optional[int] = -1
    Curr: Optional[int] = -1
    Aval:  Optional[int] = -1
    Days:  Optional[str] = None
    Begin: Optional[str] = None
    End: Optional[str] = None
    Bldg:  Optional[str] = None
    Room: Optional[str] = None
    year:Optional[str] = None
    Season:Optional[str] = None
""" select/insert """
class Addstudent(BaseModel):
    FirstName:str
    LastName:str
    Mnumber:str
    Classification: Optional[str] = None
    Email: Optional[str] = None
    Gpa:Optional[float] = -1
    GithubUname:Optional[str] = None
""" update """   
class patchstudent(BaseModel):
    FirstName:Optional[str] = None
    LastName:Optional[str] = None
    Mnumber:str
    Classification: Optional[str] = None
    Email: Optional[str] = None
    Gpa:Optional[float] = -1
    GithubUname:Optional[str] = None
""" insert """
class AddAdvisingF(BaseModel):
    StudentID:str
    Semester:str
    Year:str
    ListofCourses:str
    DateCreated:str
    FirstName: str
    LastName: str
    Classification: Optional[str] = None
    Major: Optional[str] = None
""" update """    
class PatchAdvising(BaseModel):
    StudentID:str
    Semester:Optional[str]  = None
    Year:Optional[str] =None
    ListofCourses:Optional[str] = None
    DateCreated:Optional[str] = None
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    Classification: Optional[str] = None
    Major: Optional[str] = None
""" select """
class AdvisingForms(BaseModel):
    StudentID:Optional[str] = None
    Semester:Optional[str] = None
    Year:Optional[str] = None
    Classification: Optional[str] = None
    Major: Optional[str] = None
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    Display:Optional[int] = 25
    Offset:Optional[int]= 0
    DateCreated:Optional[str] = None
    ListofCourses:Optional[str] = None
""" select/insert """
class filterStudent(BaseModel):
    FirstName:Optional[str] = None
    LastName:Optional[str] = None
    Mnumber:Optional[str] = None
    Classification: Optional[str] = None
    Gpa:Optional[float] = -1
    Display:Optional[int] = 25
    Offset:Optional[int]= 0
    GPAL:Optional[int] = 0
""" Api """



with open('/var/www/html/Database/.config.json') as f:
    config = json.loads(f.read())

cnx = MysqlCnx(**config)

@app.get("/courses")
async def Allcourses():
    sql ='SELECT * FROM `CourseInfo`'
    res = cnx.query(sql)
    return formatResult(res)

@app.get("/courses/Crn/{Crn}")
async def CRN(Crn:str):
    sql = f'SELECT * FROM `CourseInfo` WHERE `Crn` ="{Crn}"'
    res = cnx.query(sql)
    result = res['data']
    """ result[0]['Begin'] =Timetwelve(str(result[0]['Begin']))
    result[0]['End']=Timetwelve(str(result[0]['End'])) """
    if(len(result) ==0):
        return 'invalid CRN'
    else:
        result[0]['Begin'] =justUpfate(str(result[0]['Begin']))
        result[0]['End']=justUpfate(str(result[0]['End']))
        return result
    
@app.get("/courses/Subj/{Subj}")
async def Subj(Subj :str):
    sql = f'SELECT * FROM `CourseInfo` WHERE `Subj` ="{Subj}" ORDER BY `CourseInfo`.`year` DESC'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'invalid subject'
    else:
        return formatResult(res)
@app.get("/courses/Crse/{Crse}")
async def Crse(Crse  :str):
    sql = f'SELECT * FROM `CourseInfo` WHERE `Crse` ="{Crse}" ORDER BY `CourseInfo`.`year` DESC'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'invalid course number'
    else:
        return formatResult(res)
@app.get("/courses/Instructor/{name}")
async def Instructor(name :str):
    newname = name.lower() +'%'
    sql = f'SELECT * FROM `CourseInfo` WHERE `PrimaryInstructor` LIKE "{newname}" ORDER BY `CourseInfo`.`year` DESC'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'invalid name'
    else:
        return formatResult(res)
@app.get("/courses/building/{Bldg}")
async def building(Bldg :str):
    sql = f'SELECT * FROM `CourseInfo` WHERE `Bldg`= "{Bldg}" ORDER BY `CourseInfo`.`year` DESC'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'invalid building'
    else:
        return formatResult(res)


@app.get("/courses/Time/{Tyme}")
async def ClassTyme(Tyme:str):
    SplytTyme = Tyme.split(',')
    Begin = SplytTyme[0]
    if(len(SplytTyme) >1):
        End = SplytTyme[1]
    else:
        End =" "
    Begin = Timetwenty(str(Begin))
    if(End != " "):
        End = Timetwenty(str(End))
        sql =f'SELECT * FROM `CourseInfo` WHERE `Begin` >= "{Begin}" And `End` <= "{End}" ORDER BY `CourseInfo`.`year` DESC'
        res = cnx.query(sql)
        result = res['data']
        if(len(result) ==0):
            return 'invalid Time'
        else:
            return formatResult(res)
@app.get("/courses/closed/")
async def Classclosed(): 
    sql =f'SELECT * FROM `CourseInfo` WHERE `Aval` = 0 ORDER BY `CourseInfo`.`year` DESC' 
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'no available class'
    else:
        return formatResult(res)  

@app.get("/courses/Title/{title}")
async def Instructor(title :str):
    newtitle = '%' + title.lower() +'%'
    sql = f'SELECT * FROM `CourseInfo` WHERE `Title` LIKE "{newtitle}" ORDER BY `CourseInfo`.`year` DESC'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'invalid Title'
    else:
        return formatResult(res)

@app.get("/courses/buildingndroom/{buldroom}")
async def ClassTyme(buldroom:str):
    SplytTyme = buldroom.split(',')
    Bldg = SplytTyme[0]
    if(len(SplytTyme) >1):
        Room = SplytTyme[1]
        newRoom = '%' + Room +'%'
    else:
        Room =" "
    if(Room != " "):
        sql =f'SELECT * FROM `CourseInfo` WHERE `Bldg` = "{Bldg}" And `Room` LIKE "{newRoom}" ORDER BY `CourseInfo`.`year` DESC'
        res = cnx.query(sql)
        result = res['data']
        if(len(result) ==0):
            return 'invalid room or building'
        else:
            return formatResult(res)

@app.post("/Annony")
async def filterall(sqlList:filter):
    Limits = sqlList.Display
    offsets = sqlList.Offset
    sql ="SELECT * FROM `CourseInfo` WHERE" 
    response ={}
    if(sqlList.Col!=None):
        response['Col'] = sqlList.Col
    if(sqlList.Crn!=None):
        response['Crn'] = sqlList.Crn
    if(sqlList.Subj!=None):
        response['Subj'] = sqlList.Subj
    if(sqlList.Crse!=None):
        response['Crse'] = sqlList.Crse
    if(sqlList.Sect!=None):
        response['Sect'] = sqlList.Sect
    if(sqlList.Title!=None):
        response['Title'] = sqlList.Title
    if(sqlList.PrimaryInstructor!=None):
        response['PrimaryInstructor'] = sqlList.PrimaryInstructor
    if(sqlList.Max!=None):
        response['Max'] = sqlList.Max
    if(sqlList.Curr!=None):
        response['Curr'] = sqlList.Curr
    if(sqlList.Aval!=None):
        response['Aval'] = sqlList.Aval
    if(sqlList.Days!=None):
        response['Days'] = sqlList.Days
    if(sqlList.Begin!=None):
        response['Begin'] = sqlList.Begin
    if(sqlList.End!=None):
        response['End'] = sqlList.End
    if(sqlList.Bldg!=None):
        response['Bldg'] = sqlList.Bldg
    if(sqlList.Room!=None):
        response['Room'] = sqlList.Room
    if(sqlList.year!=None):
        response['year'] = sqlList.year
    if(sqlList.Season!=None):
        response['Season'] = sqlList.Season
    sql = sql+" "
    if(len(response)>1):
        for x,y in response.items():
            if(x == "PrimaryInstructor" or x =='Title' ):
                PIT = '%' + str(y) +'%'
                sql = sql + " " + '`' + x +'`'  + " " + "LIKE"+ " "+ "'" +PIT +"'"
            elif(x =="Aval"):
                if(y == 1):  
                    sql = sql + " " + '`' + x +'`'  + " " + ">="+ " "+ "'" +str(y) +"'"
                else:
                    sql = sql + " " + '`' + x +'`'  + " " + "<="+ " "+ "'" +str(0) +"'"
            elif(x =="Days"):
                if(y =='SU'):
                    firstchar = y+'%'
                else:
                    firstchar = '%'+y[0]+'%'
                sql = sql + " " + '`' + x +'`'  + " " + "LIKE"+ " "+ "'" +firstchar+"'"
                
            else:
                sql = sql + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"  
            del response[x]
            break
        for x,y in response.items():
            addand = 'AND'
            if(x == "PrimaryInstructor" or x =="Title"):
                PIT = '%' + str(y) +'%'
                sql = sql+addand + " " + '`' + x +'`'  + " " + "LIKE"+ " "+ "'" +PIT +"'"
            elif(x =="Aval"):
                if(y == 1):  
                    sql = sql+ addand +  " " + '`' + x +'`'  + " " + ">="+ " "+ "'" +str(y) +"'"
                else:
                    sql = sql + addand +  " " + '`' + x +'`'  + " " + "<="+ " "+ "'" +str(0) +"'"
            elif(x =="Days"):
                if(y =='SU'):
                    firstchar = y+'%'
                else:
                    firstchar = '%'+y[0]+'%'
                sql = sql + addand + " " + '`' + x +'`'  + " " + "LIKE"+ " "+ "'" +firstchar+"'"

            else:
                sql = sql + addand + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"      
    else:
        for x,y in response.items():
            if(x == "PrimaryInstructor" or x =="Title"):
                PIT = '%' + str(y) +'%'
                sql = sql + " " + '`' + x +'`'  + " " + "LIKE"+ " "+ "'" +PIT +"'"
            elif(x =="Aval"):
                if(y == 1):  
                    sql = sql + " " + '`' + x +'`'  + " " + ">="+ " "+ "'" +str(y) +"'"
                else:
                    sql = sql + " " + '`' + x +'`'  + " " + "<="+ " "+ "'" +str(0) +"'"
            elif(x =="Days"):
                if(y =='SU'):
                    firstchar = y+'%'
                else:
                    firstchar = '%'+y[0]+'%'
                sql = sql + " " + '`' + x +'`'  + " " + "LIKE"+ " "+ "'" +firstchar+"'"
            else:
                sql = sql + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"  
    sql =sql + "LIMIT" + " " + str(Limits)
    sql = sql+" "
    sql = sql+ "OFFSET" + " " + str(offsets)
    sql = sql + ";" 
    print(sql)
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'no available class'
    else:
        return formatResult(res)

@app.get("/student")
async def Allstudent():
    sql ='SELECT * FROM `StudentIInfo`'
    res = cnx.query(sql)
    return formatResult(res)

@app.get("/student/Mnumber/{Mnumber}")
async def StudentMnumber (Mnumber:str):
    
    sql =f'SELECT * FROM `StudentIInfo` WHERE `Mnumber` ="{Mnumber}"'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'Invalid Mnumber'
    else:
        return formatResult(res)
@app.get("/student/Name/{Name}")
async def studentName (Name:str):
    splitname =Name.split(',')
    Fname = splitname[0]
    Lname = splitname[1]
    sql =f'SELECT * FROM `StudentIInfo` WHERE `FirstName`="{Fname}"and `LastName`="{Lname}"'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'Invalid name'
    else:
        return formatResult(res)

@app.get("/student/GPAG/{GPA}")
async def GPAG (GPA:int):
    sql =f'SELECT * FROM `StudentIInfo` WHERE `GPA` >= "{GPA}"'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'Invalid GPA'
    else:
        return formatResult(res)

@app.get("/student/GPAL/{GPA}")
async def GPAL(GPA:int):
    sql =f'SELECT * FROM `StudentIInfo` WHERE `GPA` <= "{GPA}"'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'Invalid GPA'
    else:
        return formatResult(res)

@app.get("/Advising")
async def Advising ():
    sql =f'SELECT * FROM `Advisingform`'
    res = cnx.query(sql)
    return formatResult(res)

@app.get("/Advising/student/{Mnumber}")
async def AdvisingStudentnum(Mnumber:str):
    sql =f'SELECT * FROM `Advisingform` WHERE `StudentID` ="{Mnumber}"'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'Invalid number'
    else:
        return formatResult(res)

@app.get("/Advising/Semester/{Semester}")
async def AdvisingStudentSemester (Semester:str):
    sql =f'SELECT * FROM `Advisingform` WHERE `Semester`="{Semester}"'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'Invalid Semester'
    else:
        return formatResult(res)
@app.get("/Advising/year/{year}")
async def AdvisingStudentyear (Semester:str):
    sql =f'SELECT * FROM `Advising form` WHERE `Year`="{year}"'
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'Invalid Year'
    else:
        return formatResult(res)

@app.post("/Advising/All")
async def filterAdvisform(Advisform:AdvisingForms):
    count =0
    response ={}
    Limits = Advisform.Display
    offsets = Advisform.Offset
    sql ="SELECT *  FROM `Advisingform`  WHERE"
    if(Advisform.StudentID!=None):
        response['StudentID'] = Advisform.StudentID
    if(Advisform.Semester!=None):
        response['Semester'] = Advisform.Semester
    if(Advisform.Year!=None):
        response['Year'] = Advisform.Year
    if(Advisform.Classification!=None):
        response['Classification'] = Advisform.Classification
    if(Advisform.Major!=None):
        response['Major'] = Advisform.Major
    if(Advisform.FirstName!=None):
        response['FirstName'] = Advisform.FirstName
    if(Advisform.LastName!=None):
        response['LastName'] = Advisform.LastName
    if(Advisform.DateCreated!=None):
        response['DateCreated'] = Advisform.DateCreated
    sql = sql+" "
    if(len(response)>1):
        for x,y in response.items():
            sql = sql + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"  
            del response[x]
            break
        for x,y in response.items():
            addand = 'AND'
            sql = sql + addand + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"      
    else:
        for x,y in response.items():
            sql = sql + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"  
    sql = sql+" "
    sql =sql + "LIMIT" + " " + str(Limits)
    sql = sql+" "
    sql = sql+ "OFFSET" + " " + str(offsets)
    sql = sql + ";"
    
    res = cnx.query(sql)
    result = res['data']
    
    if(len(result) ==0):
        send = 'Invalid Advising filters'
    else:
        send = formatResult(res)
    return send

@app.post("/AddStudent")
async def student(sqlList:Addstudent):
    fname = str(sqlList.FirstName)
    lname = str(sqlList.LastName)
    Mnum= str(sqlList.Mnumber)
    classfi = str(sqlList.Classification)
    Email= str(sqlList.Email)
    GPA= int(sqlList.Gpa)
    gitname= str(sqlList.GithubUname)
    sql ='INSERT INTO `StudentIInfo` (`FirstName`, `LastName`, `Mnumber`, `Classification`, `Email`, `GPA`, `GitHubUname`) VALUES ("{fnam}", "{lnam}", "{Mnu}", "{classf}", "{email}", {gpa}, "{gituname}")'.format(fnam=fname,lnam =lname ,Mnu = Mnum , classf =classfi if 'None' not in classfi else " ",email= Email if 'None' not in Email else " ",gpa= GPA,gituname = gitname if 'None' not in gitname else " ")
    res = cnx.query(sql)
    return res


@app.patch("/UpdateStudent")
async def student(sqlList:patchstudent):
    response ={}
    sql ="UPDATE `StudentIInfo` SET"
    if(sqlList.FirstName!=None):
        response['FirstName'] = sqlList.FirstName
    if(sqlList.LastName!=None):
        response['LastName'] = sqlList.LastName
    if(sqlList.Classification!=None):
        response['Classification'] = sqlList.Classification
    if(sqlList.Email!=None):
        response['Email'] = sqlList.Email
    if(sqlList.Gpa!=-1):
        response['Gpa'] = sqlList.Gpa
    if(sqlList.GithubUname!=None):
        response['GithubUname'] = sqlList.GithubUname
    sql = sql+" "
    for x,y in response.items():
        sql = sql + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"  + ","
    sql =sql[:-1]
    sql = sql + " WHERE `StudentIInfo`.`Mnumber` = "
    sql = sql + "'"+str(sqlList.Mnumber)+"'"
    sql = sql + ";"
    res =cnx.query(sql)
    return res


@app.patch("/UpdateAdvisingForm")
async def AdvisingformPatch(sqlList:PatchAdvising):
    response ={}
    sql ="UPDATE `Advisingform` SET"
    if(sqlList.Semester!=None):
        response['Semester'] = sqlList.Semester
    if(sqlList.Year!=0):
        response['Year'] = sqlList.Year
    if(sqlList.ListofCourses!=None):
        response['ListofCourses'] = sqlList.ListofCourses
    if(sqlList.DateCreated!=None):
        response['DateCreated'] = sqlList.DateCreated
    if(sqlList.FirstName!=None):
        response['FirstName'] = sqlList.FirstName
    if(sqlList.LastName!=None):
        response['LastName'] = sqlList.LastName
    if(sqlList.Classification!=None):
        response['Classification'] = sqlList.Classification
    if(sqlList.Major!=None):
        response['Major'] = sqlList.Major
    sql = sql+" "
    for x,y in response.items():
        sql = sql + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"  + ","
    sql =sql[:-1]
    sql = sql + " WHERE `Advisingform`.`StudentID` = "
    sql = sql + "'"+str(sqlList.StudentID)+"'"
    sql = sql + ";"
    res =cnx.query(sql)
    return res

@app.post("/AddForm")
async def student(sqlList:AddAdvisingF):
    semester = str(sqlList.Semester)
    year = int(sqlList.Year)
    Mnum= str(sqlList.StudentID)
    Courses = str(sqlList.ListofCourses)
    Created= str(sqlList.DateCreated)
    firstName = str(sqlList.FirstName)
    lastName =str(sqlList.LastName)
    classification = str(sqlList.Classification)
    major = str(sqlList.Major)
    sql ='INSERT INTO `Advisingform` (`Semester`, `Year`, `StudentID`, `ListofCourses`, `DateCreated`, `FirstName`, `LastName`, `Classification`, `Major`) VALUES ("{Semester}", "{Year}", "{StudentID}", "{ListofCourses}", "{DateCreated}","{FirstName}","{LastName}","{Classification}","{Major}")'.format(Semester=semester ,Year =year ,StudentID = Mnum , ListofCourses =Courses ,DateCreated= Created,FirstName=firstName,LastName=lastName,Classification=classification if 'None' not in classification else " ",Major=major if 'None' not in major else " " )
    res =cnx.query(sql)
    return res

@app.post("/Addcourse")
async def Addcourses(sqlList:Addcourse):
    col = str(sqlList.Col)
    crn = str(sqlList.Crn)
    subj = str(sqlList.Subj)
    crse = str(sqlList.Crse)
    sect = str(sqlList.Sect)
    title = str(sqlList.Title)
    PI = str(sqlList.PrimaryInstructor)
    maxn = int(sqlList.Max)
    curr = int(sqlList.Curr)
    aval = str(sqlList.Aval)
    begin = str(sqlList.Begin)
    end = str(sqlList.End)
    days = str(sqlList.Days)
    if 'None' not in end:
        end = end
    if 'None' not in begin:
        begin = begin
    bldg = str(sqlList.Bldg)
    room = str(sqlList.Room)
    Year = int(sqlList.year)
    season = str(sqlList.Season)
    sql ='INSERT INTO `CourseInfo`(`Col`, `Crn`, `Subj`, `Crse`, `Sect`, `Title`, `PrimaryInstructor`, `Max`, `Curr`, `Aval`, `Days`, `Begin`, `End`, `Bldg`, `Room`, `year`, `Season`) VALUES ("{Col}","{Crn}","{Subj}","{Crse}","{Sect}","{Title}","{PrimaryInstructor}","{Max}","{Curr}","{Aval}","{Days}","{Begin}","{End}","{Bldg}","{Room}","{year}","{Season}")'.format(Col=col,Crn=crn,Subj=subj,Crse=crse,Sect=sect,Title=title,PrimaryInstructor=PI,Max=maxn,Curr=curr,Aval=aval,Days=days if 'None' not in days else " ",Begin=begin if 'None' not in begin else " ",End=end if 'None' not in end else " ",Bldg = bldg if 'None' not in bldg else " ", Room=room  if 'None' not in room else " ",year=Year,Season=season)
    res =cnx.query(sql)
    return res

@app.patch("/Updatecourse")
async def AdvisingformPatch(sqlList:patchcourse):
    sql ="UPDATE `CourseInfo` SET"
    response ={}
    if(sqlList.Col!=None):
        response['Col'] = sqlList.Col
    if(sqlList.Subj!=None):
        response['Subj'] = sqlList.Subj
    if(sqlList.Crse!=None):
        response['Crse'] = sqlList.Crse
    if(sqlList.Sect!=None):
        response['Sect'] = sqlList.Sect
    if(sqlList.Title!=None):
        response['Title'] = sqlList.Title
    if(sqlList.PrimaryInstructor!=None):
        response['PrimaryInstructor'] = sqlList.PrimaryInstructor
    if(sqlList.Max!=None):
        response['Max'] = sqlList.Max
    if(sqlList.Curr!=None):
        response['Curr'] = sqlList.Curr
    if(sqlList.Aval!=None):
        response['Aval'] = sqlList.Aval
    if(sqlList.Days!=None):
        response['Days'] = sqlList.Days
    if(sqlList.Begin!=None):
        response['Begin'] = update(str(sqlList.Begin))
    if(sqlList.End!=None):
        response['End'] = update(str(sqlList.End))
    if(sqlList.Bldg!=None):
        response['Bldg'] = sqlList.Bldg
    if(sqlList.Room!=None):
        response['Room'] = sqlList.Room
    sql = sql+" "
    for x,y in response.items():
        sql = sql + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"  + ","
    sql =sql[:-1]
    sql = sql + " WHERE `CourseInfo`.`Crn` = "
    sql = sql + "'"+str(sqlList.Crn)+"'"
    sql = sql + ";"
    res = cnx.query(sql)
    return res


@app.post("/maketable",response_class=HTMLResponse)
async def MakeAdvisingform(sqlList:list):
    hours =0
    tostrig = str(sqlList)
    tostrig=tostrig.replace('[', '(')
    tostrig=tostrig.replace(']', ')')
    sql = f"SELECT `Crn`,`Subj`,`Crse`,`Sect`,`Title`,`Days`,`Begin`,`End` FROM `CourseInfo` WHERE `Crn` IN {tostrig}"
    res = cnx.query(sql)
    iterate = formatResult(res)
    col = '<td>'
    ecol ='</td>'
    test ="""<div>
<table style="border-spacing:2em;" >
  <tr>
    <th>CRN</th>
    <th>Subj</th>
    <th>Course</th>
    <th>Sect</th>
    <th>Title</th>
    <th>Day</th>
    <th>begin</th>
    <th>end</th>
  </tr>
 

    """
    if(iterate !="invalid subject"):
        for row in iterate:
            newtest ='<tr>'
            for x,y in row.items():
                if(x =='Crse'):
                    lasdigit = int(y[-1])
                    hours+=lasdigit
                newtest += col + str(y) +ecol 
            newtest +='</tr>'
            test += newtest 
        test+='</table>'
        test+='</div>'
        test+= "<div style ='text-decoration: underline'>"+'Total hours'+" " +str(hours) +'<div>'
    return test


@app.post("/filterstudent")
async def filterstudent(sqlList:filterStudent):
    Limits = sqlList.Display
    offsets = sqlList.Offset
    GPAL = sqlList.GPAL
    response ={}
    sql ="SELECT * FROM `StudentIInfo` WHERE"
    if(sqlList.FirstName!=None):
        response['FirstName'] = sqlList.FirstName
    if(sqlList.LastName!=None):
        response['LastName'] = sqlList.LastName
    if(sqlList.Classification!=None):
        response['Classification'] = sqlList.Classification
    if(sqlList.Gpa!=-1):
        response['Gpa'] = sqlList.Gpa
    if(sqlList.Mnumber!=None):
        response['Mnumber'] = sqlList.Mnumber
    sql = sql+" "
    if(len(response)>1):
        for x,y in response.items():
            if(x =="Gpa" and GPAL == 0 ):
                sql = sql + " " + '`' + x +'`'  + " " + ">="+ " "+ "'" +str(y) +"'"
            elif(x =="Gpa" and GPAL == 1) :
                sql = sql + " " + '`' + x +'`'  + " " + "<="+ " "+ "'" +str(y) +"'" 
            elif(x =="Gpa" and GPAL == 2):
                sql = sql + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"
            else:
                sql = sql + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"  
            del response[x]
            break
        for x,y in response.items():
            addand = 'AND'
            if(x =="Gpa" and GPAL == 0 ):
                sql = sql + addand + " " + '`' + x +'`'  + " " + ">="+ " "+ "'" +str(y) +"'"
            elif(x =="Gpa" and GPAL == 1) :
                sql = sql + addand + " " + '`' + x +'`'  + " " + "<="+ " "+ "'" +str(y) +"'" 
            elif(x =="Gpa" and GPAL == 2):
                sql = sql + addand + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"
            else:
                sql = sql + addand + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"      
    else:
        for x,y in response.items():
            if(x =="Gpa" and GPAL == 0 ):
                sql = sql + " " + '`' + x +'`'  + " " + ">="+ " "+ "'" +str(y) +"'"
            elif(x =="Gpa" and GPAL == 1) :
                sql = sql + " " + '`' + x +'`'  + " " + "<="+ " "+ "'" +str(y) +"'" 
            elif(x =="Gpa" and GPAL == 2):
                sql = sql + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"
            else:
                sql = sql + " " + '`' + x +'`'  + " " + "="+ " "+ "'" +str(y) +"'"  
    sql =sql + "LIMIT" + " " + str(Limits)
    sql = sql+" "
    sql = sql+ "OFFSET" + " " + str(offsets)
    sql = sql + ";"
    print(sql)
    res = cnx.query(sql)
    result = res['data']
    if(len(result) ==0):
        return 'Invalid student filters'
    else:
        return formatResult(res)
