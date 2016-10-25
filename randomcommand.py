#coding:utf-8  

import  Image,ImageDraw,ImageFont  
import win32api,win32con,win32gui  
import re,os,sys
import urllib2
from bs4 import BeautifulSoup
from random import choice
import time
import ConfigParser
import tkinter as tk
import thread
import threading
from tkColorChooser import *


hanzisize = 15
interval_minute_change = 20
now_color = (0,0,255)

g_content = ""

changed = 0

def read_cfg():
    try:
        global hanzisize
        global interval_minute_change
        global now_color
        cf = ConfigParser.ConfigParser()

        cf.read(resource_path("default.cfg"))
        hanzisize = int(float(cf.get("cfg", "font_size")))
        interval_minute_change = int(float(cf.get("cfg", "interval_minute_change")))
        now_color = tuple(eval(cf.get("cfg", "now_color")))
        print now_color

        #print interval_minute_change, hanzisize
    except Exception as e:
        #print e
        pass
        

def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)



#获取脚本文件的当前路径
def resource_path(rel_path='icon.ico'):
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path + "/" + rel_path
    elif os.path.isfile(path):
        return os.path.dirname(path) + "/" + rel_path
  
def set_wallpaper_from_bmp(bmp_path):  
    #打开指定注册表路径  
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)  
    #最后的参数:2拉伸,0居中,6适应,10填充,0平铺  
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")  
    #最后的参数:1表示平铺,拉伸居中等都是0  
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")  
    #刷新桌面  
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,bmp_path, win32con.SPIF_SENDWININICHANGE)  
  
def set_wallpaper(img_path, content):  
    #把图片格式统一转换成bmp格式,并放在源图片的同一目录 
    hwnd = win32gui.GetDesktopWindow()
    str = u"hwnd is %x" %(hwnd)
    # method 1
    (left, top, right, bottom) = win32gui.GetClientRect(hwnd)

    img_dir = os.path.dirname(img_path)  
    bmpImage = Image.open(img_path)
    
    bmpImage = bmpImage.resize((right, bottom))
    draw = ImageDraw.Draw(bmpImage)
    global hanzisize
    ttfont = ImageFont.truetype(resource_path("huawen.ttf"), hanzisize)
    
    font_width, font_height = ttfont.getsize("hello")
    
    #print font_height
    one_height = font_height + 1
    i = 14
    for line in content.split('\r\n'):
        
        draw.text((right/3 * 2,i), line, fill=now_color,font=ttfont)
        i = i + one_height
    
    #bmpImage.show()
    
    new_bmp_path = os.path.join(img_dir,'wallpaper.bmp') 
    #print new_bmp_path
    bmpImage.save(new_bmp_path, "BMP")  
    set_wallpaper_from_bmp(new_bmp_path)
    global g_content
    g_content = content

def get_url_content(command):
    response = urllib2.urlopen(command)  
    html = response.read()
    return html
    
#按照宽度分割汉字
def f(string, width):
    allarray = []
    temp = ''
    #print string
    global hanzisize
    ttfont = ImageFont.truetype(resource_path("huawen.ttf"), hanzisize)
    font_width, font_height = ttfont.getsize(string)
    if font_width < width:
        allarray.append(string)
        return allarray
    
    for word in string:
        temp = temp + word
        
        font_width, font_height = ttfont.getsize(temp)
        if font_width >= width:
            allarray.append(temp)
            temp = ''
            
    
    allarray.append(temp)    
        
    return allarray
def devide_each_line(string):
    hwnd = win32gui.GetDesktopWindow()
    str = u"hwnd is %x" %(hwnd)

    (left, top, right, bottom) = win32gui.GetClientRect(hwnd)
    global hanzisize
    ttfont = ImageFont.truetype(resource_path("huawen.ttf"), hanzisize)
    font_width, font_height = ttfont.getsize(u'我')
    
    ret = ""
    for line in string.split('\r\n'):
        if line == "" or line.strip() == "":
            continue
        array =  f(line.strip(), right/3-font_width *2)
       
        #print "[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]"
        #print array
        
        try:
            line = "\r\n".join(array) + "\r\n"

            
            ret = ret + line
        except:
            pass
         
    return ret


    
def get_a_command_random_url():
    all = [1, 2, 3, 4, 5]
    allpage = [1, 2, 3]
    
    url = "http://man.linuxde.net/par/%s/page/%s" % (choice(all), choice(allpage))
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    
    return choice(soup.find_all('a')[8:-8])['href']




