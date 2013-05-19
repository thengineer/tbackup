'''
Created on 25.03.2012

@author: Jakob
'''

import backuplib.backuproutines
import config

backuplib.backuproutines.multibackup(config.program_config, config.backups, initial=True, dryrun=False)

# console window shouldnt be closed automatically
input('hit ENTER to close.')