#! /usr/bin/env python

import datetime as dt
import sys
import json
import argparse
import numpy as np
from numpy import mean
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
from Triggering_Behaviour import User



"""assumes seasonal period is one day"""


secsinday = 86400

"""defaults"""
workweek = 7
trainingperiod = 14
Nine80 = False
Separate_users = False
Mutual_Exciting = False
seasonal = False
geom = True
JSON = False

"""Parses command-line arguments and executes."""
formatter = argparse.ArgumentDefaultsHelpFormatter
commandlineargs = argparse.ArgumentParser(formatter_class = formatter, description = "The program reads from stdin and outputs to stdout.")

#commandlineargs.add_argument('-t', nargs = 1, dest = "trainingperiod",
#                            default = trainingperiod,
#                             help ='training period in days (must be a multiple of work week)',
#                             type = int)




commandlineargs.add_argument('-u', action = 'store_true', dest = "separate_users", default = Separate_users, help
                             = 'Set if you want to model each edge separately')




commandlineargs.add_argument('-d', nargs = 1, dest = "firstday",
                             help = 'time at midnight for the first day', required = True,
                             type = int)

args = commandlineargs.parse_args()





if args.firstday:
    #ensure midnight on the firstday
    day = int(dt.date.fromtimestamp(float(args.firstday[0])).strftime('%s'))


else:
    print >> sys.stderr, "Must specify unix time for first day."





userhash = {}
if args.separate_users:
    Separate_users = True
else:
    userhash['all'] = User(day)










for line in sys.stdin:


    fields = line.rstrip('\r\n').split(' ')
    time = round(float(fields[0]),3)
    eventid = fields[1]


    user = fields[3]


        
    
    if Separate_users:
        if user not in userhash:
            userhash[user] = User(day)
        userhash[user].update_data(time, eventid)
    else:
        userhash['all'].update_data(time, eventid)

if Separate_users:
    for user in userhash:
        event_pairs,Fisher,HC = userhash[user].plot_pvalues()

        for i in range(len(event_pairs)):
            print (event_pairs[i])
            print (Fisher[i],'Fishers method')
            print (HC[i], 'Higher criticism')



else:
    event_pairs,Fisher,HC = userhash['all'].plot_pvalues()

    for i in range(len(event_pairs)):
        print (event_pairs[i])
        print (Fisher[i],'Fishers method')
        print (HC[i], 'Higher criticism')




