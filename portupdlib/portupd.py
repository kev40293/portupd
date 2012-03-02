#!/usr/bin/python

import portage, sys, time;
from portage import os;
import _emerge.main;
from _emerge.main import *;
import signal;

class portupd(object):
   conf = None
   def __init__(self, environment):
      self.conf = environment
      pidfile = open(self.conf.get('pid_file'), 'w')

      if (self.conf.get('no_daemon') == False):
         print "forking to background"
         if (os.fork() == 0):
             os.setpgid(0,0);
             pidfile.write(str(os.getpid()));
             pidfile.close();
             fd = os.open("/dev/null", os.O_WRONLY);
             os.dup2(fd,1);
             os.close(fd);
             #self.main_loop()
         else:
            sys.exit()

      else:
           print "Keeping in foreground"
           pidfile.write(str(os.getpid()));
           pidfile.close();
           #self.main_loop();
   def quit(self):
      os.remove(self.conf.get('pid_file'))

   def main_loop(self):
         last_sync = 0
         period = self.conf.get('time') * 60 * 60
         delay = self.conf.get('wait') * 60
         time.sleep(delay)
         while 1:
            cur_time = time.time()
            if cur_time - last_sync > delay:
               if _emerge.main.emerge_main(['--sync']) == 0:
                  last_sync = cur_time
               else:
                  time.sleep(delay)
