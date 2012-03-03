#!/usr/bin/python
#
#       portupd.py - daemon for auto sychronization of portage tree
#       Copyright (C) 2012 Kevin Brandstatter
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

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

      print self.conf.get('no_daemon')
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
