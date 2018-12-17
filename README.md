#PYCOM LORA TEMPERATURE SENSOR AND GRAPHER
###Using dynambo DB and node-red on RPI

##Main.py
Main.py runs on the pycom LoRa, and is the main script which uploads temperature data using LoRa

##graphTemp.py
Python Script that graphs it using MatPlotLib, using boto3 to get temps from last 24H from AWS DynamoDB.
Requires AWS CLI (loged in) to acess tables. (RoofTemps)

##updatedb.py
Python Script which node red runs (and hands it temperature via command: eg: python3 updatedb.py <temperature>)
to upload temperature (recieved via node red LoRa node).


