import pandas as pd
import folium
import json
from folium import plugins

def mapMaker(FellowsFile, HSIFile, BSIFile, HBCUFile, R2File):
    '''
    This function takes in the necessary files to build the NHFP Map with surrounding insitutions. 
    All inputs are string file names or directory maps.
    
    FellowsFile = csv containing fellow information ('allFellows_FellowshipTypeSplit.csv')
    HSIFile = csv containing information on HSIs ('FINAL_HSIData.csv')
    BSIFile = csv containing information on BSIs ('FINAL_HBCUData.csv')
    HBCUFile = csv containing information on HBCUs ('FINAL_BSIData.csv')
    R2File = csv containing information on R2s ('R2_Inst.csv')
    
    This function returns a .html file of the map.
    '''
    
    # STEP 1: Read in files
    allFellows = pd.read_csv(FellowsFile)
    HSIs = pd.read_csv(HSIFile)
    HBCUs = pd.read_csv(BSIFile)
    BSIs = pd.read_csv(HBCUFile)
    R2s = pd.read_csv(R2File)
    
    HSIs = HSIs[HSIs['Astronomy Faculty (Y/N)'] != 'N']
    HBCUs = HBCUs[HBCUs['Astronomy Faculty (Y/N)'] != 'N']
    BSIs = BSIs[BSIs['Astronomy Faculty (Y/N)'] != 'N']
    R2s = R2s[R2s['Numerous Astronomy Faculty (Y/N)'] != 'N']
    
    # STEP 2: Initialize map
    usMap = folium.Map(location=[39.0,-96.0], tiles = 'Stamen Toner', zoom_start=4, control = False, name = "Base Map")

    tit = 'Past NHFP Host Institutions and Nearby Institutions with Astronomy Faculty'
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
                location = [BSIs.values[i][8], BSIs.values[i][9]],
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
                location = [HSIs.values[i][8], HSIs.values[i][9]],
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
                location = [HBCUs.values[i][8], HBCUs.values[i][9]],
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