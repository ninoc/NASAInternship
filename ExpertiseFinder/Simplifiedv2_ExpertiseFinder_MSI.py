import pandas as pd
import ads
import requests
from TextAnalysis import *

################################################################################################################################################################################################################################################################################################################################################################################################

def step12(start, count, rawFile):
    '''
    This function performs steps 1 and 2 for the expertiseFinder.
    '''
     # STEP 1: Import original data file. According to the start and count values taken at Step 0 of this program, in this step, I select only the desired indecies of the data frame.    
    rawDf = rawFile
    
    end = start+count
    rawDf = rawDf[start:end]
    
    # STEP 2: Once the data file is imported, pull out the important data:
    rawNames = list(rawDf['LastName, FirstName'])
    rawInsts = list(rawDf['Institution Name'])
    
    return rawNames, rawInsts

################################################################################################################################################################################################################################################################################################################################################################################################

def step3(rawNames, rawInsts, affs = False):
    '''
    This function performs step 3 for the expertiseFinder. 
    
    The boolean in this function determines if affiliation will be used when searching for ADS papers or not. 
    '''
    # STEP 3: Search ADS API to find queries matching the first author and/or affiliation requirement.  
    queryData = []
    queryNames = []
    queryInsts = []
    
    for i in range(len(rawNames)):
        name = rawNames[i]
        inst = rawInsts[i]
        
        if affs == False:
            queries = ads.SearchQuery(first_author = '^'+name, 
                                      property = 'refereed', 
                                      sort = 'citation_count', 
                                      database = 'astronomy')
            queryData.append(queries)
            queryNames.append(name)
            queryInsts.append(inst)
            
        if affs == True:
            queries = ads.SearchQuery(first_author = '^'+name, 
                                      aff = inst, 
                                      property = 'refereed', 
                                      sort = 'citation_count', 
                                      database = 'astronomy')
            queryData.append(queries)
            queryNames.append(name)
            queryInsts.append(inst)
            
    searchQueries = [queryNames, queryInsts, queryData]
    
    return searchQueries

################################################################################################################################################################################################################################################################################################################################################################################################

def step4(searchQueries):
    '''
    This function performs step 4 in the expertiseFinder.
    '''
    # STEP 4: For every query in queryData, I now need to collect every bibcodes from that query's list of associated papers. 
    Bibcodes = []
    Names = []
    Insts = []
    for i in range(len(searchQueries[2])):
        query = searchQueries[2][i]
        inst = searchQueries[1][i]
        name = searchQueries[0][i]
        for paper in query:
            Bibcodes.append(paper.bibcode)
            Names.append(name)
            Insts.append(inst)
            
    return Bibcodes, Names, Insts

################################################################################################################################################################################################################################################################################################################################################################################################

def step5(Bibcodes, Names, Insts):
    '''
    This function performs step 5 in the expertiseFinder.
    '''
    # STEP 5: In this step, I loop through every entry in the Bibcodes list and use the ads package to find the associated data: ['author', 'bibcode', 'title', 'citation_count', 'year', 'keyword', 'aff', 'abstract']. 
    FirstAuthors = []
    Titles = []
    Years = []
    Keywords = []
    Affs = []
    Abstracts = []
    
    for bib in Bibcodes:
        info = list(ads.SearchQuery(bibcode = bib, fl = ['author', 'bibcode', 'title', 'citation_count', 'year', 'keyword', 'aff', 'abstract']))[0]

        try:
            FirstAuthors.append(info.author[0])
        except:
            FirstAuthors.append('None')

        try:
            Titles.append(info.title[0])
        except:
            Titles.append('None')

        try:
            Years.append(int(info.year))
        except:
            Years.append('None')

        try:
            Affs.append(info.aff[0])
        except:
            Affs.append('None')

        try:
            Keywords.append(info.keyword[0])
        except:
            Keywords.append('None')

        try:
            Abstracts.append(info.abstract)
        except:
            Abstracts.append('None')

    dataDict = {'First Author': FirstAuthors, 
                'True Author': Names, 
                'True Institution': Insts,
                'Bibcode': Bibcodes, 
                'Title': Titles, 
                'Year': Years, 
                'Keywords': Keywords, 
                'Affiliations': Affs, 
                'Abstract': Abstracts}

    paperSearchDf = pd.DataFrame(dataDict)
    
    return paperSearchDf

