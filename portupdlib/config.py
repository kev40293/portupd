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
import option

class Config(object):
   OPTIONS = None
   FILE=None
   def __init__(self, filehandle):
      try:
        self.FILE=open(filehandle, "r")
        self.load()
      except IOError as err:
         print "Config File not found. Using Defaults."
         self.loadDefaults()

   def load(self):
      self.OPTIONS = {}
      parser = ConfigParser.ConfigParser()
      try:
         parser.readfp(self.FILE)
         for section, confopts in option.APP_OPTIONS.items():
            for confop in confopts:
               if parser.has_option(section, confop.get_name()):
                  try:
                      var = confop.get_name()
                      if confop.get_type() is bool:
                         self.OPTIONS[var] = parser.getboolean(section,var)
                      elif confop.get_type() is float:
                         self.OPTIONS[var] = parser.getfloat(section,var)
                      else:
                         self.OPTIONS[var] = parser.get(section,var);
                  except ValueError as te:
                     print confop.get_name()
                     self.OPTIONS[confop.get_name()] = confop.get_default()
               else:
                  self.OPTIONS[confop.get_name()] = confop.get_default()
      except ConfigParser.ParsingError as e:
         print "Error parsing configuration file. Using defaults"
         self.loadDefaults()

   def loadDefaults(self):
      for section, confopts in option.APP_OPTIONS.items():
         for confop in confopts:
            self.OPTIONS[confop.get_name()] = confop.get_default()

   def getOpts(self):
      return self.OPTIONS

