import tkinter as tk
import requests as req
from tkinter import *
import xml.etree.ElementTree as ET
from threading import Timer
import webbrowser
import pyttsx3
import threading
import numpy
import sys
from system_hotkey import SystemHotkey

word = None
nowword = 0
engword=''

class BodyDragWindows(tk.Tk):
    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)

    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y


def getWordOfTheDayInfo():
    global word

    url = "http://www.wordthink.com"
    html = req.get(url)
    root = ET.fromstring(html.text)
    t = root.findall('h2','title')
    word = [obj.find('{http://www.w3.org/2005/Atom}title').text for obj in t]
    wordOfTheDay.set(word[0])
    setNowWordEngWord()

    """other resource"""
    # url = "http://word.eng.tw/"
    # html = req.get(url)
    # sp = BeautifulSoup(html.text, 'html.parser')
    # date = sp.select("#Blog1")
    # word = date[0].find_all('h3', {'class': 'post-title entry-title'})
    # wordoftheday.set(word[0].text)

def autoNextWord():
    threading.Timer(600.0, autoNextWord).start()
    nextWord()

def nextWord(event = None):
    global nowword, wordOfTheDay, word
    nowword += 1
    if nowword > len(word) -1:
        nowword = 0

    wordOfTheDay.set(word[nowword])
    setNowWordEngWord()

    # wordoftheday.set(word[nowword].text)

def lastWord(event = None):
    global nowword, wordOfTheDay, word
    nowword-=1
    if nowword <0:
        nowword =0

    wordOfTheDay.set(word[nowword])
    setNowWordEngWord()

    # wordoftheday.set(word[nowword].text)

def setNowWordEngWord():
    global nowword, word, engword
    wordre = re.compile('[A-Za-z]+')
    engword = wordre.match(word[nowword]).group()
    # engword = word[nowword]

def tryGetWordOfTheDayInfo():
    try:
        # getWordOfTheDayInfo()

        getWordOfTheDayInfoFromLocalFile()
    except:
        wordOfTheDay.set('Get Information Fail')
        t = Timer(30.0, tryGetWordOfTheDayInfo)
        t.start()


def getWordOfTheDayInfoFromLocalFile():
    global word
    f = open("All Decks.txt", "rt", encoding="utf-8")
    fl = f.readlines()
    for index,w in enumerate(fl):
        warry = w.split("</div> <div>")
        w = warry[0]
        cleanr = re.compile('<.*?>')
        fl[index] = re.sub(cleanr, '', w)
        fl[index] = fl[index].replace('\t', " ")
        fl[index] = fl[index].replace('\n', "")


    numpy.random.shuffle(fl)
    word = fl
    wordOfTheDay.set(word[0])
    setNowWordEngWord()



def searchImage():
    global engword
    url="https://www.google.com.tw/search?q={}&source=lnms&tbm=isch&sa=X&biw=1280&bih=591&dpr=1.5".format(engword)
    openBrowser(url)

"""spech library is not working now"""
# def SpeechThread():
#     global engword
#     engine = pyttsx3.init()
#     engine.say(engword)
#     engine.runAndWait()
#
# def Speech():
#     listenclipboard = threading.Thread(target=SpeechThread, args=())
#     listenclipboard.start()

# def Speech():
#     global engword
#     engine = pyttsx3.init()
#     engine.say(engword)
#     engine.runAndWait()

def search():
    global engword
    url="https://www.google.com.tw/search?q={}&sourceid=chrome&ie=UTF-8".format(engword)
    openBrowser(url)

def openBrowser(url):
    webbrowser.open(url, new=0, autoraise=True)
    # webbrowser.open_new(url)
    # webbrowser.open_new_tab(url)

win = BodyDragWindows()

win.configure(background='#0e285e')
win.geometry("+997+574")
wordOfTheDay=tk.StringVar()
englishlabel = tk.Label(win, textvariable=wordOfTheDay, font=("微軟正黑體", 16), padx=20, pady=10, fg="#FFFFFF", bg='#0e285e')
englishlabel.grid(row=0, columnspan=5)

upbtn = tk.Button(win, text="<", relief=FLAT, fg="#FFFFFF", bg='#0e285e', bd=0, width=5, command=lastWord)
upbtn.grid(row=1, column=0, sticky='w')

nextbtn = tk.Button(win, text=">", relief=FLAT, fg="#FFFFFF", bg='#0e285e', bd=0, width=5, command=nextWord)
nextbtn.grid(row=1, column=4, sticky='e')

appName = tk.Label(win, text="Word of the day", font=("微軟正黑體", 8), padx=20, pady=10, fg="#FFFFFF", bg='#0e285e')
appName.grid(row=2, columnspan=5)

#python去背圖顯示需再研究
# searchimg = ImageTk.PhotoImage(file="image/search.png")
# imageimg = ImageTk.PhotoImage(file="image/gallery.png")

searchbtn = tk.Button(win, text='search', relief=FLAT, fg="#FFFFFF", bg='#0e285e', bd=0, width=5, command=search)
searchbtn.grid(row=1, column=1)
# searchbtn.config(image=searchimg)

searchimagebtn = tk.Button(win, text='searchimage', relief=FLAT, fg="#FFFFFF", bg='#0e285e', bd=0, width=12, command=searchImage)
searchimagebtn.grid(row=1, column=2)

# speechbtn = tk.Button(win, text='speech',relief=FLAT, fg="#FFFFFF", bg='#0e285e', bd=0, width=5, command=Speech)
# speechbtn.grid(row=1, column=3)
# searchimagebtn.config(image=imageimg)

win.lift()
win.call('wm', 'attributes', '.', '-topmost', '1')
win.overrideredirect(True)
win.bind('<Left>', lastWord)
win.bind('<Right >', nextWord)
tryGetWordOfTheDayInfo()

# hk = SystemHotkey()
# hk.register(('control'), callback=lambda:sys.exit(0))

autoNextWord()

win.mainloop()



