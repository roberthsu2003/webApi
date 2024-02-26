from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
async def read_root():
    return "學生用webApi(https://xxxxxx/docs)"

@app.get("/youbike")
async def read_youbike():
    url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    response = requests.request('GET',url)
    response.encoding = 'utf-8'
    allData = response.json()
    return allData

@app.get("/youbike/{sarea}")
async def youbike_area(sarea:str):
    url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    response = requests.request('GET',url)
    allData = response.json()
    response.encoding = 'utf-8'
    areaData = [site for site in allData if site['sarea']==sarea]
    return areaData

import sqlite3
from pydantic import BaseModel

class City(BaseModel):
    cityId:int
    cityName:str
    continent:str
    country:str
    image:str

class Root(BaseModel):
    root:list[City]

#使用pydatic
@app.get("/cities")
async def cities():
    conn = sqlite3.connect('citys.db')
    sql = "SELECT * FROM city"
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    dataList:list[City] = []
    for row in rows:
        city = City(cityId=row[0],
                    cityName=row[1],
                    continent=row[2],
                    country=row[3],
                    image=row[4])        
        dataList.append(city)
        
    #建立Root
    root = Root(root=dataList)
    cursor.close()
    conn.close()
    return root

#傳出一個城市
@app.get("/cities/{cityName}")
async def city_image(cityName:str):
    conn = sqlite3.connect('citys.db')
    cursor = conn.cursor()
    sql = "SELECT * FROM city WHERE ctiyName=?"    
    cursor.execute(sql,(cityName,))
    row = cursor.fetchone()
    city = City(cityId=row[0],
                cityName=row[1],
                continent=row[2],
                country=row[3],
                image=row[4])
    cursor.close()
    conn.close()
    return city
#傳出圖片
from fastapi.responses import FileResponse
import os
@app.get("/cities/image/{cityName}")
async def city_image(cityName:str):
    conn = sqlite3.connect('citys.db')
    cursor = conn.cursor()
    sql = "SELECT * FROM city WHERE ctiyName=?"    
    cursor.execute(sql,(cityName,))
    row = cursor.fetchone()
    imageName:str = row[4]
    cursor.close()
    conn.close()    
    return FileResponse(f'./images/{imageName}')