################################################################################################################################################################################################################################################################################################################################################################################################

def TAinFA_TAinAFFS(paperSearchDf, cleanDict):
    '''
    This function applies the following filter to results from step 5: Only papers with the true author name IN the first author name AND with the true institution IN the affiliations will be included in clean data.
    '''
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
         
        if trueauthor in firstauthor:
            if trueinst in affs:
                ## print(abstract)
                cleanDict['First Author'].append(firstauthor)
                cleanDict['True Author'].append(trueauthor)
                cleanDict['True Institution'].append(trueinst)
                cleanDict['Bibcode'].append(bibcode)
                cleanDict['Title'].append(title)
                cleanDict['Year'].append(year)
                cleanDict['Keywords'].append(keywords)
                cleanDict['Affiliations'].append(affs)
                cleanDict['Abstract'].append(abstract)

                paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
                
                #print(cleanDict)
                
                return paperSearchDf, cleanDict
            
        else:
            return paperSearchDf, cleanDict
                
#################################################################################################################################

def TAisFA(paperSearchDf, cleanDict):
    '''
    This function applies the following filter to results from step 5: Only papers with EXACTLY the same first author name as the true author name that was searched in ADS will be included in clean data.
    '''
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
         
        if trueauthor == firstauthor:
            ## print(abstract)
            cleanDict['First Author'].append(firstauthor)
            cleanDict['True Author'].append(trueauthor)
            cleanDict['True Institution'].append(trueinst)
            cleanDict['Bibcode'].append(bibcode)
            cleanDict['Title'].append(title)
            cleanDict['Year'].append(year)
            cleanDict['Keywords'].append(keywords)
            cleanDict['Affiliations'].append(affs)
            cleanDict['Abstract'].append(abstract)

            paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
            
            #print(cleanDict)
            
            return paperSearchDf, cleanDict
            
        else:
            return paperSearchDf, cleanDict

#################################################################################################################################

def TIinAFFS(paperSearchDf, cleanDict):
    '''
    This function applies the following filter to results from step 5: Only papers with EXACTLY the true institution name in their affiliation will be included in the clean data.
    '''
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
        
        if trueinst in affs:
            ## print(trueinst)
            cleanDict['First Author'].append(firstauthor)
            cleanDict['True Author'].append(trueauthor)
            cleanDict['True Institution'].append(trueinst)
            cleanDict['Bibcode'].append(bibcode)
            cleanDict['Title'].append(title)
            cleanDict['Year'].append(year)
            cleanDict['Keywords'].append(keywords)
            cleanDict['Affiliations'].append(affs)
            cleanDict['Abstract'].append(abstract)

            paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
            
            #print(cleanDict)
            
            return paperSearchDf, cleanDict
        
        else:
            return paperSearchDf, cleanDict
            
#################################################################################################################################

def JNinBIB(paperSearchDf, cleanDict):
    '''
    This function applies the following filter to results from step 5: Only papers with the appropriate journal names in their bibcodes will be included in the clean data.
    '''
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
         
        journalNames = ['ApJ', 'MNRAS', 'AJ', 'Nature', 'Science', 'PASP', 'AAS', 'arXiv', 'SPIE']
         
        for name in journalNames:
            if name in bibcode:
                ## print(abstract)
                cleanDict['First Author'].append(firstauthor)
                cleanDict['True Author'].append(trueauthor)
                cleanDict['True Institution'].append(trueinst)
                cleanDict['Bibcode'].append(bibcode)
                cleanDict['Title'].append(title)
                cleanDict['Year'].append(year)
                cleanDict['Keywords'].append(keywords)
                cleanDict['Affiliations'].append(affs)
                cleanDict['Abstract'].append(abstract)

                paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
                
                #print(cleanDict)
                
                return paperSearchDf, cleanDict

            else:
                return paperSearchDf, cleanDict
                
