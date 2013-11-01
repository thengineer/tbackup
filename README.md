tbackup
=======

thengineer's backup tool.

Yet another backup tool written in Python. This one creates snapshots of the backup source and uses hardlinks to save space.

Features
------------

* create folders for each snapshot
* use hardlinks for unchanged files
* detect if a file was renamed/moved
* exclude files and folders with regex matching



Usage
---------
modify `config.py` to set up your backup stuff. and if needed change `backup.py` to your taste.


Screenshot
-----------

	D:\misc\coding\python\tbackup>python3 backup.py
	> preparing backup source MA
	  > firstrun flag was set.
	  > loading tree from current state
	  > not filtering files because no config was provided
	  > creating inode list
	  > files to be added: 1140 (1.66G)
	  > files to be renamed: 0
	  > files to be modified: 0
	  > copy file tree
	> preparing backup source ADCPtool-MA
	  > firstrun flag was set.
	  > loading tree from current state
	  > not filtering files because no config was provided
	  > creating inode list
	  > files to be added: 497 (29.58M)
	  > files to be renamed: 0
	  > files to be modified: 0
	  > copy file tree
	> copying files
	 done:  63.46%, left:  631.27M, speed:    7.17M/s, probably finished at: 12:33
