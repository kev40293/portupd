#!/usr/bin/python
#
#       portupd optparser - command line options parser
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
         default=None,
         help="specify config file to use")
   parser.add_argument("--pid-file", type=str, action='store',
         help="Specify PID file", default=argparse.SUPPRESS)

   cmdargs = vars(parser.parse_args())
   configobj = config.Config(cmdargs['config'])
   configuration = configobj.getOpts()
   for key in cmdargs.keys():
      configuration[key] = cmdargs[key]

   return configuration