#################################################################################################################################

def TAinFA(paperSearchDf, cleanDict):
    '''
        This function applies the following filter to results from step 5: Only papers with the true author name IN the first author name will be included in the clean data.
    '''
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
         
        if trueauthor in firstauthor:
            ## print(abstract)
            cleanDict['First Author'].append(firstauthor)
            cleanDict['True Author'].append(trueauthor)
            cleanDict['True Institution'].append(trueinst)
            cleanDict['Bibcode'].append(bibcode)
            cleanDict['Title'].append(title)
            cleanDict['Year'].append(year)
            cleanDict['Keywords'].append(keywords)
            cleanDict['Affiliations'].append(affs)
            cleanDict['Abstract'].append(abstract)

            paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
            
            return paperSearchDf, cleanDict
        
        else:
            return paperSearchDf, cleanDict
            
################################################################################################################################################################################################################################################################################################################################################################################################
#for expertisefinder:
    #if TA in FA & if TI in AFFS
    #if TA == FA
    #if TI in AFFS
    #if JN in BIB
#for expertisefinderNAME:
    #if TA in FA
    #if TI in AFFS
    # if JN in BIB
#for expertisefinderINST:
    #if TA in FA
    #if TI in AFFS
    # if JN in BIB
    
def step6_expertiseFinder(paperSearchDf):
    '''
    This function, containing numerous smaller functions, performs step 6 in expertiseFinder.
    '''
    # STEP 6: My next job is to clean up this df by finding First Authors that match the True Author, True Institutions that are in the Affiliations, and Journal Names in the Bibcodes. 
    cleanDict = {'First Author':[],
                 'True Author': [],
                 'True Institution': [],
                 'Bibcode': [], 
                 'Title': [], 
                 'Year': [], 
                 'Keywords': [], 
                 'Affiliations': [], 
                 'Abstract': []}
    
    paperSearchDf = paperSearchDf[paperSearchDf['Year'] > 1979]
    
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
         
        if trueauthor in firstauthor:
            if trueinst in affs:
                ## print(abstract)
                cleanDict['First Author'].append(firstauthor)
                cleanDict['True Author'].append(trueauthor)
                cleanDict['True Institution'].append(trueinst)
                cleanDict['Bibcode'].append(bibcode)
                cleanDict['Title'].append(title)
                cleanDict['Year'].append(year)
                cleanDict['Keywords'].append(keywords)
                cleanDict['Affiliations'].append(affs)
                cleanDict['Abstract'].append(abstract)

                paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
                
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
         
        if trueauthor == firstauthor:
            ## print(abstract)
            cleanDict['First Author'].append(firstauthor)
            cleanDict['True Author'].append(trueauthor)
            cleanDict['True Institution'].append(trueinst)
            cleanDict['Bibcode'].append(bibcode)
            cleanDict['Title'].append(title)
            cleanDict['Year'].append(year)
            cleanDict['Keywords'].append(keywords)
            cleanDict['Affiliations'].append(affs)
            cleanDict['Abstract'].append(abstract)

            paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
    
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
        
        if trueinst in affs:
            ## print(trueinst)
            cleanDict['First Author'].append(firstauthor)
            cleanDict['True Author'].append(trueauthor)
            cleanDict['True Institution'].append(trueinst)
            cleanDict['Bibcode'].append(bibcode)
            cleanDict['Title'].append(title)
            cleanDict['Year'].append(year)
            cleanDict['Keywords'].append(keywords)
            cleanDict['Affiliations'].append(affs)
            cleanDict['Abstract'].append(abstract)

            paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
            
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
         
        journalNames = ['ApJ', 'MNRAS', 'AJ', 'Nature', 'Science', 'PASP', 'AAS', 'arXiv', 'SPIE']
         
        for name in journalNames:
            if name in bibcode:
                ## print(abstract)
                cleanDict['First Author'].append(firstauthor)
                cleanDict['True Author'].append(trueauthor)
                cleanDict['True Institution'].append(trueinst)
                cleanDict['Bibcode'].append(bibcode)
                cleanDict['Title'].append(title)
                cleanDict['Year'].append(year)
                cleanDict['Keywords'].append(keywords)
                cleanDict['Affiliations'].append(affs)
                cleanDict['Abstract'].append(abstract)

                paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
    
    dirtyDataDf = paperSearchDf
    cleanDataDf = pd.DataFrame(cleanDict)
    
    return cleanDataDf, dirtyDataDf

