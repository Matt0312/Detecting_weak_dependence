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




commandlineargs.add_argument('-u', nargs = 1,  dest = "separate_users", default = Separate_users, metavar = 'PATH', help
                             = 'Set if you want to model each user separately include the list of users as a text file with each user on a separate line' )




commandlineargs.add_argument('-d', nargs = 1, dest = "firstday",
                             help = 'time at midnight for the first day', required = True,
                             type = int)

args = commandlineargs.parse_args()





if args.firstday:
    #ensure midnight on the firstday
    day = int(dt.date.fromtimestamp(float(args.firstday[0])).strftime('%s'))


else:
    print >> sys.stderr, "Must specify unix time for first day."




if args.separate_users:
    Users = []
    Separate_users = True
    text = open(args.separate_users[0])
    for line in text:
        Users += [line.strip()]






userhash = {}



userhash['all'] = User(day)
for line in sys.stdin:


    fields = line.rstrip('\r\n').split(' ')
    time = round(float(fields[0]),3)
    eventid = fields[1]


    user = fields[1]


        


    userhash['all'].update_data(time, eventid)


event_pairs,Fisher,HC = userhash['all'].plot_pvalues()

for i in range(len(event_pairs)):
    print (event_pairs[i])
    print (Fisher[i],'Fishers method')
    print (HC[i], 'Higher criticism')




