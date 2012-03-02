#!/usr/bin/python

import portage, sys, time
from portage import os
import _emerge.main

def emerge_sync_loop(hours, wait_int):
   last_sync = 0
   delay = hours * 60
   time.sleep(wait_int*60)
   while 1:
      cur_time = time.time()
      if cur_time - last_sync > delay:
         if _emerge.main.emerge_main == 0:
            last_sync = cur_time
         else:
            time.sleep(wait_int*60)