################################################################################################################################################################################################################################################################################################################################################################################################

def step6_expertiseFinderNameInst(paperSearchDf):
    '''
    This function, containing numerous smaller functions, performs step 6 in expertiseFinderName and expertiseFinderInst.
    '''
    # STEP 6: My next job is to clean up this df by finding First Authors that match the True Author, True Institutions that are in the Affiliations, and Journal Names in the Bibcodes. 
    cleanDict = {'First Author':[],
                 'True Author': [],
                 'True Institution': [],
                 'Bibcode': [], 
                 'Title': [], 
                 'Year': [], 
                 'Keywords': [], 
                 'Affiliations': [], 
                 'Abstract': []}
    
    paperSearchDf = paperSearchDf[paperSearchDf['Year'] > 1979]
    
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
         
        if trueauthor == firstauthor:
            ## print(abstract)
            cleanDict['First Author'].append(firstauthor)
            cleanDict['True Author'].append(trueauthor)
            cleanDict['True Institution'].append(trueinst)
            cleanDict['Bibcode'].append(bibcode)
            cleanDict['Title'].append(title)
            cleanDict['Year'].append(year)
            cleanDict['Keywords'].append(keywords)
            cleanDict['Affiliations'].append(affs)
            cleanDict['Abstract'].append(abstract)

            paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
    
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
        
        if trueinst in affs:
            ## print(trueinst)
            cleanDict['First Author'].append(firstauthor)
            cleanDict['True Author'].append(trueauthor)
            cleanDict['True Institution'].append(trueinst)
            cleanDict['Bibcode'].append(bibcode)
            cleanDict['Title'].append(title)
            cleanDict['Year'].append(year)
            cleanDict['Keywords'].append(keywords)
            cleanDict['Affiliations'].append(affs)
            cleanDict['Abstract'].append(abstract)

            paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
            
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        trueinst = row[2]
        bibcode = row[3]
        title = row[4]
        year = row[5]
        keywords = row[6]
        affs = row[7]
        abstract = row[8]
         
        journalNames = ['ApJ', 'MNRAS', 'AJ', 'Nature', 'Science', 'PASP', 'AAS', 'arXiv', 'SPIE']
         
        for name in journalNames:
            if name in bibcode:
                ## print(abstract)
                cleanDict['First Author'].append(firstauthor)
                cleanDict['True Author'].append(trueauthor)
                cleanDict['True Institution'].append(trueinst)
                cleanDict['Bibcode'].append(bibcode)
                cleanDict['Title'].append(title)
                cleanDict['Year'].append(year)
                cleanDict['Keywords'].append(keywords)
                cleanDict['Affiliations'].append(affs)
                cleanDict['Abstract'].append(abstract)

                paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
    
    dirtyDataDf = paperSearchDf
    cleanDataDf = pd.DataFrame(cleanDict)
    
    return cleanDataDf, dirtyDataDf

