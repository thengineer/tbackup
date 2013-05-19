'''
Created on 18.03.2012

@author: Jakob
'''
import threading

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
#app = MyTkApp()
#print('now can continu')

class ProgressGui(threading.Thread):
	def __init__(self, totalfiles, totalbytes):
		threading.Thread.__init__(self)
		self.start()
		
		self.create_gui()
		self._total_bytes = totalbytes
		self._total_files = totalfiles
		self._done_bytes = 0
		self._done_files = 0
		
	def callback(self):
		print('GUI has been closed..')
		#self.root.quit()
		
	def create_gui(self):
		import tkinter.ttk
		from backuplib.helpertools import convert_bytes
		
		root = tkinter.Tk()
		
		root.title('Backup Progress...')
		root.iconbitmap('./icon.ico')
		
		#
		# progres
		progressframe = tkinter.ttk.LabelFrame(root, borderwidt=2, relief='groove', text='Progress' )
		progressframe.grid(column=1, row=1, sticky='n')
		
		lbl_files = tkinter.ttk.Label(progressframe, text="Files: 38 / 1204")
		lbl_files.pack(anchor='w')
		
		pbar_files = tkinter.ttk.Progressbar(progressframe, length=400, value=30)
		pbar_files.pack(anchor='w')
		
		lbl_bytes = tkinter.ttk.Label(progressframe, text="Bytes: 38 / 1204")
		lbl_bytes.pack(anchor='w')
		
		pbar_bytes = tkinter.ttk.Progressbar(progressframe,  length=400, value=20)
		pbar_bytes.pack(anchor='w')
		
		
		#
		# post/backup action selector
		postframe = tkinter.LabelFrame(root, borderwidt=2, relief='groove',text='Post-Backup action' )
		postframe.grid(column=2, row=1)
		
		pb_action = tkinter.IntVar()
		
		rbtn1 = tkinter.ttk.Radiobutton(postframe, text='Do nothing', state='active', var=pb_action, value=1)
		rbtn1.pack(anchor='w')
		rbtn2 = tkinter.ttk.Radiobutton(postframe, text='Shut down', state='active', var=pb_action, value=2)
		rbtn2.pack(anchor='w')
		rbtn3 = tkinter.ttk.Radiobutton(postframe, text='Standby', state='active', var=pb_action, value=3)
		rbtn3.pack(anchor='w')
		rbtn4 = tkinter.ttk.Radiobutton(postframe, text='Hibernate', state='active', var=pb_action, value=4)
		rbtn4.pack(anchor='w')
		
		self.root = root
		
	def go(self):
		self.root.mainloop()
	

if __name__ == '__main__':
	
	gui = ProgressGui(10,1024)
	#gui.mainloop()
	print('hello')
	gui.go()
