'''
Created on 11.03.2012

@author: Jakob
'''

from backuplib.synctools import *
from backuplib.helpertools import *
import config, sys
#from copyreg import dict


#
# testing zone here


#
# paths
path_current = 'D:\\temp\\backuptestarea\\original'
path_backup = 'D:\\temp\\backuptestarea\\backup'


def simplebackup(path_current, path_backup):
	
	#
	# load the trees of files and folders
	[files_list_current, folders_list_current] = build_treedata(path_current)
	[files_list_bak, folders_list_bak] = load_treedata('D:\\temp\\backuptestarea\\backuptree.pickle')
	
	
	
	[inodes_added, inodes_renamed, inodes_modified, inodes_unchanged] = find_added_renamed_modified_unchanged(files_list_current, files_list_bak)
	
	print('> files to be added: {}'.format(len(inodes_added)))
	print_paths(files_list_current, inodes_added)
	
	print('> files to be renamed: {}'.format(len(inodes_renamed)))
	print_paths(files_list_current, inodes_renamed)
	
	
	print('> files to be modified: {}'.format(len(inodes_modified)))
	print_paths(files_list_current, inodes_modified)
	
	print(inodes_added, inodes_renamed, inodes_modified, inodes_unchanged)
	
	
	print('> copying folder tree')
	copy_folders_only(path_current, path_backup)
	
	
	print('> doing hardlinks')
	batch_duplicate_files(files_list_current, inodes_renamed + inodes_unchanged, path_current, path_backup, copy=False)
	
	
	print('> copy files to backup')
	batch_duplicate_files(files_list_current, inodes_added + inodes_modified, path_current, path_backup, copy=True)
	
	
	
def multibackup(program_config, backups, initial=False, dryrun=True):
	import os.path, os
	from datetime import datetime
	
	# create settings folder, if not exists
	if not os.path.exists(program_config['settings_folder']):
		os.mkdir(program_config['settings_folder'])
			
	#
	# prepare the backup process
	
	# the name of the folder that will store the today's backup content
	datefoldername = datetime.strftime(datetime.now(), program_config['datefolder_format'])
	
	# lists...
	inodes_link = []
	inodes_copy = []
	filelist = []

	
	
	for bak_src in backups['bak_sources']:
		print('> preparing backup source',bak_src['name'])
		
		# path to where the tree data is being stored
		path_to_pickle = os.path.join(program_config['settings_folder'], program_config['pickle_format'].format(bak_src['name']))
		#print(path_to_pickle)
		
		if initial == True:
			print('  > firstrun flag was set. ')
			# delete any existing pickles
			try:
				os.remove(path_to_pickle)
			except WindowsError:
				# FIXME: make this error message portable
				pass
			path_oldbak = ''
			
		else:
			try:
				print('  > loading pickle:', path_to_pickle)
				[path_oldbak, tree_files_lastbak, tree_folders_lastbak] = load_treedata(path_to_pickle)
				initial = False
			except IOError:
				initial = True
				path_oldbak = ''
				print(sys.exc_info())
				print('    pickle not found. assuming its a first run.')
				initial = True
		
		print('  > loading tree from current state')
		[tree_files_live, tree_folders_live] = build_treedata(bak_src['path'])
		
		
		# make a backup of there because the will be modified later
		# but we want to save the unmodified ones after the backup
		[tree_files_live_orig, tree_folders_live_orig] = [tree_files_live, tree_folders_live]
#		print(tree_files_live)
		
		store_treedata([tree_files_live, tree_folders_live, backups], 'treedata.pkl')
		
		# exclude some files and folders from backup progress
		if 'exclude_names' in backups.keys() and 'exclude_paths' in backups.keys():
			print('  > filtering files')
			tree_files_live = filter_filesfolders(backups['exclude_names'], backups['exclude_paths'], tree_files_live)
			print('  > filtering folders')
			tree_folders_live = filter_filesfolders(backups['exclude_names'], backups['exclude_paths'], tree_folders_live)
			print('     done filtering files and folders')
		else:
			print('  > not filtering files because no config was provided')
		
		
		# paths: needed, because we modify the treedata, so that they also contain 
		#	the actual paths of there the files come from and where they go to
		path_src = bak_src['path']
		path_newbak = os.path.join(backups['bak_destination'], datefoldername, bak_src['name'])
		#path_oldbak = os.path.join(backups['bak_destination'], datefoldername, bak_src['name'])
		
		paths = dict(live=path_src, oldbak=path_oldbak, newbak=path_newbak)
		#print(paths)
		

#		print(tree_files_live)
#		store_treedata([tree_files_live, tree_files_lastbak, paths], 'find_added_renamed_modified_unchanged.pkl')
		
		if initial == True:
			print('  > creating inode list')
			inodes_renamed = inodes_modified = inodes_unchanged = []
			[tree_files_live, inodes_added] = get_inodes_as_list(tree_files_live, paths)
		else:
			print('  > sorting out files')
			[tree_files_live, inodes_added, inodes_renamed, inodes_modified, inodes_unchanged] = \
				find_added_renamed_modified_unchanged(tree_files_live, tree_files_lastbak, paths)
		
		print('DBG: done creating inode list, next: print_action_summary')
		#TODO: check for duplicated inodes (hardlinks!)
		
		
		
		print_action_summary(tree_files_live, inodes_added, inodes_renamed, inodes_modified, print_details=False)
		
		if not dryrun:
			print('  > copy file tree')
			copy_folders_only(path_src, path_newbak)
		
		# append whats needed to the lists
		inodes_link += (inodes_renamed + inodes_unchanged)
		inodes_copy += (inodes_modified + inodes_added)
		filelist += tree_files_live
		
		if not dryrun:
			# meanwhile save pickle
			store_treedata([path_newbak, tree_files_live_orig, tree_folders_live_orig], path_to_pickle)
#		store_treedata([path_newbak, tree_files_live_orig, tree_folders_live_orig], path_to_pickle)
	
	#
	# do actual action
	if not dryrun:
		if len(inodes_link) > 0:
			print('> creating hardlinks')
			batch_duplicate_files(filelist, inodes_link, copy=False, verbose=False)
		if len(inodes_copy) > 0:
			print('> copying files')
			batch_duplicate_files(filelist, inodes_copy, copy=True, verbose=False)
	else:
		print('> skipped making backup because dryrun option was selected')
	
	print('\r> backup finished!')

	
	
	
if __name__ == '__main__':
	
	multibackup(config.program_config, config.backups, initial=False, dryrun=True)
	
	