################################################################################################################################################################################################################################################################################################################################################################################################

def step7_cleanDf(cleanDataDf):
    '''
    This function performs the clean data merger from step 7 in expertiseFinder.
    '''
    # STEP 7: Now it's time to merge by True Author ! The input here is the data frame from the previous step, and the return is a merged data frame.
    cleanDataDf['Year']= cleanDataDf['Year'].astype(str)
    cleanDataDf['Abstract']= cleanDataDf['Abstract'].astype(str)
    
    mergedDataDf = cleanDataDf.groupby('True Author').aggregate({'True Institution':', '.join,
                                                                 'First Author':', '.join,
                                                                 'Bibcode':', '.join, 
                                                                 'Title':', '.join, 
                                                                 'Year':', '.join, 
                                                                 'Keywords':', '.join, 
                                                                 'Affiliations':', '.join, 
                                                                 'Abstract':', '.join}).reset_index()
    return mergedDataDf

#################################################################################################################################

def step7_dirtyDf(dirtyDataDf):
    '''
    This function performs the dirty data merger from step 7 in expertiseFinder.
    '''
    # STEP 7: Now it's time to merge by True Author ! The input here is the data frame from the previous step, and the return is a merged data frame.
    dirtyDataDf['Year'] = dirtyDataDf['Year'].astype(str)
    dirtyDataDf['Abstract'] = dirtyDataDf['Abstract'].astype(str)
    
    mergedDirtyDf = dirtyDataDf.groupby('True Author').aggregate({'True Institution':', '.join,
                                                                  'First Author':', '.join,
                                                                  'Bibcode':', '.join, 
                                                                  'Title':', '.join, 
                                                                  'Year':', '.join, 
                                                                  'Keywords':', '.join, 
                                                                  'Affiliations':', '.join, 
                                                                  'Abstract':', '.join}).reset_index()
    return mergedDirtyDf

################################################################################################################################################################################################################################################################################################################################################################################################

def step8(mergedDataDf, mergedDirtyDf, directorypath):
    '''
    This function performs step 8 in the expertiseFinder function.
    '''
    # STEP 8: Find the top 10 words, bigrams, and trigrams of the mergedDataDf.
    top10Dict = {'Top 10 Words':[], 
                 'Top 10 Bigrams':[],
                 'Top 10 Trigrams':[]}
     
    for row in mergedDataDf.values:
        abstracts = row[8]
         
        top10words = topwords(abstracts, directorypath)
        top10bigrams = topbigrams(abstracts, directorypath)
        top10trigrams = toptrigrams(abstracts, directorypath)
         
        top10Dict['Top 10 Words'].append(top10words)
        top10Dict['Top 10 Bigrams'].append(top10bigrams)
        top10Dict['Top 10 Trigrams'].append(top10trigrams)
        
    top10Df = mergedDataDf
    top10Df['Top 10 Words'] = top10Dict['Top 10 Words']
    top10Df['Top 10 Bigrams'] = top10Dict['Top 10 Bigrams']
    top10Df['Top 10 Trigrams'] = top10Dict['Top 10 Trigrams']
    
    
    top10DirtyDict = {'Top 10 Words':[], 
                      'Top 10 Bigrams':[],
                      'Top 10 Trigrams':[]}
     
    for row in mergedDirtyDf.values:
        abstracts = row[8]
         
        top10words = topwords(abstracts, directorypath)
        top10bigrams = topbigrams(abstracts, directorypath)
        top10trigrams = toptrigrams(abstracts, directorypath)
         
        top10DirtyDict['Top 10 Words'].append(top10words)
        top10DirtyDict['Top 10 Bigrams'].append(top10bigrams)
        top10DirtyDict['Top 10 Trigrams'].append(top10trigrams)
        
    top10DirtyDf = mergedDirtyDf
    top10DirtyDf['Top 10 Words'] = top10DirtyDict['Top 10 Words']
    top10DirtyDf['Top 10 Bigrams'] = top10DirtyDict['Top 10 Bigrams']
    top10DirtyDf['Top 10 Trigrams'] = top10DirtyDict['Top 10 Trigrams']
    
    return top10Df, top10DirtyDf

