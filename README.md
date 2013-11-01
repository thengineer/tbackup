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
