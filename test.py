import requests
from bs4 import BeautifulSoup
import lxml,html5lib
from splinter import Browser
import time
import random
year='2017'#'''出發時間'''
month=8
day=1
year1='2017'#'返回時間'
month1=8
day1=6
while(True):
    if(month>12):
        year=int(year)+1
        year='%s' %(str(year))
#     year='%s' %(str(year))#轉成字串
    elif(month==1|month==3|month==5|month==7|month==8|month==10|month==12):#檢查31號的月份
        if(day>31):
            day=1
            month=int(month)+1
#             month='%s' %(str(month))
    elif(month==4|month==6|month==9|month==11):
        if(day>30):
            day=1
            month=int(month)+1
#             month='%s' %(str(month))
    elif(month==2):
        if(day>28):
            day=1
            month=int(month)+1
#             month='%s' %(str(month))
    month='%s' %(str(month))
    day='%s'%(str(day))
    if(len(day)==1&len(month)==1):
        date='%s/0%s/0%s' %(year,month,day)
    else:
        date='%s/%s/%s' %(year,month,day)       
    if(month1>12):
        year1=int(year1)+1
        year1='%s' %(str(year1))
#     year1='%s' %(str(year))#轉成字串
    if(month1==1|month1==3|month1==5|month1==7|month1==8|month1==10|month1==12):#檢查31號的月份
        if(day1>31):
            day1=1
            month1=int(month1)+1
            month1='%s' %(str(month1))
    elif(month1==4|month1==6|month1==9|month1==11):
        if(day1>30):
            day1=1
            month1=int(month1)+1
#             month1='%s' %(str(month1))
    elif(month1==2):
        if(day1>28):
            day1=1
            month=int(month1)+1
#             month='%s' %(str(mont1))
    month1='%s' %(str(month1))
    day1='%s' %(str(day1))
    if(len(day1)==1&len(month1)==1):
        date1='%s/0%s/0%s' %(year1,month1,day1)
    else:
        ate1='%s/%s/%s' %(year1,month1,day1)
    browser=Browser("chrome")
    browser.driver.set_window_size(400, 1600)
    browser.visit("https://www.china-airlines.com/tw/zh?utm_content=RGT-01-140MAR17GOSEM&utm_source=GO&utm_medium=sem&utm_campaign=RGT&utm_number=140")
    browser.find_by_id('From-booking').fill('台北')
    browser.find_by_xpath('//*[@id="From-booking-suggestions"]/li[1]').click()
    browser.find_by_id('To-booking').fill('大阪-KIX-日本')
    time.sleep( random.uniform(0.1,5))
    browser.find_by_xpath('//*[@id="departureDateMobile"]').fill(date)

    browser.find_by_xpath('//*[@id="returnDateMobile"]').fill(date1)
    time.sleep(random.uniform(0.1,5))
    browser.find_by_xpath('//*[@id="FlightSearchResultPost"]/div[3]/div/div[5]/a').click()
    while True:
        if browser.is_element_not_present_by_id('#availability')==True:
            break
    with open('%s.html','w',encoding="utf-8"%(date)) as f:
        f.write(browser.html)
    browser.quit()
    day=1+int(day)#字串轉整數
    day1=1+int(day)
    month=int(month)
    month1=int(month1)
  