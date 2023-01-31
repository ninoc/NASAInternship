import pandas as pd
import folium
import json
from folium import plugins

def mapMaker(FellowsFile, MSIR2File):
    '''
    This function takes in the necessary files to build the NHFP Map with surrounding insitutions. 
    All inputs are string file names or directory maps.
    
    EDIT BELOW:
    FellowsFile = csv containing fellow information ('allFellows_FellowshipTypeSplit.csv')
    MSIR2File = csv containing information on HSIs ('FINAL_MSIR2Data.csv')
    
    EDIT BELOW:
    This function returns an interactive map.
    '''
    
    # STEP 1: Read in files
    allFellows = pd.read_csv(FellowsFile)
    MSIs = pd.read_csv(MSIR2File)
    
    HSIs = MSIs[MSIs['Classification'] == 'HSI']
    HSIs = HSIs[HSIs['Astronomy Program (Y/N)'] != 'N']
    
    HBCUs = MSIs[MSIs['Classification'] == 'HBCU']
    HBCUs = HBCUs[HBCUs['Astronomy Program (Y/N)'] != 'N']
    
    BSIs = MSIs[MSIs['Classification'] == 'BSI']
    BSIs = BSIs[BSIs['Astronomy Program (Y/N)'] != 'N']
    
    R2s = MSIs[MSIs['Research Classification'] == 'R2']
    R2s = R2s[R2s['Classification'] != 'HSI']
    R2s = R2s[R2s['Classification'] != 'BSI']
    R2s = R2s[R2s['Classification'] != 'HBCU']
    R2s = R2s[R2s['Astronomy Program (Y/N)'] != 'N']
    
    # STEP 2: Initialize map
    usMap = folium.Map(location=[39.0,-96.0], tiles = 'Stamen Toner', zoom_start=4, control = False, name = "Base Map")

    tit = 'Past NHFP Host Institutions and Nearby Institutions with Astronomy Programs'
    title_html = '''
                 <h3 align="center" style="font-size:24px"><b>{}</b></h3>
                 '''.format(tit)

    sig = 'Credit: M. Volz, A. Cucchiara (NASA HQ)'
    sig_html = '''
                <h1 align="center" style = "font-size:16px">{}</h1>
                '''.format(sig)

    usMap.get_root().html.add_child(folium.Element(title_html))
    usMap.get_root().html.add_child(folium.Element(sig_html))
    
    # STEP 3: Build Fellow layer
    FG_Fellows = folium.FeatureGroup(name = 'Fellows')

    for i in range(len(allFellows)):
        try:
            folium.CircleMarker(
                location = [allFellows['Latitude'][i], allFellows['Longitude'][i]],
                popup = allFellows['Host Institution'][i] + '. ' + str(allFellows['Number of Fellows'][i]) + ' Fellows in total.' + ' H: ' + str(allFellows['Number of Hubble Fellows'][i]) + ' S: ' + str(allFellows['Number of Sagan Fellows'][i]) + ' E: ' + str(allFellows['Number of Einstein Fellows'][i]),
                radius = float(allFellows['Number of Fellows'][i]),
                color = 'crimson',
                fill = True,
                fill_color = 'crimson'
            ).add_to(FG_Fellows)
        except:
            i = i+1

    FG_Fellows.add_to(usMap)
    
    # STEP 4: Build BSI layer
    FG_BSIs = folium.FeatureGroup(name = 'Black Serving Institutions')

    for i in range(len(BSIs)):
        try:
            folium.Marker(
                location = [BSIs.values[i][9], BSIs.values[i][10]],
                popup = BSIs.values[i][0],
                icon = folium.Icon(color = 'darkpurple', icon_color = 'white', icon = 'circle'),
                fill = True,
            ).add_to(FG_BSIs)
        except:
            i = i+1

    FG_BSIs.add_to(usMap)

    # STEP 5: Build HSI Layer
    FG_HSIs = folium.FeatureGroup(name = 'Hispanic Serving Institutions')

    for i in range(len(HSIs)):
        try:
            folium.Marker(
                location = [HSIs.values[i][9], HSIs.values[i][10]],
                popup = HSIs.values[i][0],
                icon = folium.Icon(color = 'blue', icon_color = 'white', icon = 'circle'),
                fill = True,
            ).add_to(FG_HSIs)
        except:
            i = i+1

    FG_HSIs.add_to(usMap)

    # STEP 6: Build HBCU layer
    FG_HBCUs = folium.FeatureGroup(name = 'HBCUs')

    for i in range(len(HBCUs)):
        try:
            folium.Marker(
                location = [HBCUs.values[i][9], HBCUs.values[i][10]],
                popup = HBCUs.values[i][0],
                icon = folium.Icon(color = 'darkblue', icon_color = 'white', icon = 'circle'),
                fill = True,
            ).add_to(FG_HBCUs)
        except:
            print(i)

    FG_HBCUs.add_to(usMap)
    
    FG_R2s = folium.FeatureGroup(name = 'R2 Institutions')

    # STEP 7: Build R2 layer
    for i in range(len(R2s)):
        try:
            folium.Marker(
                location = [R2s.values[i][9], R2s.values[i][10]],
                popup = R2s.values[i][0],
                icon = folium.Icon(color = 'orange', icon_color = 'white', icon = 'circle'),
                fill = True,
            ).add_to(FG_R2s)
        except:
            i = i+1

    FG_R2s.add_to(usMap)
    
    # STEP 8: Add legend to map
    folium.LayerControl(collapsed = False).add_to(usMap)
    
    # STEP 9: Download map
    usMap.save('NHFPFellowsMap.html')
    
    return usMap
