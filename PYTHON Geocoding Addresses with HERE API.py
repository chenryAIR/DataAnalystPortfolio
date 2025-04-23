#################################################################################################
#Created by Chad Henry
#Created 2.14.2025
#Updated 2.14.2025

#Purpose: This code will geocode addresses using HERE api

#NOTE: The limit for geocoding is currently 30k per month. Any usage over that will have a cost.
     
#################################################################################################


import requests
import pandas as pd 
import numpy as np

#Set up where all the data is and going--------------------------
path = r'H:\share\GIS Methods Group\ISBE'
input = fr'{path}\RawData\isbemap_dot.xlsx'
output = fr'{path}\WorkingData'


#Read in the data------------------------------------------------
df = pd.read_excel(input)

#Clean up the zip codes------------------------------------------
##Replace spaces with -
df['Zip']=df['Zip'].apply(lambda x: x.strip().replace(" ","-"))

#Set up for the geocoding----------------------------------------
URL = "https://geocode.search.hereapi.com/v1/geocode" 
api_key = 'xxxxxxxxxxxx' 


#Set up the vars we'll get from the API
df['X_Here'] = float()
df['Y_Here'] = float()

df['resultType'] = ""
df['queryScore'] = ""
df['city'] = ""
df['streets'] = ""
df['houseNumber'] = ""
df['postalCode'] = ""


for i in df.index:
    location = "{0} {1} {2}".format(df.Address[i], df.City[i], df.Zip[i])
   
    params = {'q':location, 'apikey':api_key}


    # sending get request and saving the response as response object
    # 
    print(URL, params=params, verify=False)
    response = requests.get(URL, params=params, verify=False) 
    data = response.json()
   

    
    if response.status_code == 200:
        data = response.json()
    # Check if any results were found
        if data['items']:
            # Extract the latitude and longitude from the first result
            # Also get the scores, etc. 
            location = data['items'][0]['position']
            text_address = data['items'][0]['address']
            scoring = data['items'][0]['scoring']
            fieldscoring = data['items'][0]['scoring']['fieldScore']

            latitude = location['lat']
            longitude = location['lng']
            df['X_Here'].loc[i] = longitude
            df['Y_Here'].loc[i] = latitude
            try:
                df['resultType'].loc[i] = data['items'][0]['resultType']
            except:
                df['resultType'].loc[i] = "NA"
            try:
                df['queryScore'].loc[i] = scoring['queryScore']
            except:
                df['queryScore'].loc[i] = "NA"
            try:
                df['city'].loc[i] = fieldscoring['city']
            except:
                df['city'].loc[i] =  "NA"
            try:
                df['streets'].loc[i] = fieldscoring['streets']
            except:
                df['streets'].loc[i] =  "NA"
            try:
                df['houseNumber'].loc[i] = fieldscoring['houseNumber']
            except:
                df['houseNumber'].loc[i] =  "NA"
            try:
                df['postalCode'].loc[i] = fieldscoring['postalCode']
            except:
                df['postalCode'].loc[i] =  "NA"

        else:
            print("{}. {} couldn't be found".format(i, location))
        
        #export every 500 in case the code hits and error. Don't want to have to redo so many if it errors. 
        if i % 500 == 0:
            df.to_csv(fr'{output}\geocodes_{i}.csv')

#Light data results checking
""""IL":
  {
    "name": "Illinois",
    "min_lat": 36.9894,
    "max_lat": 42.5116,
    "min_lng": -91.512,
    "max_lng": -87.0213
  }"""

print("Are the lat/lngs outside of the state?")
df['check_long'] = np.where((df['X_Here'] < -91.512) | (df['X_Here'] > -87.0213), 1, 0)
print("Longitude: {df['check_long'].value_counts()}")


df['check_lat'] = np.where((df['Y_Here'] < 36.9894) | (df['Y_Here'] > 42.5116), 1, 0)
print("Latitude: df['check_lat'].value_counts()")


print("Geocode Quality Checks")
df['queryScore_fill'] = np.where(df['queryScore'] == "", "0",df['queryScore'])
df['check_score'] = np.where(df['queryScore_fill'].astype(float) < .9,1,0)
print("Scores < .9")
print(df['check_score'].value_counts())
print("Result Types")
print(df['resultType'].value_counts())

#export data
df.to_csv(fr'{output}\geocodes_final.csv')
