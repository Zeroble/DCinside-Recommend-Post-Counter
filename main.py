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
    return cnt,averageRecommends

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
BASEURL = input('input gallery URL or GALLERY NAME : ')
if(not "dcinside" in BASEURL):
    try:
        BASEURL = BeautifulSoup(requests.get("http://search.dcinside.com/gallery/q/"+BASEURL).text, "html.parser").select("#container > div > section.center_content > div.inner > div.integrate_cont.gallsch_result > ul > li > a")[0].get("href")
    except:
        try:
            BASEURL = BeautifulSoup(requests.get("http://search.dcinside.com/gallery/q/" + BASEURL).text, "html.parser").select("#container > div > section.center_content > div.inner > div.integrate_cont.mgallsch_result > ul > li > a")[0].get("href")
            BASEURL = "http://gall.dcinside.com/mgallery/board/lists"+BASEURL[BASEURL.find("?id="):]
        except:
            print("갤러리명을 정확하게 입력하여 주세요.")
            exit(0)
    print("URL : "+BASEURL)

GALLERY_NAME = BeautifulSoup(requests.get(BASEURL).text,"html.parser").select("#container > section.left_content > header > div > div.fl.clear > h2 > a")[0].text
while True:
    print("NOW PAGE : ",i)
    recommendPage = BeautifulSoup(requests.get(BASEURL+ "&page=" + str(i) + "&exception_mode=recommend").text,"html.parser")
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
print(GALLERY_NAME+"의 개념글 검사 결과")
printData("시간/날짜")
dates = [[],[],[]]
for i in datas:
    if(previous_date != i["date"]):
        previous_date = i["date"]
        dates[0].append(previous_date)
        dates[1].append(0)
        dates[2].append(0)
        printData(previous_date)
print()
for i in range(0,25):
    printData(i)
    for j in range(0,dates[0].__len__()):
        time = str(i)
        if time.__len__() is 1:
            time = "0"+time
        POSTS,AVR = serchData(dates[0][j], time)
        printData(str(POSTS)+"/"+str(AVR))
        dates[1][j]+=POSTS
        dates[2][j] += AVR
    print()

printData("")
for j in range(0,dates[0].__len__()):
    printData(str(dates[1][j])+"/"+str(dates[2][j]))