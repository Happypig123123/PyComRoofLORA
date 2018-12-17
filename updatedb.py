from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import time
import calendar
import sys


def getTemp():

    return sys.argv[1]
# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1') #Get table

table = dynamodb.Table('RoofTemps') #get table
Time = int(time.strftime('%H%M')) #Get current time
date = str(time.strftime('%d/%m/%y')) #Get curent date
identify = calendar.timegm(time.gmtime()) # Get seconds since EPOCH (used as our ID in dynamodb)


#Write the JSON, with our item and its ID, Time, Temperature, and Date.
response = table.put_item(
   Item={
        'ID': identify,
        'Time': Time,
        'Tempreature': getTemp(),
        'Date': date
        }

)

print("PutItem succeeded:") #Let us know it worked
print(json.dumps(response, indent=4, cls=DecimalEncoder)) #print response from dynamodb
