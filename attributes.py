#!/usr/bin/env python3

#
#
#

import os
import fileinfo

def getFileInfo(filename):
  
  fileObj = fileinfo.FileInfo(filename)
  
  fileObj.updatePathInfo()
  fileObj.getAttrs()
  fileObj.calcHashes()
  
  return(fileObj)

def main(filename):
  print(getFileInfo(filename))

if __name__ == '__main__':
  import argparse
  
  parser = argparse.ArgumentParser(description='N/A')
  
  parser.add_argument("filename", action="store")

  results = parser.parse_args()

  if not os.path.isfile(results.filename):
    print("Error:", os.path.abspath(results.filename), "does not exist!")
    sys.exit(-1)

  #!print()
  #!print("filename      = ", results.filename)
  #!print()

  main(results.filename)

