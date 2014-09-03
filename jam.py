"""Better file syncing"""

import ConfigParser
import os
import paramiko
import pickle
import subprocess
import sys

from os import listdir, walk
from paramiko import SSHClient

class Jam():

    def __init__(self):
        credDict = self.get_credential_dict()
        self.HOSTPwd = credDict['hostpwd']
        self.REMOTEServer = credDict['remoteserver']
        self.REMOTEPort = int(credDict['remoteport'])
        self.REMOTEUser = credDict['remoteuser']
        self.REMOTEPwd = credDict['remotepwd']
        self.REMOTEPassword = credDict['remotepassword']
        self.REMOTEFull = (self.REMOTEUser + '@' + self.REMOTEServer + ":" +
            self.REMOTEPwd)
        self.dirstruct = self.get_dirstruct()
        self.get_current_dirstruct()
        self.sftp = self.get_sftp_client(self.REMOTEServer)

    def get_credential_dict(self):
        try:
            credDict = pickle.load(open("creds.pickle", 'rb'))
        except IOError:
            credDict = self.parse_credential_cfg()
        return credDict

    def parse_credential_cfg(self):
        Config = ConfigParser.ConfigParser()
        Config.read("credentials.cfg")
        credDict = {}
        for section in Config.sections():
            options = Config.options(section)
            for option in options:
                credDict[option] = Config.get(section, option)
        return credDict

    def get_sftp_client(self, remote):
        """Returns an paramiko sftp object. Assumes local ssh keys are valid

        :param remote: the remote server
        """
        paramiko.util.log_to_file("filename.log")
        transport = paramiko.Transport((self.REMOTEServer, self.REMOTEPort))
        transport.connect(username=self.REMOTEUser,
            password=self.REMOTEPassword)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp

    def put_file(self, local_path, remote_path):
        """Using ftp, put a file from local_path to remote_path"""
        self.sftp.put(local_path, remote_path)

    def get_file(self, remote_path, local_path):
        """Using ftp, get a file from the remote and copy it locally"""
        self.sftp.get(remote_path, local_path)

    def get_dirstruct(self):
        """Returns access to dirstruct, a pickle repr of our working dir"""
        try:
            dirstruct = pickle.load(open("dirstruct.pickle","rb"))
        except IOError as e:
            empty = {}
            pickle.dump(empty, open("dirstruct.pickle","wb"))
            dirstruct = pickle.load(open("dirstruct.pickle","rb"))
        return dirstruct

    def get_current_dirstruct(self):
        """Returns a json object repr the current dir structure

        Not yet functional
        """
        dirstruct = {}
        excludeDirs = ['.git']
        i = 0
        for root, dirs, files in walk(self.HOSTPwd):
            #print dirs
            #print files
            for exclude in excludeDirs:
                if exclude in dirs:
                    dirs.remove(exclude)
                #else:
                    #dirstruct
        #print dirs
        return dirstruct

    def get_head(self, file):
        """Return the first len(REMOTEFull) bytes of a file given the path"""
        chars =  repr(open(file, 'rb').read(len(self.REMOTEFull)))
        return chars[1:len(chars)-1]

    def stash(self, local_file, remote_file):
        """Push the file from local to remote (full path)

        Replace the local file with raw text as follows:
        user@host:/full/path/to/file
        :param local_file: full path to local file
        :param remote_file: full path to remote file
        """
        if self.get_head(local_file) == self.REMOTEFull:
            # The file has already been stashed
            return
        self.put_file(local_file, remote_file)
        remote_full = (self.REMOTEUser + "@" + self.REMOTEServer + ":" +
            remote_file)
        open_local_file = open(local_file, "w")
        subprocess.Popen(['echo', str(remote_full)], stdout=open_local_file)

    def checkout(self, local_file):
        """Replace the pointer with the actual file"""
        if self.get_head(local_file) != self.REMOTEFull:
            # The file has already been checked out
            return
        remote_file = open(local_file, "r").read().splitlines()[0].split(":")[1]
        self.get_file(remote_file, local_file)
