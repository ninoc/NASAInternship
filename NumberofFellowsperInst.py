import numpy as np
import pandas as pd

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