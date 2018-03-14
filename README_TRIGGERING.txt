# SToCND

### Python code for modelling seasonality and self-exciting behaviour in a sequence of event times

###Verion 1.0 uploaded of 14th March 2017

###Usage ./Triggering_model_git.py -h

###Documentation A description of the algorithms are given in the manuscripts Detecting weak dependence in computer network traffic patterns using higher criticism and Statistical Modelling of Computer Network Traffic Event Times.

### Output For each pair of event ids in the test data output is. 
### Triggering eventid, Triggered eventid ‘\n’ Fishers method p-value ‘\n Higher criticism pvlaue.


### Data Format, the data should come in the form of an event time, event id, log on type and a user separated by a space. An example is shown in Failed_LOGON_and_SSD.txt.


###TEST EXAMPLE cat Failed_LOGON_and_SSD.txt |./Triggering_model_git.py -d 0 
###This should give similar results to those shown in the manuscript Detecting weak dependence in computer network traffic patterns using higher criticism for detecting triggering between screen saver disable events and failed log on events for User 233172.


