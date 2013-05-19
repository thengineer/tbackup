'''
filefoldertree.py

this provides classes to represent folders and files 

Created on 11.03.2012

@author: Jakob
'''

import os


class Folder():
	''' Folder() can contain folders and files
		represented as Folder() objects in self.subfolders
		and File() objects in self.files
		
	'''
	def __init__(self, fr, fa):
		
		s = os.stat(fa)
		
		
		self.name = os.path.basename(fa)
		self.path = fr # contain relative path to file/folder (including name itself)
		self.inode = s.st_ino
		#self.islink = False	# TODO: determine somehow
		self.isfile = False
		
		
class File(Folder):
	''' File() represents a file. '''
	
	def __init__(self, fr, fa):
		Folder.__init__(self, fr, fa)
		
		s = os.stat(fa)
		
		self.size = s.st_size
		self.modified = s.st_mtime
		#self.checksum = '' # TODO: eventually also add a checksum. but usually not needed..
		self.isfile = True
		self.path_rel = fr
		

		
		
	def SetPaths(self, s, d, src_path_rel=False):
		#print('DEBUG: SetPaths() called.')
		# this is the full path (incl. name) to enable easy copying and linking
		if src_path_rel == False:
			# sometimes (if file was renamed, the src path is not the live path, but the one from the backup)
			self.path_src = os.path.join(s, self.path_rel)
		else:
			self.path_src = os.path.join(s, src_path_rel)
			
		self.path_dst = os.path.join(d, self.path_rel)
		
