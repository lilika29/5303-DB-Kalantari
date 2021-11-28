
import json
from mysqlCnx import MysqlCnx
from datetime import datetime



def convertTime(TC):
    result =''
    end =""
    TCarry =[]
    if('am' in TC):
        end ='am'
        TCarry = TC.split('am')
    else:
        end ='pm'
        TCarry = TC.split('pm')
    timeleft = TCarry[0]
    first2 = timeleft[:2]
    last2 = timeleft[-2:]
    result= result + first2
    result= result + ":"
    result= result + last2
    result= result + " "
    result= result + end 
    return result
def Timetwenty(converted):
    in_time = datetime.strptime(converted, "%I:%M %p")
    out_time = datetime.strftime(in_time, "%H:%M")
    return out_time

def Timetwelve(converted):
    in_time = datetime.strptime(converted, "%H:%M %p")
    out_time = datetime.strftime(in_time, "%I%M%p" )
    return out_time


    


with open('/var/www/html/Database/.config.json') as f:
    config = json.loads(f.read())

cnx = MysqlCnx(**config)
student ={
    "FirstName" =
}
""" coursedic = {
        "Col": "",
        "Crn": "",
        "Subj": "",
        "Crse": "",
        "Sect": "",
        "Title": "",
        "PrimaryInstructor": "",
        "Max": -1,
        "Curr": -1,
        "Aval": -1,
        "Days": " ",
        "Begin": " ",
        "End":" ",
        "Bldg": "EMPTY",
        "Room": " "

}
f = open('/var/www/html/Database/Assignment7/2021_summer_1_schedule.json')

data = json.load(f)
count =0
count2 =0
test =[]
for i in data:
    dic = i
    
    if("Crn" not in dic):
        test.append(i)
        count2+=1
        continue
    if(type(dic['Crn'])!= str):
        count2+=1
        continue
    if('-' in dic['Crn'] or dic['Crn'] == '' ):
        test.append(i)
        count2+=1
        continue
    else:
        
        if("Col" in dic):
            coursedic['Col'] = dic['Col']
        if("Crn" in dic):
            coursedic['Crn'] = dic['Crn']
        if("Subj" in dic):
            coursedic['Subj'] = dic['Subj']
        if("Crse" in dic):
            coursedic['Crse'] = dic['Crse']
        if("Sect" in dic):
            coursedic['Sect'] = dic['Sect']
        if("Title" in dic):
            coursedic['Title'] =  dic['Title']
        if("PrimaryInstructor" in dic):
            coursedic['PrimaryInstructor'] =  dic['PrimaryInstructor']
        if("Max" in dic):
            coursedic['Max'] = dic['Max']
        if("Curr" in dic):
            coursedic['Curr'] = dic['Curr']
        if("Aval" in dic):
            if(dic['Aval'] == " "):
                coursedic['Aval'] =-1
            else:
                coursedic['Aval'] = dic['Aval']
        if("Days" in dic):
            coursedic['Days'] = dic['Days']
        if("Begin" in dic):
            if('am' in dic['Begin'] or 'pm' in dic['Begin'] ):
                coursedic['Begin'] =  Timetwenty(convertTime(dic['Begin']))
            else:
                coursedic['Begin']=" "
        if("End" in dic):
            if('am' in dic['End'] or 'pm' in dic['End'] ):
                coursedic['End'] =  Timetwenty(convertTime(dic['End']))
            else:
                coursedic['End'] =" "
        if("Bldg" in dic):
            coursedic['Bldg'] =  dic['Bldg']
        if("Room" in dic):
            coursedic['Room'] = dic['Room']
        
        count+=1
        
        
        sql ="INSERT INTO `CourseInfo` (`Col`, `Crn`, `Subj`, `Crse`, `Sect`, `Title`, `PrimaryInstructor`, `Max`, `Curr`, `Aval`, `Days`, `Begin`, `End`, `Bldg`, `Room`, `year`, `Season`) VALUES ('{Col}', '{Crn}','{Subj}', '{Crse}','{Sect}','{Title}','{PrimaryInstructor}', '{Max}', '{Curr}', '{Aval}', '{Days}', '{Begin}', '{End}', '{Bldg}', '{Room}', '2021', 'Spring');".format(**coursedic)
        cnx.query(sql)
        
print(len(data))
print(len(test))
print(count)
print(count2)"""

   







    
   


