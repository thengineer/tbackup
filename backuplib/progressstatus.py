'''
Created on 25.03.2012

@author: Jakob
'''
#from _dummy_thread import error
import time
from backuplib.helpertools import convert_bytes
import backuplib.progressgui


class ConsoleFE():
	def update(self, d):
		print('\r done: {:>7.2%}, left: {:>8}, speed: {:>8}/s, probably finished at: {}'.format(
					d['pdone_bytes'],
					convert_bytes(d['bytes_todo']),
					convert_bytes(d['bytes_per_second']),
					time.strftime('%H:%M', d['time_finished'])
					), end='')
	
class tkinterFE(backuplib.progressgui.ProgressGui):
	def __init__(self, totalfiles, totalbytes):
		backuplib.progressgui.ProgressGui.__init__(self, totalfiles, totalbytes)



class ProgressStatus():
	def __init__(self, totalfiles=0, totalbytes=0, fe=0):
		
		self.files_total = totalfiles
		self.files_done = 0
		self.bytes_total = totalbytes
		self.bytes_done = 0
		self.t_started = time.localtime()
		
		
		
		if fe == 0:
			# raw console front end
			self.fe = ConsoleFE()
		else:
			#FIXME: make a real python error 
			print('EROR: unknown FE type')
		
	def update(self, filename, size):
		
		
		pdone_files = self.files_done / self.files_total
		pdone_bytes = self.bytes_done / self.bytes_total
		
		bytes_per_second =  self.bytes_done / (time.time() - time.mktime(self.t_started))
		
		bytes_todo = self.bytes_total - self.bytes_done
		
		try:
			seconds_todo = bytes_todo / bytes_per_second
		except ZeroDivisionError:
			seconds_todo = 0
		
		time_finished = time.localtime(seconds_todo + time.time())
		
		self.fe.update({'pdone_files':pdone_files,
					'pdone_bytes':pdone_bytes,
					'bytes_per_second':bytes_per_second, 
					'bytes_todo':bytes_todo,
					'seconds_todo':seconds_todo,
					'time_finished':time_finished
					 })
		
		
		self.files_done += 1
		self.bytes_done += size