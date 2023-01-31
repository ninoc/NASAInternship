import numpy as np
import pandas as pd
import geopy.geocoders
from geopy.geocoders import Nominatim

######################################################################################################################################################################################################################################################################################################################################################################################################

def latlongcalculator(place, username):
    '''
    place = Location name (string)
    username = geolocator Nominatim user_agent name (string) 
    '''
    geolocator = Nominatim(user_agent=username)
    location = geolocator.geocode(place)
    return location.latitude, location.longitude

######################################################################################################################################################################################################################################################################################################################################################################################################

def get_zipcode(lat, long, username):
    '''
    lat = latitude (float)
    long = longitude (float)
    username = geolocator Nominatim user_agent name (string)
    '''
    geolocator = Nominatim(user_agent=username)
    location = geolocator.reverse((lat, long))
    return location.raw['address']['postcode']

######################################################################################################################################################################################################################################################################################################################################################################################################

def LocFinder(df, username):
    '''
    This code takes in a DataFrame of fellows and their host institutions and returns the same DataFrame with filled out Latitude, Longitude, Address, and Zip Code columns.
    
    df = a pandas DataFrame with empty Latitude, Longitude, Address, and Zip Code columns to the right of a filled-out "Host Institution" column
    
    df (return) = a pandas DataFrame with filled-out Latitude, Longitude, Address, and Zip Code columns
    ERROR = a list of institutions that need to be manually filled out because they were not recognized by geopy
    
    NOTE: Ensure that the inputted DataFrame's Host Institutions have consistent names, i.e., correct abbreviations such as UC Berkely or UVA to their full, official names.
    '''
    loc = Nominatim(user_agent=username)
    geopy.geocoders.options.default_timeout = 10
    
    # Pulling data from df
    names = df['Full Name']
    institutions = df['Host Institution']
    
    print('Step 1 complete.')
    
    # Finding lat and long with geopy
    ERROR = []
    lat, long = [],[]
    for i in institutions.values:
        getLoc = loc.geocode(i)
        #print(i)
        try:
            lat.append(getLoc.latitude)
            long.append(getLoc.longitude)
            #print('Found for', i)
        except:
            #print('Not found for', i )
            ERROR.append(i)
            lat.append(np.NAN)
            long.append(np.NAN)
            
    print('Step 2 complete.')
    
    # Finding address with geopy
    address = []
    for i in institutions.values:
        getLoc = loc.geocode(i)
        try:
            address.append(getLoc.address)
            #print('Found for', i)
        except:
            #print('Not found for', i )
            address.append(np.NAN)
    
    print('Step 3 complete.')
    
    # Finding zip code from lat and long
    zipcodes = []
    for i in range(len(institutions)):
        try:
            zipcode = get_zipcode(lat[i], long[i])
            zipcodes.append(zipcode)
        except:
            zipcodes.append(np.NAN)
    
    print('Step 4 complete.')
    
    df['Latitude of Host Institution'] = lat
    df['Longitude of Host Institution'] = long
    df['Address of Host Institution'] = address
    df['Zip Code of Host Institution'] = zipcodes
    
    print('Step 5 complete.')
    
    return df, ERROR

######################################################################################################################################################################################################################################################################################################################################################################################################

def NumberofFellowsperInst(df):
    '''
    This code takes a DataFrame of host institutions and returns the number of fellows at each institution.
    
    df = a pandas DataFrame that includes the following information:
        - Host institution name
        - Full name of fellow
        - Latitude of host institution
        - Longitude of host institution
        - Zip code of host institution
        
    instnumClean = a pandas DataFrame that includes the following information:
        - Host institution name
        - Latitude of host institution
        - Longitude of host institution
        - Number of fellows at host institution
    '''
    
    # Pulling data from df
    lat = df['Latitude of Host Institution']
    long = df['Longitude of Host Institution']
    inst = df['Host Institution']
    name = df['Full Name']
    zipcode = df['Zip Code of Host Institution']
    
    print('Step 1 complete.')
    
    # Sorting by institution name 
    numInst = df.groupby('Host Institution').count()

    numFellowByInst = pd.DataFrame()

    numFellowByInst['Host Institution'] = [str(i) for i in numInst.index]
    numFellowByInst['Number of Fellows'] = numInst['Full Name'].values
    
    print('Step 2 complete.')
    
    # Building instzipnum
    instnum = []
    for i in range(len(inst)): 
        current_inst1 = df['Host Institution'][i]
        current_lat = df['Latitude of Host Institution'][i]
        current_long = df['Longitude of Host Institution'][i]
        for j in range(len(numFellowByInst)):
            current_inst2 = numFellowByInst['Host Institution'][j]
            current_num = numFellowByInst['Number of Fellows'][j]
            if current_inst2 == current_inst1:
                instnum.append([current_inst1, current_lat, current_long, current_num])
            else:
                j = j+1
        #i = i+1
    
    print('Step 3 complete.')
    
    # Converting to array
    instnum = np.array(instnum)
    
    print('Step 4 complete.')
    
    # Building a dictionary of this data
    instnumDict = {
        "Host Institution": instnum[:,0],
        "Latitude": instnum[:,1],
        "Longitude": instnum[:,2],
        "Number of Fellows": instnum[:,3]
    }
    
    print('Step 5 complete.')
    
    # Converting to a DataFrame
    instnumDf = pd.DataFrame.from_dict(instnumDict)
    
    print('Step 6 complete.')
    
    # Removing duplicates
    instnumClean = instnumDf.drop_duplicates()
    
    print('Step 7 complete.')
    
    return instnumClean