def btnHelloClicked():
    global changed
    changed = 1
    alltext = entryCd.get().split('#')
    
    if len(alltext) != 2:
        return
    
    
    
    global interval_minute_change
    
    global hanzisize

    interval_minute_change = int(float(alltext[0].strip()))
    hanzisize = int(float(alltext[1].strip()))
    
    labelHello.config(text = "当前interval:%s 秒, font size: %s" % (interval_minute_change, hanzisize))
    
    conf = ConfigParser.ConfigParser()  
    conf.read(resource_path("default.cfg"))

    conf.set('cfg', 'interval_minute_change', str(interval_minute_change))
    conf.set('cfg', 'font_size', str(hanzisize))
    conf.write(open(resource_path("default.cfg"), "w"))  

class workthread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)
        self.st = 2 
    def run(self):
        while True:
            try:
                #print interval_minute_change, hanzisize
                
                content = get_url_content(get_a_command_random_url())
                soup = BeautifulSoup(content)
                try:
                    soup.find_all(id ="content-index")[0].string = ""
                except:
                    pass
               
                temp0 = "".join(soup.find_all('p')[1].text.split('\n')) + "\r\n"
                temp1 = "\r\n".join(soup.find_all('pre')[0].text.split('\n')) + "\r\n"
                temp2 = "\r\n".join(soup.find_all('pre')[1].text.split('\n'))
                
                temp2 = "\r\n".join(soup.find_all('div', "post_bd post")[0].text.split('\n'))
                
                #print temp0+temp1+temp2
                
                #print 
                set_wallpaper(resource_path("a.jpg"), devide_each_line(temp2))
                global changed
                changed = 0
                
                #睡眠5秒钟检查一次
                interval_before = interval_minute_change
                hanzisize_before = hanzisize
                timess = interval_minute_change/1
                while (timess>0):
                    time.sleep(1)
                    timess = timess - 1
                    if interval_before != interval_minute_change or hanzisize_before != hanzisize or changed == 1:
                        break
            except Exception as e:
                #print e
                continue

def set_color():
    m = askcolor()
    if m[0] ==None:
        return
    print m
    global now_color
    now_color  = m[0]
    conf = ConfigParser.ConfigParser()  
    conf.read(resource_path("default.cfg"))

    conf.set('cfg', 'now_color', now_color)
    conf.write(open(resource_path("default.cfg"), "w"))  
    
    if g_content == "":
        return
    set_wallpaper(resource_path("a.jpg"), g_content)

def printkey(event):
    try:
        #print interval_minute_change, hanzisize alltext = entryCd.get().split('#')
        
        text = entryCd1.get().strip()
        if text == "":
            return
        print text
        content = get_url_content("http://man.linuxde.net/" + text)
        soup = BeautifulSoup(content)
        try:
            soup.find_all(id ="content-index")[0].string = ""
        except:
            pass
       
        temp0 = "".join(soup.find_all('p')[1].text.split('\n')) + "\r\n"
        temp1 = "\r\n".join(soup.find_all('pre')[0].text.split('\n')) + "\r\n"
        temp2 = "\r\n".join(soup.find_all('pre')[1].text.split('\n'))
        
        temp2 = "\r\n".join(soup.find_all('div', "post_bd post")[0].text.split('\n'))
        
        #print temp0+temp1+temp2
        
        #print 
        set_wallpaper(resource_path("a.jpg"), devide_each_line(temp2))

    except Exception as e:
        #print e
        pass
    

work_t = workthread("t1")
work_t.setDaemon(True)
if __name__ == '__main__':
    #print cur_file_dir()
    #print os.path.abspath(os.curdir)
    #print resource_path()
    read_cfg()
    top = tk.Tk()
    top.title("RangeCommand")
    labelHello = tk.Label(top, text = "当前interval:%s 秒, font size: %s" % (interval_minute_change, hanzisize), height = 2, width = 50, fg = "blue")
    labelHello.pack()
    labelHello2 = tk.Label(top, text = "输入格式：秒#大小。例如：5#10", height = 1, width = 30, fg = "blue")
    labelHello2.pack()
    
    
    entryCd = tk.Entry(top, bd =5)
    entryCd.pack(side = tk.LEFT)
    btnCal = tk.Button(top, text = "set", command = btnHelloClicked)
    btnCal.pack(side = tk.LEFT)

    #entryCd1 = tk.Entry(top, text = "0")
    #entryCd1.pack()

    entryCd1 = tk.Entry(top, bd =5)
    
    entryCd1.bind('<Key-Return>', printkey)
    entryCd1.pack(side = tk.BOTTOM) 
    btnCal1 = tk.Button(top, text = "set color", command = set_color)
    btnCal1.pack(side = tk.BOTTOM)
    


    #thread.start_new_thread(get_new_command, ("Thread-1", 2, ))
    work_t.start()
    top.iconify()
    top.mainloop()
    
    

    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
