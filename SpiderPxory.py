#!/usr/bin/env python
# coding=utf-8
# skyvvx
# http://www.linuxyw.com
import urllib
import urllib2
import socket
import threading
import random
import bs4
from bs4 import BeautifulSoup
from gzip import GzipFile
from StringIO import StringIO
import zlib
import gzip
import re
import string
import time
import Queue
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

q = Queue.Queue()
# 要采集的网址
indexurl = "www.xicidaili.com"

uas = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
     'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
     'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
     'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
     'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
     'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
     'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
     'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
     'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
     'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
     'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11'
]
Cookie = "CNZZDATA1256960793=1736984896-1482898250-%7C1482898250; _free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWFlMzNiMWI3YzNiYWE5NWU2OTYzZGMzMjFjMDBlN2FhBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVlaaVEyM3NSeUVGSHNROHFVaDdqbUVoUVBTRmNyRlVMTHBkT2dKWlgwNzQ9BjsARg%3D%3D--0b444fc75c741fa892881b5c706612a5dad3fe5c; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1495011851; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1495012858"
# 设置http 头部信息
headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
    "Referer":indexurl,
    "Cookie": Cookie,
    "User-Agent": random.choice(uas),
    "if-None-Match":'W/"127341086613f8b9e2440cfb5c9102e3"'
}
# 设置 user-agent列表，每次请求时，可在此列表中随机挑选一个user-agnet

#设置访问代理
def setproxy(type, ip, port):
    proxy_host = {type:type+'://'+ip+':'+port}
    if(len(proxy_host)):
        proxy_support = urllib2.ProxyHandler(proxies=proxy_host)
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
    return

def urlget(url):
    req = urllib2.Request(url,data=None,headers=headers)
    rep = urllib2.urlopen(req)
    res = rep.read()
    encoding = rep.info().get('Content-Encoding')
    if encoding == 'gzip':
        resphtml = getzip(res)
    elif encoding == 'deflate':
        resphtml = deflate(res)
    return resphtml.decode('utf-8')


def urlpost(url, param):
    req = urllib2.Request(url)
    data = urllib.urlencode(param)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()

#获取所有页面
def gettotalpage(iptype, pageurl):
    respage = urlget(pageurl)
    parent = re.compile(r'<a href="(/[^"]{2}/\d*)">([^<]\d*)</a>')
    pagelist = re.findall(parent, respage)
    return pagelist[len(pagelist)-1]

#获取所有页面可用ip
def getpageipandtest(pageurl):
    respage = urlget(pageurl)
    parent = re.compile(r'<tr\s*[^>]*>\s*<td\s*[^>]*><img\s*[^>]*></td>\s*<td>([^<]*)</td>\s*<td>([0-9]{0,5})</td>\s*<td>\s*<a\s*[^>]*>([^<]*)</a>\s*</td>\s*<td[^>]*>([^<]*)</td>\s*<td[^>]*>([\w]*)</td>')
    pagelist = re.findall(parent,respage)
    for x in pagelist:
        thread = threading.Thread(target=checkip, args=(x[4],x[0],x[1],x[2]))
        threads.append(thread)
        thread.start()
        thread.join()
    return
def getzip(data):
    buf = StringIO(data)
    f = gzip.GzipFile(fileobj=buf)
    return f.read()


def deflate(data):
    try:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)


#检查代理IP的可用性
fp = open('ip.txt', 'w+')
def checkip(type, ip, port, addr):
    socket.setdefaulttimeout(10)
    #url = "http://www.baidu.com"
    proxy_host = {type: type + '://' + ip + ':' + port}
    try:
        lock.acquire()
        r= requests.get('http://1212.ip138.com/ic.asp',proxies=proxy_host,headers = headers)
        r.encoding = 'gb2312'
        var = r.text.decode('utf-8')
        parent = re.compile(r'\[(.*?)\]\s*([^<]*)')
        log = re.findall(parent,var)
        for i in log:
            print i[1],type,ip,'is ok'
        # setproxy(type,ip,port)
        # res = urlget(url)
    except Exception,e:
        print('connect ip fail',ip)
        lock.release()
        return False
    else:
        fp.seek(0,2)
        fp.write(ip + ':' + port+'\r\n')
        fp.flush()
        lock.release()
        return True

threads = []
lock = threading.Lock()
def start():
    # #获取12306bypass所有代理ip列表并进行测试
    # respdata = urlpost("http://www.12306bypass.com/Cdn.ashx", "")
    # parent = re.compile(r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))")
    # iplist = re.findall(parent, respdata)
    # return iplist
    try:
		#获取首页
        indexpage = urlget('http://www.xicidaili.com')
    except Exception, e:
        print e
		#获取所有二级目录
    parent = re.compile(r'<h2>([^<]*)</h2>\s*<a[^>]+?href="(/[^"]*)">')
    urllist = re.findall(parent, indexpage)
    for x in urllist:
        print x[0]
        maxpage = gettotalpage(x[0], "http://www.xicidaili.com" + x[1])
        maxvalue = int(maxpage[1])
        for i in range(1,maxvalue):
            getpageipandtest("http://www.xicidaili.com" + x[1]+"/"+str(i), )
            time.sleep(random.randint(0,4))
    fp.close()
    

start()
        