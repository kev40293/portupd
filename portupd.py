#!/usr/bin/python

import portage, sys, time;
from portage import os;
import _emerge.main;
from _emerge.main import *;
import argparse;
import ConfigParser;
import signal;

def handler(signum, frame):
   os.remove('/var/run/portupd.pid')
   print 'Exiting'
   exit(0)

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)


parser = argparse.ArgumentParser(prog="portsyncd", description="A daemon for automatic background synchronization of the portage tree");
parser.add_argument('--no-daemon', help="Don't fork process to background",
      action='store_const', const=True, default=argparse.SUPPRESS);
parser.add_argument('--time', "-t", action='store', help="Time in hours \
      between syncs", type=float, default=argparse.SUPPRESS);
parser.add_argument('--wait', '-w', action='store', help="Time to wait after\
      failed sync", type=float, default=argparse.SUPPRESS);
parser.add_argument('--config', type=file, action='store',
      default='/etc/portup.conf',
      help="specify config file to use")

default_opts = {'time': 24.0, 'wait': 5.0, \
      'deep': True, 'pkglist': 'world', 'no_daemon': False}
last_sync = 0;

def main_loop(hours, wait_int):
   global last_sync
   delay = float(hours) * 60 * 60 # hours to check
   time.sleep(float(wait_int) * 60);
   while 1:
      cur_time = time.time();
      print "Last Sync at ", time.ctime(last_sync)
      print "Current time is ", time.ctime(cur_time)
      print "Difference of ", cur_time-last_sync
      print "waiting till ", delay
      if cur_time-last_sync > delay: # Hours
         last_sync = cur_time
         _emerge.main.emerge_main(['--sync'])
         print "Synced waiting ",delay, " hours"
         time.sleep(delay) # sleep till next time to sync
      else:
         print "Failed, waiting ", wait_int, " minutes"
         time.sleep(float(wait_int)*60) # else wait five minutes. TODO add feature in config file

def setEnv():
   environment = default_opts
   clargs = vars(parser.parse_args())
   fileOpts=ConfigParser.RawConfigParser();
   try:
      fileOpts.readfp(clargs.get('config'))
      for each in default_opts.keys():
         if fileOpts.has_option('portupd', each):
            environment[each] = fileOpts.get('portupd', each)
         if clargs.get(each) != None:
            environment[each] = clargs.get(each)

   except IOError as e:
      print "Config file not found"
      sys.exit()

   return environment

def portupd_main(args):
   if (os.geteuid() != 0):
      print "Must be run as root";
      sys.exit();

   env = setEnv();

   if (env.get('no_daemon') == 'False' or env.get('no_daemon') == False):
      print "forking to background"
      if (os.fork() == 0):
          os.setpgid(0,0);
          pidfile = open('/var/run/portupd.pid', 'w')
          pidfile.write(os.getpid());
          close(pidfile);
          fd = os.open("/dev/null", os.O_WRONLY);
          os.dup2(fd,1);
          os.close(fd);
          main_loop(env.get('time'), env.get('wait'));

   else:
        print "Keeping in foreground"
        main_loop(env.get('time'), env.get('wait'));
#args = ["-D", "-u", "-p", "-N", "world"];
#_emerge.main.emerge_main(args);

portupd_main(sys.argv);
