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

#update this to be easier to add functionality and such
def parse_arguments():
   parser = argparse.ArgumentParser(prog="portupd", description="A daemon for automatic background synchronization of the portage tree");
   options = {"--no-daemon" : {
                        "help" : "Don't run as daemon",
                        "action" : "store_const",
                        "const" : True,
                        "default" : argparse.SUPPRESS},
              "--time" : {
                        "shortopt" : "-t",
                        "help" : "Time in hours between syncs.",
                        "type" : float,
                        "action" : "store",
                        "default" : argparse.SUPPRESS},
              "--wait" : {
                        "shortopt" : "-w",
                        "help" : "Time in minutes to wait after failed sync.",
                        "type" : float,
                        "action" : "store",
                        "default" : argparse.SUPPRESS},
              "--config" : {
                        "type": file,
                        "action" : "store",
                        "default" : argparse.SUPPRESS,
                        "help" : "Configuration file to use"},
              "--pid-file" : {
                        "type" : str,
                        "help" : "pid file for daemon",
                        "default" : argparse.SUPPRESS,
                        "action" : "store"}
              }
   for opts, kwargs in options.items():
      shortopt = kwargs.pop("shortopt",None)
      args = [opts]
      if shortopt is not None:
         args.append(shortopt)
      parser.add_argument(*args, **kwargs)

   cmdargs = vars(parser.parse_args())
   configobj = config.Config(cmdargs['config'])
   configuration = configobj.getOpts()
   for key in cmdargs.keys():
      configuration[key] = cmdargs[key]

   return configuration
