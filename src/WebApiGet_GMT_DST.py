from asyncio.windows_events import NULL
from cProfile import label
from functools import update_wrapper
import airportsdata
import csv
from numpy import delete
import pandas as pd
from datetime import datetime
from pytz import timezone
import datetime as dt 
from dateutil import tz 
import pytz
import datetime
import tkinter as tk
import threading

with open('\Data.csv') as csvfile:
    rows = csv.reader(csvfile)

    for row in rows:
        #輸入的搜尋值設定
        airports = airportsdata.load('IATA')  # key is IATA code
        with open('\Output.txt','a',encoding='utf-8') as Output:
            #字典的labels
            labels=['icao','iata','name','city','state','country','elevation','lat','lon','tz']
            #如果讀出來為Keyerror,用Not found取代
            Airports=airports.get(row[0],'No Found')
            #標點符號
            p=","
            
            if(Airports!='No Found'):
                #設定DateRange
                NowYear = (datetime.datetime.now().year)
                DST_StartRangeTime = datetime.datetime(NowYear, 1, 1, 0, 0, 0)
                DST_EndRangeTime = datetime.datetime(NowYear, 12, 31, 0, 0, 0)
                #TimeZone get DST str and end
                tzto=timezone(Airports[labels[9]])
                #獲取未計算DST之UTC
                utc=(pytz.timezone(Airports[labels[9]]).localize(datetime.datetime(NowYear,1,1)).strftime('%z'))
                ##
                All_StartAndEndTimeForDst=tzto._utc_transition_times
                #篩選當年的 Dst str and end
                #flag記換行
                flag=1
                #nodata記當年沒有執行DST時間
                nodata=0
                for lenDst in range(len(All_StartAndEndTimeForDst)):
                    if(All_StartAndEndTimeForDst[lenDst]>DST_StartRangeTime and All_StartAndEndTimeForDst[lenDst]<DST_EndRangeTime):
                        f=All_StartAndEndTimeForDst[lenDst]
                        nodata=nodata+1
                        if flag==1:
                            strtime=f
                        else:
                            endtime=f
                        flag=2
                    if nodata==0:
                        strtime="No Dst"
                        endtime="No Dst"
                #輸出
                print(Airports[labels[1]]+p+Airports[labels[2]]+p+Airports[labels[5]]+p+Airports[labels[3]]+p+Airports[labels[4]]+p+str(Airports[labels[7]])+p+str(Airports[labels[8]])+p+Airports[labels[9]]+p+utc+p+str(strtime)+p+str(endtime),file=Output)
            else :
                print(row[0]+p+"No Found",file=Output)
                print(row[0])
                #1.iata,2.name,3.country,4.city,5.State,6.lat,7.lon,8.tz,9.GMT,10.DST Str,11.DST End
        Output.close()
csvfile.close()




