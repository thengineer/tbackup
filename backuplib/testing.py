import tkinter
import threading
import time

class MyTkApp(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    def callback(self):
       print('bye!')
       self.root.quit()
    def run(self):
        self.root=tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.s = tkinter.StringVar()
        self.s.set('Foo')
        l = tkinter.Label(self.root,textvariable=self.s)
        l.pack()
        self.root.mainloop()
app = MyTkApp()
print('now can continue running code while mainloop runs')

time.sleep(5)

app.s.set('modified you!')