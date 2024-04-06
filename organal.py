"""
(pyvenv-activate "/home/andy/venvs/org-analyze") 
"""

import orgparse

from orgparse import load, loads

try:
    xs, ys
except:
    xs = orgparse.load("/home/andy/repos/gtd/gtd.org")
    ys = orgparse.load("/home/andy/gtd_wc/gtd.org")

info = [ x for x in xs[0].children if 'Info' in x.heading ][0]

def getNodes(xs, prev = None):
    if prev==None:
        prev = set()

