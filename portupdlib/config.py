#!/usr/bin/python
#
#       portupd ConfigParser - Parse config file
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

import ConfigParser

TYPES={
      'boolean' : ['no_daemon', 'deep'],
      'floats'  : ['time', 'wait']
      }
DEFAULTS={
      'portupd' : {
         'time' : 24,
         'wait' : 5,
         'pkglist' : 'world',
         'no_daemon' : False,
         'deep' : True},
      'other' : {
         'config' : None,
         'pid_file' : '/var/run/portupd.pid'}
      }

class Config(object):
   OPTIONS = None
   def __init__(self, filehandle):
      self.load(filehandle);

   def load(self, FILE):
      self.OPTIONS = DEFAULTS
      parser = ConfigParser.ConfigParser()
      try:
         parser.readfp(FILE)
         for section in DEFAULTS.keys():
            if parser.has_section(section):
               for op in DEFAULTS[section].keys():
                  if parser.has_option(section, op):
                     if op in TYPES['boolean']:
                        self.OPTIONS[section][op] = parser.getboolean(section,op)
                     elif op in TYPES['floats']:
                        self.OPTIONS[section][op] = parser.getfloat(section,op)
                     else:
                        self.OPTIONS[section][op] = parser.get(section,op)
                  else:
                     self.OPTIONS[section][op] = DEFAULTS[section][op]
      except IOError as e:
          print "Config file not found, using defaults"

   def getOpts(self):
      configvals = {}
      for section in self.OPTIONS.keys():
         for param in self.OPTIONS[section].keys():
            configvals[param] = self.OPTIONS[section][param]
      return configvals

