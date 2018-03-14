#! /usr/bin/env python


import sys
import datetime as dt
from scipy.optimize import minimize
from numpy import log,exp,diff,cumsum,mean,argmin,median
import matplotlib.pyplot as plt
from scipy.stats import expon,kstest, combine_pvalues
import random
import math
import networkx as nx
import Modelling_Network_Data_git as MND

secsinday = 86400
season = 7
workweek=7
geom = True
Waiting =False


random_events = [int(random.uniform(86400*7,86400*14)) for i in range(100)]
random_events.sort()
#print (random_events)

class User():
    def __init__(self, firsttimeseen):
        
        self.random_pvalues = {}

        self.trainingdata = []
        self.transformed_data = []
        self.pvalues = []
        
        self.eventids = []
        self.events_hash = {}
        self.CPP = {}
        


    
        ###WS
        self.WS_cps = {}
        self.WS_rates = {}
        self.WS_cutoffs = {}
        self.WS_pvalues = {}


    
    
        self.start = int(dt.date.fromtimestamp(firsttimeseen).strftime('%s'))
        self.training_periods = 0

    def update_data(self, time, eventid):
        if eventid not in self.eventids:
            self.eventids += [eventid]
            self.events_hash[eventid] = [time-self.start]



        else:
            self.events_hash[eventid] += [time - self.start]

                
        
    

    def plot_pvalues(self):
            
        
        self.get_self_exciting_parameters()
        
        for id1 in self.events_hash:
            for id2 in self.events_hash:
                j = 0
                start_events =[k for k in range(len(self.events_hash[id1])) ]
                if len(start_events ) > 0:
                    
                    i = min(start_events)
                else:
                    break
        
                while 1==1:
                    end_events = [k for k in range(len(self.events_hash[id2])) if self.events_hash[id2][k] >= self.events_hash[id1][i] and k > j ]
                
                    
                    if len ( end_events ) > 0:
                        j = min(end_events)
                    else:
                        break
                    if id2 in self.WS_cutoffs  and id1 != id2:
                        waiting_time = self.events_hash[id2][j] - self.events_hash[id1][i]
                        previous_event = self.events_hash[id2][j-1]
                        start_time = self.events_hash[id1][i]
                        starting_point = start_time - previous_event

                        pvalue_1 = self.get_pvalue_WS_geom(starting_point, waiting_time + starting_point, id2)
                            

   
                        if waiting_time == 0:
                            pvalue_2 = 0
                        else:
                            
                            pvalue_2 = self.get_pvalue_WS_geom(starting_point,waiting_time + starting_point - 1, id2 )

                        pvalue = random.uniform(pvalue_1, pvalue_2)

                        if pvalue != 0:
    
                            if id1+ ',' + id2 in self.WS_pvalues:
                                self.WS_pvalues[id1 + ',' + id2] += [pvalue]
                            else:
                                self.WS_pvalues[id1 + ',' + id2] = [pvalue]
                    




                    end_events = [k for k in range(len(self.events_hash[id1])) if self.events_hash[id1][k] >= self.events_hash[id2][j] and k > i ]
                    
                    if len ( end_events ) > 0:
                        i = min(end_events)
                    else:
                        break
                    if id1 == id2:
                        waiting_time = self.events_hash[id1][i] - self.events_hash[id1][i-1]
                        starting_point = 0
                    
                    else:
                        waiting_time = self.events_hash[id1][i] - self.events_hash[id2][j]
                        previous_event = self.events_hash[id1][i-1]
                        start_time = self.events_hash[id2][j]
                        starting_point = start_time - previous_event

                
    
                                    
        events = []
        combs = []
        means = []
        medians = []
        H_Cs = []
        for i in self.WS_pvalues:
            
            start,end = i.strip().split(',')

            if len(self.WS_pvalues[i]) > 1:
                P = self.WS_pvalues[i]

                if len(P) < 10:
                    continue
                
                
                samp_stat=[]
                M = 10000
                
                for k in range(M):
                    list1=[random.uniform(0,1) for l in range(len(P))]

                    samp_stat+=[donohostat(list1)]

                stat=donohostat(P)


                H_C_pvalue = sum([1 for q in samp_stat if q>stat])/float(M)
    
                total_pvalue = combine_pvalues(P)[1]

                events += [i]
                combs += [total_pvalue]
                means += [mean(P)]
                medians += [median(P)]
                H_Cs += [H_C_pvalue]



        return events,combs,H_Cs




    






############FUCTIONS TO GET PARAMETERS




    def get_self_exciting_parameters(self):
        for id1 in self.eventids:
            if len(self.events_hash[id1]) > 1:
                

                self.WS_cutoffs[id1] = []
                self.WS_cps[id1] = []
                self.WS_rates[id1] = []

                self.WS_cutoffs[id1] ,self.WS_rates[id1], self.WS_cps[id1] =  MND.step_function_PELT_MLE( self.events_hash[id1], geom, Waiting )










################ FUNCTIONS TO GET PVALUES




    def get_pvalue_WS_geom(self, s, x, id):
        C = 0
        T = 1

    
        if len(self.WS_cutoffs[id]) == 0:
            C += T * (1 - (1 - self.WS_rates[id][-1])**( x - s +1 ) )
            return C
    
        if s > self.WS_cutoffs[id][-1]:
            C += T * (1 - (1 - self.WS_rates[id][-1])**( x - s +1 ) )

            return C

        
        start = min ([c for c in range(len(self.WS_cutoffs[id])) if self.WS_cutoffs[id][c] >= s])
        


        if x <= self.WS_cutoffs[id][start]:
            return 1 - (1 - self.WS_rates[id][start])**(x-s+1)
        else:
            T = T * (1 - self.WS_rates[id][start])**(self.WS_cutoffs[id][start] -s + 1)
            C += 1 - (1 - self.WS_rates[id][start])**(self.WS_cutoffs[id][start] - s + 1)

        for i in range (start + 1  , len ( self.WS_cutoffs[id] ) ):
            if x > self.WS_cutoffs[id][i]:
                C += T * (1 - (1 - self.WS_rates[id][i])**( self.WS_cutoffs[id][i] - self.WS_cutoffs[id][i-1] ) )
                T = T * ( (1 - self.WS_rates[id][i])**( self.WS_cutoffs[id][i] - self.WS_cutoffs[id][i-1] ) )
            else:
                C += T * (1 - (1 - self.WS_rates[id][i])**( x - self.WS_cutoffs[id][i-1] ) )
                return C
        C += T * (1 - (1 - self.WS_rates[id][-1])**( x - self.WS_cutoffs[id][-1] ) )
        return C
    
    




def get_cdf(P):
    P.sort()
    cdfx=[i/10000 for i in range(10000)]
    cdfy =[]
    k=0
    for i in cdfx:
        #print (k)
        while P[k] < i:
            k+=1
            if k>=len(P):
                break
        cdfy +=[k/len(P)]
        if k>=len(P):
            break
    while len(cdfy) < len(cdfx):
        cdfy+=[1]
    return cdfx,cdfy


def  donohostat(x):
    x.sort()
    nn = len(x)
    if nn ==0:
        return 1
    else:
        res=[]
        for i in range(nn):
            if x[i]>=0.9999999:
                x[i] = 0.99999999
            if x[i]<= 1/nn:
                x[i] =0.5
            res+=[math.sqrt(nn)*((i+1.0)/nn-x[i])/(math.sqrt(x[i]*(1-x[i])))]

    return max(res)
