################################################################################################################################################################################################################################################################################################################################################################################################

def expertiseFinder(token, directorypath, rawFile, start, count):    
    '''
    This function's purpose is to process faculty data using ADS to determine each faculty's astronomical expertise. To achieve this goal, the function must first be given the following:
    token = an ADS API token (string)
    fileName = a .csv file with the data to be processed. This file should be a .csv with columns representing at LEAST LastName, FirstName and Institution Name. ('R2FacultyInfo_withoutNoInfoNoFac.csv')
    start = the starting row index of that data where the function will begin processing (int)
    count = the amount of rows following the start point to continue processing (int). 
    The reason these last two arguments are included is to limit the number of queries this function processes; ADS API has a limit of 5000 queries per token per day, which if exceeded, will result in a loss of data from this function. 
    
    The steps followed throughout this function will be explained as they come along.
    
    NOTE: This version of the expertiseFinder function only queries people's names (and no affs) in ADS, but DOES use name and institution as an important condition in the post-query section (STEP 6). This can be considered the function with medium strictness in its search criteria.
    '''
    ads.config.token = token
    
    # STEP 1 & STEP 2:
    rawNames, rawInsts = step12(start, count, rawFile)
    
    # STEP 3: 
    searchQueries = step3(rawNames, rawInsts, affs = False)
    
    # STEP 4: 
    Bibcodes, Names, Insts = step4(searchQueries)
            
    # STEP 5: 
    paperSearchDf = step5(Bibcodes, Names, Insts)

    # STEP 6: 
    cleanDataDf, dirtyDataDf = step6_expertiseFinder(paperSearchDf)

    # STEP 7: 
    mergedDataDf = step7_cleanDf(cleanDataDf)
    mergedDirtyDf = step7_dirtyDf(dirtyDataDf)

    # STEP 8: 
    top10Df, top10DirtyDf = step8(mergedDataDf, mergedDirtyDf, directorypath)
    
    # STEP 9: 
    return top10Df, top10DirtyDf

################################################################################################################################################################################################################################################################################################################################################################################################

def expertiseFinderName(token, directorypath, rawFile, start, count):    
    '''
    This function's purpose is to process faculty data using ADS to determine each faculty's astronomical expertise. To achieve this goal, the function must first be given the following:
    token = an ADS API token (string)
    fileName = a .csv file with the data to be processed. This file should be a .csv with columns representing at LEAST LastName, FirstName and Institution Name. ('R2FacultyInfo_withoutNoInfoNoFac.csv')
    start = the starting row index of that data where the function will begin processing (int)
    count = the amount of rows following the start point to continue processing (int). 
    The reason these last two arguments are included is to limit the number of queries this function processes; ADS API has a limit of 5000 queries per token per day, which if exceeded, will result in a loss of data from this function.    
    The steps followed throughout this function will be explained as they come along.
    
    NOTE: This version of the expertiseFinder function only queries people's names (and no affs), and does not use affiliation and name at the same time in the post-query section (STEP 6). This can be considered the function with the least strict query criteria. 
    '''
    ads.config.token = token

    # STEP 1 & STEP 2:
    rawNames, rawInsts = step12(start, count, rawFile)
    
    # STEP 3: 
    searchQueries = step3(rawNames, rawInsts, affs = False)
    
    # STEP 4: 
    Bibcodes, Names, Insts = step4(searchQueries)
            
    # STEP 5: 
    paperSearchDf = step5(Bibcodes, Names, Insts)

    # STEP 6: 
    cleanDataDf, dirtyDataDf = step6_expertiseFinderNameInst(paperSearchDf)

    # STEP 7: 
    mergedDataDf = step7_cleanDf(cleanDataDf)
    mergedDirtyDf = step7_dirtyDf(dirtyDataDf)

    # STEP 8: 
    top10Df, top10DirtyDf = step8(mergedDataDf, mergedDirtyDf, directorypath)
    
    # STEP 9: 
    return top10Df, top10DirtyDf

