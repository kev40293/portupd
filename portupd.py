#!/usr/bin/python

import portage, sys, time;
from portage import os;
import _emerge.main;
from _emerge.main import *;

options = ["-d", "--daemon"];
env = {}

last_sync = 0;

def runTest():
   args=["--help"];
   timeout = 1.0;
   global last_sync
   while 1:
      thetime=time.time();
      if thetime-last_sync > timeout or last_sync==0:
         last_sync = thetime;
         _emerge.main.emerge_main(args);
      time.sleep(10);


def parseArgs(args):
   global env
   for i in args:
        if i == "-d":
           env['daemon'] = True;

def portupd_main(args):
   if (os.geteuid() != 0):
      print "Must be run as root";
      runTest();
      sys.exit();

   parseArgs(sys.argv);

   os.setpgid(0,0);
   if (env.get('daemon') == True):
      print "forking to background"
      if (os.fork() == 0):
          fd = os.open("/dev/null", os.O_WRONLY);
          os.dup2(fd,1);
          os.close(fd);
          syncopt = ["--help"];
          _emerge.main.emerge_main(syncopt);
#args = ["-D", "-u", "-p", "-N", "world"];
#_emerge.main.emerge_main(args);

portupd_main(sys.argv);
