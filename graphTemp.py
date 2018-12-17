from __future__ import print_function # Python 2/3 compatibility (Idk if this actualy works.)
import boto3
import operator
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import calendar
import time
import datetime
import ast

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdate


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
#SETUP TABLE
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
idmin = calendar.timegm(time.gmtime()) - 86400 #ALL TEMPERATURES IN THE LAST 24 HOURS
idmax = calendar.timegm(time.gmtime()) + 60 #ALL TEMPERATURES IN THE LAST 24 HOURS, USING ID (EPOCH)
table = dynamodb.Table('RoofTemps')

fe = Key('ID').between(idmin, idmax) #OUR FILTER, which only grabs temps in the last 24H
pe = "ID, #tr, Tempreature"
# Expression Attribute Names for Projection Expression only.
ean = { "#tr": "Time", } # time is a reserved word, so we use a reference, (So #tr represents Time in our scan.)
esk = None


response = table.scan( #Applying our filters, and what information we want to get back.
    FilterExpression=fe,
    ProjectionExpression=pe,
    ExpressionAttributeNames=ean
    )

x = [] #X - xaxis to plot.
y = [] #Y - yaxis to plot.
new = {}
for i in response['Items']: #add all the items (in our scan) to a dictionary called new.
    data = json.dumps(i, cls=DecimalEncoder)
    data = ast.literal_eval(data)
    a = float((float(data["Tempreature"])))
    b = data["ID"]
    data = {b:a}
    new.update(data)
    #print(data)


sortn = [] # The scan may be unsorted, so we sort them in the loop below:

for key in sorted(new.keys()) :
    temp = {key : new[key]} #THE key is seconds since epoch, our time is epoch

    x.append(key) # Append seconds since EPOCH to x axis

    y.append((new[key]/100)) #Devide temperature by 100 (as for eg: 24.67 'c is represented by 2467 in database as LoRa dose not like floats.)






#print(x)
#print("")
#print(y)

#-----------------------------  PLOT IT ---------------------------------------#

fig, ax = plt.subplots() #configure sub plots
secs = mdate.epoch2num(x) #Convert the epoch time to a number for matplotlib

#PLOT IT!
plt.ylim(15, 30) #Set temp limit (so that our graph dosent look wird, eg: (24'C at top, 22'C at bottom))
ax.plot(secs, y, color = 'r') #MAke a sublot, with epoch time as x axis, temps as y axis.

date_fmt = '%H:%M:%S' #Fortmat we want our date to be (Hours minutes seconds) on the graph.
date_formatter = mdate.DateFormatter(date_fmt) #Think this lets matplotlib know what format we want.
ax.xaxis.set_major_formatter(date_formatter) #Think this lets matplotlib know what format we want.

plt.xlabel('Time') #some formating
plt.ylabel("Temperature ('C)")#some formating
fig.autofmt_xdate() #Formatt the x axis with our date_fmt (Hours: Minutes: Seconds)

plt.title('Roof Temperature (past 24H)') #Title
plt.grid(True) # Show a grid
plt.savefig("/var/www/html/t.png") #Save the picture.

#THE END! Yay!
