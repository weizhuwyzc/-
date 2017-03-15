# -*-coding:utf-8-*-

import re
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spider(object):
    def __init__(self):
        print "start spider"
    def changepage(self, url, total_page):
        now_page = int(re.search('pageNum=(\d+)', url, re.S).group(1))
        page_group = []
        for i in range(now_page, total_page+1):
            link = re.sub('pageNum=\d+', 'pageNum=%s'%i, url, re.S);
            page_group.append(link);
        return page_group;

    def getsource(self,url):
        html = requests.get(url)
        return html.text;

    def geteveryclass(self, source):
        everyclass = re.findall('<li id="(.*?)</li>', source, re.S);
        return everyclass;
    def getinfo(self, eachclass):
        info = {}
        info['title'] = re.search('title="(.*?)" alt', eachclass, re.S).group(1);
        info['content'] = re.search('<p style="height: 0px; opacity: 0; display: none;">(.*?)</p>', eachclass, re.S).group(1);
        timeandlevel = re.findall('<em>(.*?)</em>', eachclass, re.S);
        info['classtime'] = timeandlevel[0];
        info['classlevel'] = timeandlevel[1];
        info['learnnum'] = re.search('"learn-number">(.*?)</em>', eachclass, re.S).group(1);
        return info;
    def saveinfo(self, classinfo):
        f = open('info.txt', 'a');
        for each in classinfo:
            f.writelines('title:' + each['title'] + '\n');
            f.writelines('content:' + each['content'] + '\n');
            f.write('classtime:' + each['classtime'] + '\n');
            f.writelines('classlevel:' + each['classlevel'] + '\n');
            f.writelines('learnnum:' + each['learnnum'] + '\n');
            f.writelines('************************************\n\n');
        f.close();

if __name__ == '__main__':
    classinfo = []
    url = 'https://www.jikexueyuan.com/course/?pageNum=1'
    jikespider = spider();
    all_links = jikespider.changepage(url, 20)
    # print all_links
    for link in all_links:
        print u'正在处理页面：' + link
        html = jikespider.getsource(link);
        everyclass = jikespider.geteveryclass(html);
        for each in everyclass:
            info = jikespider.getinfo(each);
            #print each;
            classinfo.append(info);

    jikespider.saveinfo(classinfo);

