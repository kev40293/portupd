#!/usr/bin/python

import argparse;
import config;

def parse_arguments():
   parser = argparse.ArgumentParser(prog="portupd", description="A daemon for automatic background synchronization of the portage tree");
   parser.add_argument('--no-daemon', help="Don't fork process to background",
         action='store_const', const=True, default=argparse.SUPPRESS);
   parser.add_argument('--time', "-t", action='store', help="Time in hours \
         between syncs", type=float, default=argparse.SUPPRESS);
   parser.add_argument('--wait', '-w', action='store', help="Time to wait after\
         failed sync", type=float, default=argparse.SUPPRESS);
   parser.add_argument('--config', type=file, action='store',
         default='/etc/portup.conf',
         help="specify config file to use")
   parser.add_argument("--pid-file", type=str, action='store',
         help="Specify PID file", default=argparse.SUPPRESS)
   bool_opts = ['deep','no_daemon']
   float_opts = ['time', 'wait']
   default_opts = {'time': 24.0, 'wait': 5.0,
         'deep': True, 'pkglist': 'world', 'no_daemon': False,
         'pid_file': '/var/run/portupd.pid'}

   cmdargs = vars(parser.parse_args())
   configobj = config.Config(cmdargs['config'])
   configuration = configobj.getOpts()
   for key in cmdargs.keys():
      configuration[key] = cmdargs[key]

   return configuration
