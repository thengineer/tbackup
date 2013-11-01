'''
Created on 12.03.2012

@author: Jakob
@summary: holds the backup configuration for the runtime
'''

import os.path

backup_default = dict(
			bak_name = 'personal backup',
			bak_destination = 'u:\\bak\\hlbackup',
			bak_sources = [
						dict(name='daten', path='D:/'),
						dict(name='Desktop', path='C:/Users/Jakob/Desktop'),
						dict(name='AppData', path='C:/Users/Jakob/AppData'),
						],
			exclude_names = r'^$',	# matches only file or folder names
			exclude_paths = r'Torrent|torrent|^tmp$|^temp$|System Volume Information|pulp|RECYCLE.BIN'		# matches relative path of files or folders
			)

backups_testing = dict(
			bak_name = 'demo backup',
			bak_destination = 'D:\\temp\\backtarget',
			bak_sources = [
						dict(
							name='demo',
							path='D:/temp/backsource')
						],
			exclude_names = r'.tmp$|.temp$',	# matches only file or folder names
			exclude_paths = r'tmp$|temp$'		# matches relative path of files or folders
			)

backups = backup_default

program_config = dict(
					settings_folder = os.path.join(os.path.expanduser('~'),'.config','hlbackup'),
					datefolder_format = '%Y%m%d_%H%M%S',
					pickle_format = 'filefoldertree_{}.pkl'
					)