################################################################################################################################################################################################################################################################################################################################################################################################

def expertiseFinderInst(token, directorypath, rawFile, start, count):
    '''
    This function's purpose is to process faculty data using ADS to determine each faculty's astronomical expertise. To achieve this goal, the function must first be given the following:
    token = an ADS API token (string)
    fileName = a .csv file with the data to be processed. This file should be a .csv with columns representing at LEAST LastName, FirstName and Institution Name. ('R2FacultyInfo_withoutNoInfoNoFac.csv')
    start = the starting row index of that data where the function will begin processing (int)
    count = the amount of rows following the start point to continue processing (int). 
    The reason these last two arguments are included is to limit the number of queries this function processes; ADS API has a limit of 5000 queries per token per day, which if exceeded, will result in a loss of data from this function.    
    The steps followed throughout this function will be explained as they come along.
    
    NOTE: This version of the expertiseFinder function queries ADS with BOTH NAME AND AFFILIATION (aff), but does not use affiliation and name at the same time in the post-query section (STEP 6). It can be considered the function with the strictest query criteria. 
    '''
    ads.config.token = token

    # STEP 1 & STEP 2:
    rawNames, rawInsts = step12(start, count, rawFile)
    
    # STEP 3: 
    searchQueries = step3(rawNames, rawInsts, affs = True)
   
    # STEP 4: 
    Bibcodes, Names, Insts = step4(searchQueries)
            
    # STEP 5: 
    paperSearchDf = step5(Bibcodes, Names, Insts)

    # STEP 6: 
    cleanDataDf, dirtyDataDf = step6_expertiseFinderNameInst(paperSearchDf)

    # STEP 7: 
    mergedDataDf = step7_cleanDf(cleanDataDf)
    mergedDirtyDf = step7_dirtyDf(dirtyDataDf)

    # STEP 8: 
    top10Df, top10DirtyDf = step8(mergedDataDf, mergedDirtyDf, directorypath)
    
    # STEP 9: 
    return top10Df, top10DirtyDf

######################################################################################################################################################################################################################################################################################################################################################################################################

def dirtyCleaner_moreStrict(dirtyDf, cleanDf, ogDf):
    '''
    This function takes in a dirty data frame outputted from expertiseFinder and removes any names in the dirty spreadsheet that are already present in the clean spreadsheet. Thus, it leaves only data on people who are missing from the clean spreadsheet, and need more investigating. 
    It also returns a spreadsheet of names without any hits on ADS. The names in missingNames are those that are not present in either cleanDf or dirtyDf.
    '''
    ogDf = ogDf.reset_index(drop = True)
    ogNames = ogDf['LastName, FirstName']   
    ogInsts = ogDf['Institution Name']
    
    
            
    for row in dirtyDf.values:
        trueauthorDirty = row[0]
        for i in range(len(cleanDf['True Author'])):
            if trueauthorDirty == cleanDf['True Author'][i]:
                dirtyDf = dirtyDf[dirtyDf['True Author'] != trueauthorDirty]
                
    dirtyDf = dirtyDf.reset_index(drop = True)
    
    missingNames = ogNames
    missingInsts = ogInsts
    missingNames = pd.DataFrame({'LastName, FirstName': missingNames, 'Institution Name':missingInsts})
    
    for row1 in missingNames.values:
        name = row1[0]
        inst = row1[1]
        for row2 in cleanDf.values:
            cleanname = row2[0]
            if name == cleanname:
                missingNames = missingNames[missingNames['LastName, FirstName'] != name]
        for row3 in dirtyDf.values:
            dirtyname = row3[0]
            if name == dirtyname:
                missingNames = missingNames[missingNames['LastName, FirstName'] != name]
                
    missingNames = missingNames.reset_index(drop = True)
    
    
    return dirtyDf, cleanDf, missingNames

