# todo
import requests
import os
import img2pdf
import shutil
import multiprocessing

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time
from datetime import date

import yaml

# import socket
# import socks
# sock=socket.socket()
# socks.set_default_proxy(socks.SOCKS5,'127.0.0.1',8889)
# socket.socket=socks.socksocket
# sock.connect(('127.0.0.1',8889))
# user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
# headers = {
#     'User-Agent': user_agent
# }
# my_proxies={"http":"socks5://127.0.0.1:8889","https":"socks5://127.0.0.1:8889"}

def get_page(args):
    page_url,now_page_num=args
    # pic=requests.get(page_url,proxies=my_proxies,timeout=5)
    pic=requests.get(page_url,timeout=5)
    with open("temp/"+str(now_page_num)+'.png','wb') as f:
        f.write(pic.content)
    print(str(now_page_num)+'done')

def parallel_download(page_num,a_url):
    pool=multiprocessing.Pool(processes=8)
    x1=a_url.find("&width=")
    x2=a_url.find("&ServiceType=")
    pool.map(get_page,[(a_url[:x1]+'&width=1500&height=2100&pageid='+str(i)+a_url[x2:],i) for i in range(1,page_num+1)])
    pool.close()

def get_detail_by_bookname(driver,bn):
        # driver.get(tt_url)
    driver.get("http://162.105.138.126/Usp")
    WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,'tbKeywords'))
    ).send_keys(bn)
    WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,'uspSearch'))
    ).click()
    WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,'tbKeywords'))
    ).clear()
    try:
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.TAG_NAME,'img'))
        ).click()
    except:
        print('not found')
        return 0
    driver.switch_to.window(driver.window_handles[1])


    bookname=WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.CLASS_NAME,'title'))
    ).text
    # bookname=driver.find_element_by_class_name('title').text
    driver.find_element_by_id('onlineread').click()
    driver.switch_to.window(driver.window_handles[2])
    page_num=int(
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID,'TotalCount'))
        ).text
    )
    # page_num=int(driver.find_element_by_id('TotalCount').text)
    t_url=WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,'img1'))
    ).get_attribute('src')

    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    # driver.close()
    print('get details successfully!\Book\'s name is %s\nPagenum is %d'%(bookname,page_num))
    return {'bookname':bookname,'page_num':page_num,'t_url':t_url}

def get_by_url(driver,url):
    driver.get(url)
    bookname=WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.CLASS_NAME,'title'))
    ).text
    # bookname=driver.find_element_by_class_name('title').text
    driver.find_element_by_id('onlineread').click()
    driver.switch_to.window(driver.window_handles[-1])
    page_num=int(
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID,'TotalCount'))
        ).text
    )
    # page_num=int(driver.find_element_by_id('TotalCount').text)
    t_url=WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,'img1'))
    ).get_attribute('src')

    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    # driver.switch_to.window(driver.window_handles[-1])
    # driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    # driver.close()
    print('get details successfully!\Book\'s name is %s\nPagenum is %d'%(bookname,page_num))
    return {'bookname':bookname,'page_num':page_num,'t_url':t_url}

def get_by_page_url(driver,url,bookname):
    driver.get(url)
    page_num=int(
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID,'TotalCount'))
        ).text
    )
    # page_num=int(driver.find_element_by_id('TotalCount').text)
    t_url=WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,'img1'))
    ).get_attribute('src')

    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    # driver.switch_to.window(driver.window_handles[-1])
    # driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    # driver.close()
    print('get details successfully!\Book\'s name is %s\nPagenum is %d'%(bookname,page_num))
    return {'bookname':bookname,'page_num':page_num,'t_url':t_url}


def download_by_details(details):
    if(details==0):
        return
    bookname=details['bookname']
    page_num=details['page_num']
    t_url=details['t_url']
    print('get details successfully!\Book\'s name is %s\nPagenum is %d'%(bookname,page_num))
    print('continue?y/n:\n')
    y_or_n=input()
    if(y_or_n!='n'):
        
        os.makedirs("temp")
        print("downloading pictures")

        parallel_download(page_num,t_url)

        print("Changing")
        with open(bookname+".pdf","wb") as f:
            f.write(img2pdf.convert(list("temp/"+str(i)+'.png' for i in range(1,page_num+1))))
        print("done")
        shutil.rmtree("temp")

if __name__ == "__main__":
    
    profile = webdriver.FirefoxProfile()

    # read id,password,headless from config.yaml
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    id = config['id']
    password = config['password']
    headless = config['headless']
    

    # # Socks5 Host SetUp:-
    # myProxy = "127.0.0.1:7900"
    # ip, port = myProxy.split(':')
    # profile.set_preference('network.proxy.type', 1)
    # profile.set_preference('network.proxy.socks', ip)
    # profile.set_preference('network.proxy.socks_port', int(port))

    ff_op=webdriver.FirefoxOptions()
    ff_op.headless=headless
    driver=webdriver.Firefox(options=ff_op,firefox_profile=profile) 

    # driver=webdriver.Firefox()
    driver.get("http://162.105.138.126/Usp")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user_name"))
    ).send_keys(id)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('logon_button').click()
    # time.sleep(1)



    # t_url=driver.find_element_by_id("img1").get_attribute('src')
    # driver.quit()
    # book_list=['量子力学教程']
    # for bn in ['量子力学教程']:
    #     details=get_detail_by_bookname(driver,bn)
    #     download_by_details(details)
    select=0
    try:
        while(select!='q'):
            details={}
            select=input('which type?\n1\tby bookname\n2\tby book details url\n3\tby book page url and name\nq\tquit\n')

            if select=='1':
                bn=input('bookname?\n')
                if(bn):
                    details=get_detail_by_bookname(driver,bn)
            # details=0
            # if(bn[:4]=='http'):
            elif select=='2':
                bn=input('book details url\n')
                if(bn):
                    details=get_by_url(driver,bn)
                
            elif select=='3':
                break
                page_url=input('page url\n')
                bookname=input('bookname\n')
                if(page_url and bookname):
                    details=get_by_page_url(driver,page_url,bookname)
            else:
                select='q'
                break
            if(details):
                download_by_details(details)  
        driver.quit()
    except:
        print('error')
        try:
            driver.quit()     
        except:
            print('driver already quit')



