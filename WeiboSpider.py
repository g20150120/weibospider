#-*-coding:utf8-*-

#-----------------!IMPORTANT!--------------------
#-----------------!IMPORTANT!--------------------
#--- UPDATE USER_ID & COOKIE FIRST!
#--- REMEMBER TO CD ./1234567890 ETC. TO SAVE ALL THE .TXT AND WEIBO_IMAGE!
#--- YOU MAY NEED TO OPEN .TXT FILE IN CHROME TO DECODE IT
#-----------------!IMPORTANT!--------------------
#-----------------!IMPORTANT!--------------------

import re
import string
import sys
import os
import urllib
import urllib2
import requests
import shutil
import time
from lxml import etree

reload(sys) 
sys.setdefaultencoding('utf-8')

#put user id here:  m.weibo.cn/u/%d
user_id = 0

#chrome->inspect->network; go to https://m.weibo.cn; log in; m.weibo.cn->request headers->cookie:
cookie = {"Cookie": ""}

#set filter_value to 1 to include only original posts, 0 to include all posts(not implemented in this code)
filter_value = 1

#simplified version of web weibo:
url = 'https://weibo.cn/u/%d?filter=%d&page=1'%(user_id,filter_value)

#get homepage:
html = requests.get(url, cookies = cookie).content
print 'Get homepage successfully!'

#get html:
selector = etree.HTML(html)
#get total number of pages
pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

#--------------------!CAREFUL!-------------------
#--------------------!CAREFUL!-------------------
page_start = 1
page_end = pageNum
pageNum = page_end - page_start + 1
#--------------------!CAREFUL!-------------------
#--------------------!CAREFUL!-------------------

result = "" 
urllist_set = set()
failedurl_set = set()
word_count = 1
image_count = 1

print 'Total number of pages = ',pageNum
sys.stdout.flush()

#sleep is measured in seconds
sleep_between_pages = 1
sleep_between_steps = 1
steps = 5
one_step = pageNum/steps

for step in range(0,steps): # [0,steps-1]
    if step < steps - 1:
        i = step * one_step + page_start
        j =(step + 1) * one_step + page_start
    else: # (step = steps - 1)
        i = step * one_step + page_start
        j =page_end + 1
    
    for page in range(i, j):
        #get lxml (I don't know why, probably to translate <br>, emojis, &amp; etc.)
        #and store all the texts and img_urls in arrays in RAM; then write into files or download to a folder
        try:
            url = 'https://weibo.cn/u/%d?filter=1&page=%d'%(user_id,page) 
            html = requests.get(url, cookies = cookie).content
            #get text
            selector = etree.HTML(html)
            #find all the <span> tags with class "ctt"
            content = selector.xpath('//span[@class="ctt"]')
            for each in content:
                text = each.xpath('string(.)')
                if word_count >= 3:
                    text = "%d: "%(word_count - 2) +text+"\n"
                else :
                    text = text+"\n\n"
                result = result + text
                word_count += 1
            print page,'text OK'
            sys.stdout.flush()
            
            #RegExp to find all oripic links in this page
            reg = 'a href="https://weibo.cn/mblog/oripic([^"]+?)">'
            patt = re.compile(reg,re.I)
            urllist = re.findall(patt,html)
            # ?id=Fj935zHBX&amp;u=b836907bgy1fiz42rkq24j20qo0zktdj
            # https://weibo.cn/mblog/oripic?id=Fj935zHBX&u=b836907bgy1fiz42rkq24j20qo0zktdj.jpg
            # http://wx4.sinaimg.cn/large/b836907bgy1fiz42rkq24j20qo0zktdj.jpg

            #RegExp to find all sub-page of oripics in this page           
            reg1 = 'a href="https://weibo.cn/mblog/picAll([^"]+?)">'
            patt1 = re.compile(reg1,re.I)
            urllist1 = re.findall(patt1,html)
            # /Fj935zHBX?rl=1
            # https://weibo.cn/mblog/picAll/Fj935zHBX?rl=1

            #iterate through all the oripics on this page:
            for imgurl in urllist: 
                #firstly restore &amp;
                imgurl = imgurl.replace("&amp;","&")
                #then restore url (this url can ba accessed without cookie)
                imgurl = 'http://wx4.sinaimg.cn/large/' + imgurl.split('&')[1].split('=')[1] + '.jpg'                
                #print large_img_url in terminal
                print 'img_url %d = %s'%(image_count,imgurl)
                #add to set
                urllist_set.add(imgurl)
                image_count += 1
            
            #iterate through picAll links on homepage:
            for imgurl_all in urllist1:
                #restore url
                imgurl_all = 'https://weibo.cn/mblog/picAll' + imgurl_all
                #print link in terminal
                print 'picAll_url = ',imgurl_all
                #get picAll page
                html_content = requests.get(imgurl_all, cookies = cookie).content 
                
                #RegExp to find all oripics on sub-page                
                reg2 = 'a href="/mblog/oripic([^"]+?)">'
                patt2 = re.compile(reg2,re.I)
                urllist2 = re.findall(patt2,html_content)

                #iterate from 1 since urllist2[0] has already been saved
                for i in range(1,len(urllist2)):  # [1,len-1]
                    imgurl = urllist2[i]
                    #firstly restore &amp;
                    imgurl = imgurl.replace("&amp;","&")
                    #then restore url (this url can ba accessed without cookie)
                    imgurl = 'http://wx2.sinaimg.cn/large/' + imgurl.split('&')[1].split('=')[1] + '.jpg'
                    #print in terminal
                    print 'sub-page img_url %d = %s'%(image_count,imgurl)
                    #add to list
                    urllist_set.add(imgurl)
                    image_count += 1
            
            print page,'img_url OK'
        
        except:
            print page,'ERROR'
        
        print page, 'Sleep'
        sys.stdout.flush()
        time.sleep(sleep_between_pages)
    
    print u'Stop No. ', step + 1
    time.sleep(sleep_between_steps)

#write data(text and img_url) in RAM into .txt file
try:
    fo = open(os.getcwd()+"/%d_raw.txt"%user_id, "wb")
    fo.write(result)
    fff = open(os.getcwd()+"/%d.txt"%user_id, "wb")
    fff.write(result)
    word_path=os.getcwd()+'/%d.txt'%user_id
    print u'All texts are OK'
    link = ""
    fo2 = open(os.getcwd()+"/%s_image.txt"%user_id, "wb")
    for eachlink in urllist_set:
        link = link + eachlink +"\n"
    fo2.write(link)
    print u'All img_urls are OK'
except:
    print u'ERROR'
sys.stdout.flush()

if not urllist_set:
    print u'No oriPic found'
else:
    #download all the images
    image_path=os.getcwd()+'/weibo_image'
    if os.path.exists(image_path) is False:
        os.mkdir(image_path)
    os.chdir(image_path)
    x = 1
    for imgurl in urllist_set:
        print u'Downloading image No. %s' % x
        try:
            # download_add = requests.get(imgurl, cookies = cookie).url
            urllib.urlretrieve(imgurl, '%s.jpg'%x)
        except:
            failedurl_set.add(imgurl)
            print u"Downloading image No. %d failed"%x
        x += 1

if not failedurl_set:
    print 'All oriPics downloaded successfully'
else:
    link = ""
    fo3 = open(os.getcwd()+"/%s_failedimage.txt"%user_id, "wb")
    for eachlink in failedurl_set:
        link = link + eachlink +"\n"
    fo3.write(link)
    print u'All failed links are recorded'

print 'END'













