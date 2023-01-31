Hi ! Thanks for accessing my files. This should just be Nino looking at this to make sure I didn't mess anything up when tweaking my code for GitHub testing. If you're not Nino, please delete these files. Thanks.

Eventually I will include a more detailed disclaimer and description in this file. I'm continuously working on it, so make sure to check back for updates.

Necessary packages:
- pandas
- folium
    - folium plugins
- json
- geopy.geocoders
    - geopy.geocoders Nominatim
    - Nominated user_agent (you have to make an account)

Detailed function descriptions:

mapMaker()
-----------------------------
This function takes in two necessary .csv files to build the NHFP Map with surrounding insitutions:

FellowsFile - Begins with a column of all host institutions in the history of the NHFP, and is followed by latitute and longitude, the total number of fellows that attended that insitution, and then three column with the total number of Hubble, Sagan, and Einstein fellows. 

MSIR2File - This file lists information on Minority Serving Institutions and R2 Institutions in the U.S. that match specific  criteria. The MSIs included in the map are Hispanic Serving Institutions, Historically Black Colleges and Universities (both defined by the Carnegie classification), and Black Serving Institutions (defined by NASA, comparable to Predominately Black Institutions in the Carnegie classification). This file also includes the following columns:
    - Classification: MSI label
    - Research Classification: R2 or not
    - Highest Level of Degree Available: Mostly blank
    - Physics Program (Y/N): Physics department, major, minor, or concentration available
    - Astronomy Program (Y/N): Astronomy department, major, minor, or concentration available
    - Astronomy Faculty (Y/N): At least 1 faculty with astronomy expertise
    - Numerous Astronomy Faculty (Y/N): 2 or more faculty with astronomy expertise
    - NOTES: Faculty names, department specifics, etc.
    - Latitude
    - Longitude
    - Address
    - Zip Code

The data from FellowsFile is displayed as red bubbles. The bubbles are centered on the lat and long of a host institution, and their size is proportional to the number of fellows that have attended that institution. The data from MSIR2File is displayed as multicolored pins whose colors correspond to their status as an HSI, BSI, HBCU or R2. The fellows red bubbles and the MSI and R2 pins are each individual layers whose appearance can be toggled in the top right menu on the map. 

PLEASE NOTE FOR FacultyMapMakingCode.py: For an MSI or R2 to be displayed on the faculty map (FacultyMapMakingCode.py), the insitution must have at least 2 faculty with an expertise in astronomy: this includes, by default, locations with astronomy departments, majors, minors, and concentrations. Institutions with only 1 astronomy faculty will not be displayed on the map. THEREFORE, ONLY THOSE INSTITUTIONS WHOSE "Numerous Astronomy Faculty" COLUMN IS LABELLED "Y" WILL APPEAR ON THE MAP AS A PIN.

PLEASE NOTE FOR DepartmentMapMakingCode.py: For an MSI or R2 to be displayed on the faculty map (DepartmentMapMakingCode.py), the insitution must have an astronomy program: this includes locations with astronomy departments, majors, minors, and concentrations. There is no requirement placed on the number of astronomy faculty. THEREFORE, THOSE INSTITUTIONS WHOSE "Astronomy Program" COLUMN IS LABELLED "Y" WILL APPEAR ON THE MAP AS A PIN.

TO TEST: Please run the file 'MAPMakingCode.py'. Thanks !
