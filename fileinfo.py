#!/usr/bin/env python3

import os
import hashlib
import time

class FileInfo:
  """A file info class"""
  
  def __init__(self, path):
    self.path = os.path.abspath(path)
    
    # filename
    self.parent = None
    self.directory = None
    self.fullFilename = None
    self.filename = None
    self.extension = None
    self.type = None
    
    # os.stat
    self.inode = None
    self.size = None
    self.atime = None
    self.mtime = None
    self.ctime = None
    
    # checksums
    self.sha1sum = None
    self.sha256sum = None
    
    # db
    self.index = None
    self.tags = []

  def __repr__(self):
    return "{} - inode = {}".format(self.path, self.inode)

  def formatTime(self, t):
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(t))

  def __str__(self):
    outStr = "Path: {}\n".format(self.path)
    outStr += "Parent: {}\n".format(self.parent)
    outStr += "Directory: {}\n".format(self.directory)
    outStr += "Full Filename: {}\n".format(self.fullFilename)
    outStr += "Filename: {}\n".format(self.filename)
    outStr += "Extension: {}\n".format(self.extension)
    outStr += "Type: {}\n".format(self.type)
    outStr += "Inode: {}\n".format(self.inode)
    outStr += "Size (Bytes): {}\n".format(self.size)
    outStr += "Access Time: {}\n".format(self.formatTime(self.atime))
    outStr += "Modification Time: {}\n".format(self.formatTime(self.mtime))
    outStr += "Creation Time: {}\n".format(self.formatTime(self.ctime))
    outStr += "SHA1 sum: {}\n".format(self.sha1sum)
    outStr += "SHA256 sum: {}\n".format(self.sha256sum)
    outStr += "Database Index: {}\n".format(self.index)
    outStr += "Database Tags: {}\n".format(self.tags)
    return outStr

  def updatePathInfo(self):
    self.directory, self.fullFilename = os.path.split(self.path)
    self.parent = os.path.dirname(self.directory)
    self.filename, self.extension = os.path.splitext(self.fullFilename)
  
  def updateAttrs(self, stat):
    """This function updates the stat info from a stat structure returned by os.stat())"""
    self.inode = stat.st_ino
    self.size = stat.st_size
    self.atime = stat.st_atime
    self.mtime = stat.st_mtime
    self.ctime = stat.st_ctime
  
  def getAttrs(self):
    try:
      stat = os.stat(self.path)
      self.updateAttrs(stat)
    except IOError:
      print("The file could not be opened: {0}".format(self.path))
  
  def updateHashes(self, sha1sum=None, sha256sum=None):
    if sha1sum != None:
      self.sha1sum = sha1sum
    if sha256sum != None:
      self.sha256sum = sha256sum
  
  def calcHashes(self):
    chunkSize = 1048576 # 1024 B * 1024 B = 1048576 B = 1 MB
    sha1sum = hashlib.sha1() 
    sha256sum = hashlib.sha256() 
    try:
      with open(self.path, "rb") as f:
        chunk = f.read(chunkSize)
        previousChunk = chunk
        totalRead = len(chunk)
        while chunk:
          sha1sum.update(chunk) 
          sha256sum.update(chunk) 
          previousChunk = chunk
          chunk = f.read(chunkSize)
          totalRead += len(chunk)
      if totalRead == self.size:
        self.updateHashes(sha1sum.hexdigest(), sha256sum.hexdigest())
    except IOError:
      print("The file could not be opened: {0}".format(self.path))

