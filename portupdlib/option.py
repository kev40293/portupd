#!/usr/bin/python
#
#       lportupd ConfigParser - Parse config file
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

class Option(object):
   var = None
   default_val = None
   var_type = None
   def __init__(self, name, default=None, type=str):
      self.var = name
      self.default_val = default
      self.var_type = type
   def get_type(self):
      return self.var_type
   def get_default(self):
      return self.default_val
   def get_name(self):
      return self.var

APP_OPTIONS = {
      'global': [
         Option('config', default=None, type=file)],
      'sync' : [
         Option('time', default=25, type=float),
         Option('wait', default=5, type=float),
         Option('no_daemon', default=False, type=bool),
         Option('pid_file', default='/var/run/portupd.pid', type=str)],
      'update' : [
         Option('deep', default=True, type=bool),
         Option('pkglit', default='world', type=str)]
      }
