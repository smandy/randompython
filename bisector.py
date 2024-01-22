#!/usr/bin/env python

import sys

for x in open('/home/andy/gtd_wc/gtd.org'):
    if ' Mam 999 ' in x:
        print("Found - returning 0")
        sys.exit(0)

print("Failed - return 1")
sys.exit(1)
