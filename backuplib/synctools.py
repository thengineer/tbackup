'''
Created on 11.03.2012

@author: Jakob
'''
# python standard libs
import  os.path, shutil

# backup tools extras
from backuplib.filefoldertree import *
from backuplib.helpertools import get_size, sort_tree_by_inode


def build_treedata(rootdir):
	''' return lists of files and list of folders'''
	
	files = []
	folders = []
	rdlen = len(rootdir)
	for root, _, fs in os.walk(rootdir):
		folders.append(Folder(root[rdlen:], root))
		
		for f in fs:
			#relative path to file or folder
			files.append(File(os.path.join(root, f)[rdlen:], os.path.join(root, f)))
				
	return [files, folders]


def find_added_renamed_modified_unchanged(c, b, paths):
	''' return a list (of inode-IDs from the backup)
		of missing files in the original (=current state)
	
	'''
	
	added = []
	renamed = []
	modified = []
	unchanged = []

	fbs = sort_tree_by_inode(b)
	for f_c in c:
		if f_c.inode in fbs.keys():
			if fbs[f_c.inode].modified != f_c.modified or fbs[f_c.inode].size != f_c.size:
				modified.append(f_b.inode)
				f_c.SetPaths(paths['live'], paths['newbak'])
				
			elif fbs[f_c.inode].path != f_c.path:
				renamed.append(f_b.inode)
				f_c.SetPaths(paths['oldbak'], paths['newbak'], fbs[f_c.inode].path_rel)
			else:
				unchanged.append(f_c.inode)
				f_c.SetPaths(paths['oldbak'], paths['newbak'])
			break	
				
		else:
			# file couldn't be found
			added.append((f_c.inode))
			f_c.SetPaths(paths['live'], paths['newbak'])

	return [c, added, renamed,  modified, unchanged]		


def find_added_renamed_modified_unchanged_____________________orig(c, b, paths):
	''' return a list (of inode-IDs from the backup)
		of missing files in the original (=current state)
	
	'''
	
	added = []
	renamed = []
	modified = []
	unchanged = []

	for f_c in c:
		for f_b in b:
			if f_b.inode == f_c.inode:
				# file is still there
				if f_b.modified != f_c.modified or f_b.size != f_c.size:
					modified.append(f_b.inode)
					f_c.SetPaths(paths['live'], paths['newbak'])
					
				elif f_b.path != f_c.path:
					renamed.append(f_b.inode)
					f_c.SetPaths(paths['oldbak'], paths['newbak'], f_b.path_rel)
				else:
					unchanged.append(f_b.inode)
					f_c.SetPaths(paths['oldbak'], paths['newbak'])
				break
				
		else:
			# file couldn't be found
			added.append((f_c.inode))
			f_c.SetPaths(paths['live'], paths['newbak'])

	return [c, added, renamed,  modified, unchanged]		


def get_inodes_as_list(c, paths):
	''' return all file or folder inodes as list '''
	import gc
	gc.disable()
	for f in c:
		#inodes.append(f.inode)
		f.SetPaths(paths['live'], paths['newbak'])
	inodes = [f.inode for f in c]
		
#	print('DBG: done with .SetPaths, now making inode list, length: {}'.format(len(c)))
	
#	inodes = []
#	i = 0
##	import time
##	t0 = time.time()
#	
#	
#	for f in c:
#		inodes.append(f.inode)
		
	gc.enable()
#	print('DBG: gc.enable called.')
	return [c, inodes]


def copy_folders_only(src, dest):
	''' copy a whole folder tree without files '''
	
	try:
		shutil.rmtree(dest)
	except WindowsError:
		pass
	shutil.copytree(src, dest, ignore=ignore_files)



def batch_duplicate_files(filetree, inodes, copy=True, verbose=False):
	''' duplicate (link or copy) a number of files'''
	from backuplib.progressstatus import ProgressStatus
	status = ProgressStatus(len(inodes), get_size(filetree, inodes))
	
	# FIXME: if hardlinks exist in the source, they wont be copied!
	filetree_sorted = sort_tree_by_inode(filetree)
	
#	for file in filetree:
#		for inode in inodes:
#			if file.inode == inode:
#				src = file.path_src
#				dst = file.path_dst

	for i in inodes:
		src = filetree_sorted[i].path_src
		dst = filetree_sorted[i].path_dst
		duplicate_file(src, dst, copy, verbose, status, filetree_sorted[i].size)
	
	
def duplicate_file(src, dst, copy, verbose, status, size):
	''' actually copy or link the file '''
	
	if verbose == True:
		print('{} >> {}'.format(src, dst))
	if copy == False:
		os.link(src, dst)
	else:
		status.update(src, size)
		shutil.copy2(src, dst)
	
	

def ignore_files(path, names):
	''' helper function for copy_folders_only() to not copy any files '''
	
	files = []
	for name in names:
		fullpath = os.path.join(path, name)
		if os.path.isfile(fullpath):
			files.append(name)
			
	files.append('System Volume Information')
	files.append('$RECYCLE.BIN')
	return files



def filter_filesfolders(filter_names, filter_paths, tree):
	''' return a inode list (and maybe tree list too) which doesnt 
		contain any files or folders that shall be excluded from backup '''
	import re
	
	tree_filtered = []
	
	for f in tree:
		if re.search(filter_names, f.name) == None and re.search(filter_paths, f.path) == None:
			# then no filter matched, so we can include it into the backup
			tree_filtered.append(f)
#		else:
#			print('     {} was filtered out.'.format(f.path))
	return tree_filtered
			
	
	pass