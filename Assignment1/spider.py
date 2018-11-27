# coding:utf-8
from bs4 import BeautifulSoup
import requests
import re
import csv
count =0
index =1
#
#Goal: 出前TripAdvisor HK 20页的餐厅名字，餐厅排名，点评数量，餐厅类型/标签，价格区间，
#
file = open('result.csv', 'w')
fileObject=csv.writer(file)
fileObject.writerow(['name','rank','reviews','tag','price'])
while index<=20:
    if index==1:
        url="https://en.tripadvisor.com.hk/Restaurants-g294217-Hong_Kong.html"
    else:
        pagenum=(index-1)*60
        url="https://en.tripadvisor.com.hk/RestaurantSearch-g294217-oa"+str(pagenum)+"-Hong_Kong.html#EATERY_LIST_CONTENTS"
    r = requests.get(url)
    # Acquire the whole html page after accessing the first page
    blog = r.content
    #Decode with html.parser
    soup = BeautifulSoup(blog, "html.parser")
    tag_soup = soup.find_all(class_=re.compile("ui_column is-9 shortSellDetails"))



    for i in tag_soup:
        #print(i)
        if i.find(class_="title").find("a"):
            name = i.find(class_="title").find("a").text
        rank=i.find(class_="popIndexBlock").find(class_="popIndex rebrand popIndexDefault").text
        reviews=i.find(class_="rating rebrand").find(class_="reviewCount").find("a").text
        desc=""
        price=""
        if i.find(class_="cuisines"):
            tag = i.find(class_="cuisines").find_all(class_="item cuisine")
            desc=tag[0].text
            for item in tag[1:]:
                desc=desc+","+item.text
        if i.find(class_="cuisines"):
            if i.find(class_="cuisines").find(class_="item price"):
                price=i.find(class_="cuisines").find(class_="item price").text
        #print(name,rank,reviews,desc,price)
        tlist = []
        tlist.append(name)
        tlist.append(re.findall(r"#(.+?) of", rank)[0])
        tlist.append(re.findall(r"(.+?) reviews", reviews)[0].replace(",",""))
        tlist.append(desc)
        tlist.append(price)
        fileObject.writerow(tlist)
        del tlist[:]  # Delete lists
        count=count+1
    index=index+1
print(count)
file.close()
