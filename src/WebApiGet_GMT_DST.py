import re
from sqlite3 import DatabaseError
from traceback import print_tb
import requests
import csv
import time
import random
from io import BytesIO
from lxml import etree
from pytz import timezone
from datetime import datetime
import pandas as pd
import datetime

url = "https://timezonedb.p.rapidapi.com/"


def pri():
    print("==========")

def replaceStr(inputstr):
    trans_str = "".join(inputstr)
    trans_str = trans_str.replace("[","").replace("]","").replace("\'","")
    return trans_str

# 開啟IATA AIRPORT CODE經緯度
with open('\Data.csv') as csvfile:
    rows = csv.reader(csvfile)

    with open('\GMT_DST.txt', 'a', encoding='utf-8') as GMT_DST:
        # 印表頭資訊
        print("IATA"+","+"latitude"+","+"longitude"+","+"country_iso"+","+"ZoneTime"+","+"GMT"+","+"DST"+","+"DST Start"+","+"DST End", file=GMT_DST)
    GMT_DST.close()

    for row in rows:
        with open('\GMT_DST.txt', 'a', encoding='utf-8') as GMT_DST:
            # 填入API金鑰 key
            querystring = {"key": "", "lat": row[1], "lng": row[2], "format": "xml"}

            headers = {
                'x-rapidapi-host': "timezonedb.p.rapidapi.com",
                # 填入rapidapi-key
                'x-rapidapi-key': ""
            }

            # 抓時區
            response = requests.request("GET", url, headers=headers, params=querystring)
            # xml轉換
            outxml = etree.parse(BytesIO(response.content))
            # xml輸出
            countryCode = [t.text for t in outxml.xpath("countryCode")]
            dstzoneName = [t.text for t in outxml.xpath("zoneName")]
            gmtTime = [t.text for t in outxml.xpath("gmtOffset")]
            dstTime = [t.text for t in outxml.xpath("dst")]
            # 轉成正常STR
            StrDstZoneName = replaceStr(dstzoneName)
            StrCountryCode = replaceStr(countryCode)
            StrGmtTime = replaceStr(gmtTime)
            StrDstTime = replaceStr(dstTime)

            # 用時區抓取DST開始結束時間
            tzto = timezone(StrDstZoneName)

            # 所有當地DST歷年開始以及結束時間
            All_StartAndEndTimeForDst = tzto._utc_transition_times

            # 設定DateRange
            NowYear = (datetime.datetime.now().year)
            DST_StartRangeTime = datetime.datetime(NowYear, 1, 1, 0, 0, 0)
            DST_EndRangeTime = datetime.datetime(NowYear, 12, 31, 0, 0, 0)

            # 測試輸出======
            # 原始response內容
            pri()
            print(response.text, end="")
            pri()
            # 顯示當前查詢DST區域名稱、經緯度
            print(row[0]+","+row[1]+","+row[2]+","+StrCountryCode+","+StrDstZoneName+","+StrGmtTime+","+StrDstTime+",", file=GMT_DST, end="")
            # flag記換行
            flag = 1
            # nodata記當年沒有執行DST時間
            nodata = 0
            for lenDst in range(len(All_StartAndEndTimeForDst)):
                if All_StartAndEndTimeForDst[lenDst] > DST_StartRangeTime and All_StartAndEndTimeForDst[lenDst] < DST_EndRangeTime:
                    f = All_StartAndEndTimeForDst[lenDst]
                    nodata = nodata + 1
                    print(f, file=GMT_DST, end='')
                    if flag == 1:
                        print(",", file=GMT_DST, end="")
                    else:
                        print("", file=GMT_DST)
                    flag = 2

            if nodata == 0:
                print("No DST", file=GMT_DST)

        GMT_DST.close()

        time.sleep(random.randint(2, 5))
