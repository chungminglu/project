import time
import threading
class myThread (threading.Thread):
   def __init__(self, threadID,year,month,day):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.year = year
      self.month= month
      self.day=day
   def run (self):
       crawlerchina(self.year,self.month,self.day)  
def crawlerchina(year,month,day):
    import requests
    from bs4 import BeautifulSoup
    import lxml,html5lib
    from splinter import Browser
    import time
    import random
    year=year     #'''出發時間'''
    month=int(month)
    day=int(day)#強轉成整數
    year1=year#'返回時間'
    month1=int(month)
    day1=int(day)+5
    while(True):
        count=1 #計算這個連線下載次數
        if(month>12):
            year=int(year)+1
            year='%s' %(str(year))
#       year='%s' %(str(year))#轉成字串
        elif(month==1|month==3|month==5|month==7|month==8|month==10|month==12):#檢查31號的月份
            if(day>31):
                day=1
                month=int(month)+1
#             month='%s' %(str(month))
        elif(month==4|month==6|month==9|month==11):
            if(day>30):
                day=1
                month=int(month)+1
#               month='%s' %(str(month))
        elif(month==2):
            if(day>28):
                day=1
                month=int(month)+1
#               month='%s' %(str(month))
        month='%s' %(str(month))
        day='%s'%(str(day))
        if(len(day)==1&len(month)==1):
            date='%s/0%s/0%s' %(year,month,day)
        else:
            date='%s/%s/%s' %(year,month,day)       
        if(month1>12):
            year1=int(year1)+1
            year1='%s' %(str(year1))
#       year1='%s' %(str(year))#轉成字串
        if(month1==1|month1==3|month1==5|month1==7|month1==8|month1==10|month1==12):#檢查31號的月份
            if(day1>31):
                day1=1
                month1=int(month1)+1
                month1='%s' %(str(month1))
        elif(month1==4|month1==6|month1==9|month1==11):
            if(day1>30):
                day1=1
                month1=int(month1)+1
#               month1='%s' %(str(month1))
        elif(month1==2):
            if(day1>28):
                day1=1
                month=int(month1)+1
#               month='%s' %(str(mont1))
        month1='%s' %(str(month1))
        day1='%s' %(str(day1))
        if(len(day1)==1&len(month1)==1):
            date1='%s/0%s/0%s' %(year1,month1,day1)
        else:
            date1='%s/%s/%s' %(year1,month1,day1)
        print('%s downlowing'%(date))
        # browser=Browser("chrome")
        browser=Browser('phantomjs')
        browser.driver.set_window_size(400, 1600)
        browser.visit("https://www.china-airlines.com/tw/zh?utm_content=RGT-01-140MAR17GOSEM&utm_source=GO&utm_medium=sem&utm_campaign=RGT&utm_number=140")
        browser.find_by_id('From-booking').fill('台北')
        browser.find_by_id('To-booking').fill('大阪-KIX-日本')
        time.sleep( random.uniform(0.1,5))
        browser.find_by_xpath('//*[@id="departureDateMobile"]').fill(date)
        time.sleep(random.uniform(0.1,5))
        browser.find_by_xpath('//*[@id="returnDateMobile"]').fill(date1)
        time.sleep(random.uniform(0.1,5))
        browser.cookies.delete()        
        browser.find_by_xpath('//*[@id="FlightSearchResultPost"]/div[3]/div/div[5]/a').click()
        print(browser.status_code)
        count+=1
        while True:
            if browser.is_element_present_by_text('航班')==True:   
                with open('./{}{}{}.html'.format(year,month,day),'w',encoding='utf-8') as f:
                    f.write(browser.html)
                    f.close()
                break
            if browser.is_element_present_by_text('Access To Website Blocked')==True:
                
                break 
#         if(count>=10):#移除這個browser
#         browser.cookies.delete()
        browser.quit()
        day=1+int(day)#字串轉整數
        day1=1+int(day)
        month=int(month)
        month1=int(month1)
if __name__ == '__main__':
    print("thread 請輸入三個 year,month,day:")
    a=input()
    b=input()
    c=input()
    thread1=myThread(1,a,b,c)
    print("thread 請輸入三個year,month,day:")
    a=input()
    b=input()
    c=input()
    thread2=myThread(2,a,b,c)
    print("thread 請輸入三個year,month,day:")
    a=input()
    b=input()
    c=input()
    thread3=myThread(3,a,b,c)
    threads=[]
    try:
        thread1.start()
        thread2.start()
        thread3.start()
        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)
        for t in threads:
            t.join()
            print(" {} Exiting Main Thread".format(t))
    except:
        pass
