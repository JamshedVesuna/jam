jam
===

File Syncing Done Right.

Background
----------
For the most part, almost all of my main files are on my Dropbox. On a daily basis, I don't use every file or every directory, but my entire Dropbox is synced with every computer (They do have an option to sync only certain directories). Most laptops now-a-days come with 128 or 258 gigs of storage, and an increasing percentage of this is being used up by heavy applications (Adobe products, System files, Virtual Machines, other content producing apps).

Let's say on a daily basis, I have one or two active working directories. On a weekly basis, I explore 5 or 6 directories, and on a monthly basis I explore 10 to 20 top level directories.

Most people use Dropbox as a backup system, syncing system, and (somewhat poor) version control.

Solution
--------

On a daily basis, I don't want to have my entire Dropbox synced on every computer, only a small subset of my working directories. Only store these locally. With some smart algorithm, sync files that are related to the files I'm looking at (file extension, file type, file name, and close relative working dirs). Cache files I might potentially want, but store the entire directory structure locally so I have a roadmap of my files without using up space. When I explore a dir outside of my daily/weekly working dir, sync that dir and dirs like it. Similarly, be able to "checkout" directories, commit files and dirs manually as well as have a automatic sync.

Version Control
---------------
(Version controll has been pushed back in terms of priority)

* Just like git, you can commit files and directories manually, however, with or without a commit message. In the background, your working files and directories are committed automatically (either every x minutes, on every 'important' change, or on every write).
* Diff Syncing

The Right Files When You Need Them
----------------------------------
* The Algorithm: LRU (naive)
* Keep Backups Off My Laptop: Old media and files I rarely touch should be stored on a more secure and reliable server, not my laptop.

Distributed File System
-----------------------

* Server Caching: I can daisy chain multiple servers together or even put them in parallel to act as RAID mirroring. This allows me to bundle multiple drives or servers together and make them act as a single device. "I don't care which drive my files are on as long as I have access to them"
* Edge Caching: Further down the road, you could have your "daily" files stored locally, your "weekly" files stored at the edge, and all your files stored far away on some server. This lets you quickly access files that you probably use more often than files that are mere backups. My local laptop has my daily working directory. A close server has my daily and weekly working directory, and a distant server has all of my files (including backups)


Pros
----
* Uses far less disk space, if your Dropbox is 100 gigs, you probably only use a small fraction of that daily, no need to store it all at home. Adds the ability to have a huge backup and working dirs intermingled and stored safely on some server. Adds git's ability of version control as well as automatic backups just in case. Local cache of similar files allows for a quicker sync of files (only sync the diff). Ability to move files and change dir structure without actually touching the files themselves (esp if they are very large files)

Cons
----
* Potential latency when accessing files. Can't access certain files without a network connection (but you can still explore their dir structure and move files, etc).


Naive
-----

1. Get a dir structure of your working dir
2. Using LRU, take the bottom 75%
3. Replace each file with a pointer to that file on the remote server (ssh://) and maybe some meta data. This will be mannual at first
4. Use 'checkout' to pull a file or all the contents of a dir locally using each pointer
Look at Fuse api to make 'stat' available. The file shows its proper size but isn't actually there

Eventually: run a python server locally and remotely to keep things updated.

Usage
-----
1. Use `stash.py` and `checkout.py` for stash and checkout.
2. For now, fill out the following information in __init__ in both files (This will change with added functionality):
    * self.HOSTPwd: the full pwd of the jam repo clone
    * self.RemoveServer: the remote host
    * self.RemoteUser: the remote user
    * self.RemotePwd: the full pwd of the remote directory where files will be stored (on self.REMOTEServer)
3. In get_sftp_client, fill out the password in `transport.connect` for the remote host
4. You should be able to stash and checkout any file that's in the same dir as `jam/`:
    * `python stash.py pg100.txt`
    * `python checkout.py pg100.txt`

Let me know if you have any trouble with this.


To Do
-----
* Files and directories
* Files/dirs from any path
* Build cli for mannual stash / checkout
* Build daemon using pyinotify to automatically stash / checkout
    * Ability to set time thresholds (Stuff older than 10 minutes, stash)
    * Ability to set server locations and bundle devices
    * Add meta data times to dirstruct
