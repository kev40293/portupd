#!/usr/bin/python

import portage, sys, time;
from portage import os;
import _emerge.main;
from _emerge.main import *;


if (os.geteuid() != 0):
   print "Must be run as root";
   sys.exit();

os.setpgid(0,0);
if (os.fork() == 0):
   fd = os.open("/dev/null", os.O_WRONLY);
   os.dup2(fd,1);
   os.close(fd);
   syncopt = ["--help"];
   _emerge.main.emerge_main(syncopt);
   while 1:
        time.sleep(20);
#args = ["-D", "-u", "-p", "-N", "world"];
#_emerge.main.emerge_main(args);