######################################################################################################################################################################################################################################################################################################################################################################################################

def dirtyCleaner_lessStrict(dirtyDf, cleanDf, ogDf):
    '''
    This function takes in a dirty data frame outputted from expertiseFinder and removes any names in the dirty spreadsheet that are already present in the clean spreadsheet. Thus, it leaves only data on people who are missing from the clean spreadsheet, and need more investigating. 
    It also returns a spreadsheet of names without any CLEAN hits on ADS. So, the missingNames return includes names that are not present in cleanDf, but ARE present in dirtyDf.
    '''
    ogDf = ogDf.reset_index(drop = True)
    ogNames = ogDf['LastName, FirstName']   
    ogInsts = ogDf['Institution Name']
    
    
            
    for row in dirtyDf.values:
        trueauthorDirty = row[0]
        for i in range(len(cleanDf['True Author'])):
            if trueauthorDirty == cleanDf['True Author'][i]:
                dirtyDf = dirtyDf[dirtyDf['True Author'] != trueauthorDirty]
                
    dirtyDf = dirtyDf.reset_index(drop = True)
    
    missingNames = ogNames
    missingInsts = ogInsts
    missingNames = pd.DataFrame({'LastName, FirstName': missingNames, 'Institution Name':missingInsts})
    
    for row1 in missingNames.values:
        name = row1[0]
        inst = row1[1]
        for row2 in cleanDf.values:
            cleanname = row2[0]
            if name == cleanname:
                missingNames = missingNames[missingNames['LastName, FirstName'] != name]
                
    missingNames = missingNames.reset_index(drop = True)
  
    
    return dirtyDf, cleanDf, missingNames

######################################################################################################################################################################################################################################################################################################################################################################################################

def expertiseFinder_singleName(token, directorypath, name, inst):
    '''
    This function's main goal is to take a given researcher's name and institution and find all of their associated papers on NASA ADS.
    
    token = an ads API token (string)
    directorypath = the file location of 'stopwords.txt' on your device (string)
    name = the name of the researcher in 'LastName, FirstName MiddleInitial.' format (string)
    inst = the institute of the researcher (string)
    
    This function returns a data frame with information on the researcher's expertise. This includes relevant papers, and the top 10 words, bigrams, and trigrams in their abstracts.
    '''
    ads.config.token = token

    # STEP 1 & 2:
    # SKIP
    
    # STEP 3:
    querydata = []
    queryname = []
    queryinst = []
    queries = ads.SearchQuery(first_author = '^'+name, 
                              aff = inst, 
                              property = 'refereed', 
                              sort = 'citation_count', 
                              database = 'astronomy')
    querydata.append(queries)
    queryname.append(name)
    queryinst.append(inst)
            
    searchQueries = [queryname, queryinst, querydata]  
    
    # STEP 4:
    bibcodes = []
    names = name
    insts = inst
    
    inst = searchQueries[1]
    name = searchQueries[0]
    
    for paper in queries:
        bibcodes.append(paper.bibcode)
            
    # STEP 5:
    paperSearchDf = step5(bibcodes, names, insts)
    
    # STEP 6:
    cleanDataDf, dirtyDataDf = step6_expertiseFinder(paperSearchDf)
    
    # STEP 7: 
    mergedDataDf = step7_cleanDf(cleanDataDf)
    mergedDirtyDf = step7_dirtyDf(dirtyDataDf)

    # STEP 8: 
    top10Df, top10DirtyDf = step8(mergedDataDf, mergedDirtyDf, directorypath)
    
    # STEP 9: 
    return top10Df, top10DirtyDf    
