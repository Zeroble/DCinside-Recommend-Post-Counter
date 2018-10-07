from bs4 import BeautifulSoup
import requests
from datetime import datetime

TIME_LIMIT = 7
i = 1
date_format = "%Y-%m-%d"
datas = []
breakCode = False

maxAverageRecommendDates = []
maxAverageRecommend = 0
maxRecommendPostsDates = []
maxRecommendPosts = 0

def serchData(date,time):
    global datas
    '''
    global maxRecommendPostsDates
    global maxAverageRecommendDates
    global maxAverageRecommend
    global averageRecommends
    '''
    cnt = 0
    averageRecommends = 0
    for i in datas:
        if(i["date"] == date and time == i["time"][0]):
            cnt+=1
            averageRecommends+=int(i["recommend"])
    if cnt is 0:
        averageRecommends = 0
    else:
        averageRecommends=averageRecommends//cnt
    return str(cnt)+"/"+str(averageRecommends)

def printData(str):
    print("%12s" % str, end="")
def parseDate(date):
    global breakCode
    date = date.split(" ")
    data = {}
    delta = datetime.strptime(datetime.today().strftime(date_format), date_format) - datetime.strptime(date[0],date_format)
    if(delta.days>TIME_LIMIT):
        breakCode = True
    if(delta.days is 0):
        return False
    data["date"] = date[0]
    data["time"] = date[1].split(":")
    return data
BASEURL = input('input gallery URL like "http://gall.dcinside.com/board/lists/?id=cat": ')
while True:
    print("NOW PAGE : ",i)
    recommendPage = BeautifulSoup(requests.get(BASEURL + "&page=" + str(i) + "&exception_mode=recommend").text,"html.parser")
    for j in recommendPage.select('#container > section.left_content > article > div.gall_listwrap.list > table > tbody > tr'):
        if(j.select("td.gall_num")[0].text != "공지"):
            recommend = j.select("td.gall_recommend")[0].text
            date = parseDate(j.select("td.gall_date")[0].get("title"))
            if(date is False):
                continue
            if(breakCode):
                break
            data = {}
            data["date"] = date["date"]
            data["time"] = date["time"]
            data["recommend"] = recommend
            datas.append(data)
            print(data)
    if (breakCode):
        break
    i+=1

datas.reverse()
previous_date = "000000000000000000000000000"
printData("")
dates = []
for i in datas:
    if(previous_date != i["date"]):
        previous_date = i["date"]
        dates.append(previous_date)
        printData(previous_date)
print()
for i in range(0,25):
    printData(i)
    for j in dates:
        time = str(i)
        if time.__len__() is 1:
            time = "0"+time
        printData(serchData(j,time))
    print()