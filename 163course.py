import re
from urllib import request
import os
import sys
import time
all_course_url=[]

def get_page(url_any):
    """获取文本网页内容"""
    req=request.urlopen(url_any)
    content=req.read().decode("gb18030")
    return content

def get_all_course(url_any):
    """获取所有课程"""
    ss=get_page(url_any)
    sec_content=ss.split("var _movies = []")
    cc=re.compile(r"http://open.163.com/movie/[\d\/\w]{5,}\.html")
    global all_course_url
    tmp=cc.findall(sec_content[1])
    for x in tmp:
        if x not in all_course_url:
            all_course_url.append(x)
    print("\n获取到 {0} 个课程视频地址".format(len(all_course_url)))

def parse_html(course_url):
    """解析单个网页 获取视频名称等内容"""
    ss=get_page(course_url)
    tmp=ss.split("number : ")
    course_seq=int(tmp[1][:tmp[1].find(",")])
    tmp=tmp[1].split("title : '")
    vedio_name=tmp[1][:tmp[1].find("'")]
    course_name=tmp[2][:tmp[2].find("'")]
    tmp=tmp[1].split("appsrc : '")
    tmp=tmp[1][:tmp[1].find(".m3u8",0,90)]
    tmp=tmp.replace("mp4","flv")
    if tmp.find("-list")!=-1:
        vedio_url=tmp[:-5]+".flv"
    elif  tmp.find("_shd")!=-1:
        vedio_url=tmp.replace("_shd","_hd")+".flv"
    else:
        vedio_url=tmp+".flv"
    #下载视频
    if not os.path.exists(course_name):
        os.mkdir(course_name)
    print("\n开始下载课程 {0} {1}、{2}".format(course_name,course_seq,vedio_name))
    file_name="{0}/{1}.{2}.flv".format(course_name,course_seq,vedio_name)
    tmp_name="{0}/{1}.flv".format(course_name,course_seq)
    if os.path.exists(file_name):
        print("......{0}.{1} 已下载完成\n".format(course_seq,course_name))
        return
    time_start=time.time()
    with open(tmp_name,"wb+") as f:
        count=0
        req=request.urlopen(vedio_url)
        tot=conv_size(req.length)
        while True:
            sys.stdout.flush()
            c=req.read(512*1024)
            count+=len(c)
            print("{0}...{1}         ".format(conv_size(count),tot),end="")
            if len(c)==0:
                break
            f.write(c)
            sys.stdout.write("\r\r\r\r\r\r\r\r")
    os.renames(tmp_name,file_name)
    print("耗时 {0} 秒".format(round(time.time()-time_start),2))

def conv_size(size):
    if size < 1024:
        return str(size)+"B"
    if size <1024*1024:
        return str(round(size/1024,2))+"K"
    if size < 1024*1024*1024:
        return str(round(size/(1024*1024)))+"M"
    if size < 1024*1024*1024*1024:
        return str(round(size/(1024*1024*1024)))+"G"

if __name__=="__main__":
    #获取所有课程
    url=input("\n请打开课程内任一视频播放页面，复制其网址后粘贴并按回车键开始下载：\n")
    get_all_course(url)
    #逐一下载课程
    for course in all_course_url:
        #获取视频下载链接
        vedio_url=parse_html(course)

    input("当前课程下载完成")
