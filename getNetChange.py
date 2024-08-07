#!/usr/local/bin/python

import sys, os, string, regexp, time
from getopt import getopt

shortOpts = 'r'
longOpts = ['source=']

try:
    optlist, args = getopt(sys.argv[1:], shortOpts, longOpts)
    if len(args) < 1:
        print "Usage: getNetChangePort.pl tickerfile [...]"
        raise "UsageError", "No RIC (or file) specified!"
except:
    print "\n", sys.exc_value, "\n"
    sys.exit(-1)

optsGiven = {}
for opt, value in optlist:
    optsGiven[opt] = value

#feed = 'IDN_SELECTFEED';
feed = 'IDN_MARKETFEED';
if optsGiven.has_key('--source'):
    feed = optsGiven['--source']

if optsGiven.has_key('-r'):
    normal = "\033[37;40m"
    positive = "\033[32;40m"
    negative = "\033[31;40m"
else:
    normal = "\033[30;47m"
    positive = "\033[32;47m"
    negative = "\033[31;47m"

import ssl

def getTickerData(ticker):
    if all_lower.match(ticker) != ():
        ticker = string.upper(ticker)

    data = []
    data = ssl.getReutersData(feed, ticker, fields)
    try:
        if data[0] != "":
            data.insert(0, ticker)
            sys.stdout.write("%s%-10s" % (normal, data[0]))
            sys.stdout.write("%10s" % data[1])
            netchg = string.atof(data[2])
            if (netchg == 0):
                sys.stdout.write("%10s" % data[2])
            elif (netchg < 0):
                sys.stdout.write("%s%10s%s" % (negative, data[2], normal))
            else:
                sys.stdout.write("%s%10s%s" % (positive, data[2], normal))
            sys.stdout.write("%10s" % data[3])
            sys.stdout.write("%10s" % data[4])
            sys.stdout.write("%10s" % data[5])
            sys.stdout.write("\n")
        else:
            print ticker, ": Error!"
    except TypeError:
        pass
    return None

all_lower = regexp.compile("^[a-z0-9\.]+$")

try:
    ssl.openReuters("/LocalDeveloper/Reuters/idn/templates/getprice_gf_tab")
except:
    pass
    sys.exit(-1)

fields = ["TRDPRC_1", "NETCHNG_1", "HST_CLOSE", "BID", "ASK"]

for fn in args:
    if os.path.isfile(fn):
        try:
            f = open(fn)
        except IOError, msg:
            sys.stderr.write('%s: %s\n' % (fn, msg))
            continue

        while 1:
            line = f.readline()
            if not line:
                break
            ticker = string.split(line)[0]
            if ticker == '':
                continue

            getTickerData(ticker)
        f.close()
    else:
        getTickerData(fn)

ssl.closeReuters()
sys.stdout.write(normal)
