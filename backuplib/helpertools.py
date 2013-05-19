'''
Created on 12.03.2012

@author: Jakob
'''
def convert_bytes(bytes):
	''' taken from: http://www.5dollarwhitebox.org/drupal/node/84 '''
	
	bytes = float(bytes)
	if bytes >= 1099511627776:
		terabytes = bytes / 1099511627776
		size = '%.2fT' % terabytes
	elif bytes >= 1073741824:
		gigabytes = bytes / 1073741824
		size = '%.2fG' % gigabytes
	elif bytes >= 1048576:
		megabytes = bytes / 1048576
		size = '%.2fM' % megabytes
	elif bytes >= 1024:
		kilobytes = bytes / 1024
		size = '%.2fK' % kilobytes
	else:
		size = '%.2fb' % bytes
	return size

def print_paths(flist, inodes=True):
	''' print the paths that belong to the corresponding inodes '''
	# TODO: use sort_tree_by_inode()
	
	if inodes == True:
		for f in flist:
			print('    {}'.format(f.path))
	else:
		for f in flist:
			for i in inodes:
				if f.inode == i:
					print('    {}'.format(f.path))
					
					
def print_action_summary(files_list_current, inodes_added, inodes_renamed, inodes_modified, print_details=False):
	''' print a list of files that were removed, renamed, ... '''
	
	print('  > files to be added: {} ({})'.format(len(inodes_added), convert_bytes(get_size(files_list_current, inodes_added))))
	if print_details == True:
		print_paths(files_list_current, inodes_added)
	
	print('  > files to be renamed: {}'.format(len(inodes_renamed)))
	if print_details == True:
		print_paths(files_list_current, inodes_renamed)
	
	
	print('  > files to be modified: {}'.format(len(inodes_modified)))
	if print_details == True:
		print_paths(files_list_current, inodes_modified)
	
def check_dupes(a):
	# TODO: make a more informative one
	
	
	if len(set(a)) != len(a):
		print('WARNING: there is a duplicate!!')
		
		

def store_treedata(what, where):
	import pickle
	
	pickle.dump(what, open(where,'wb'))
	
def load_treedata(where):
	import pickle
	
	return pickle.load(open(where,'rb'))


def get_size(flist, inodes=False):
	''' return of total bytes of files in flist with optional inode in inodes
	'''
	total = 0
	if inodes == False:
		for f in flist:
			total += f.size
	else:
		sfl = sort_tree_by_inode(flist)
		for i in inodes:
			total += sfl[i].size
	return total


def sort_tree_by_inode(flist):
	''' return a dictionary that has f.inode as key and f as value
		(used to speed up queries) '''
	
	sfl = dict()	# sorted file list
	
	for f in flist:
		sfl[f.inode] = f
		
	return sfl


def walktest(rootdir):
	import os
	for root, _, _ in os.walk(rootdir):
		print(root)
		
		