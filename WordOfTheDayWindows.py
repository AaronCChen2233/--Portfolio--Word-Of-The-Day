import tkinter as tk
import requests as req
from bs4 import BeautifulSoup
from tkinter import *

word = None
nowword = 0

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

def GetWordOfTheDayInfo():
    global word
    url = "http://word.eng.tw/"
    html = req.get(url)
    sp = BeautifulSoup(html.text, 'html.parser')
    date = sp.select("#Blog1")
    word = date[0].find_all('h3', {'class': 'post-title entry-title'})
    wordoftheday.set(word[0].text)

def nextword(event = None):
    global nowword, wordoftheday,word
    nowword+= 1
    if nowword >9:
        nowword=9

    wordoftheday.set(word[nowword].text)

def upword(event = None):
    global nowword, wordoftheday, word
    nowword-=1
    if nowword <0:
        nowword =0

    wordoftheday.set(word[nowword].text)

win = BodyDragWindows()
win.configure(background='#0e285e')
win.geometry("+997+574")
wordoftheday=tk.StringVar()
englishlabel = tk.Label(win, textvariable=wordoftheday, font=("微軟正黑體", 16), padx=20, pady=10, fg="#FFFFFF", bg='#0e285e')
englishlabel.grid(row=0, columnspan=2)

nextbtn = tk.Button(win, text=">", relief=FLAT, fg="#FFFFFF", bg='#0e285e', bd=0, width=5, command=nextword)
nextbtn.grid(row=1, column=1, sticky='e')
upbtn = tk.Button(win, text="<", relief=FLAT, fg="#FFFFFF", bg='#0e285e', bd=0, width=5, command=upword)
upbtn.grid(row=1, column=0, sticky='w')

win.lift()
win.call('wm', 'attributes', '.', '-topmost', '1')
win.overrideredirect(True)
win.bind('<Left>', upword)
win.bind('<Right >', nextword)
GetWordOfTheDayInfo()
win.mainloop()



