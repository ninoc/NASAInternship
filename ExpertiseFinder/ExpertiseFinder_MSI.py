import pandas as pd
import ads

################################################################################################################################################################################################################################################################################################################################################################################################

def expertiseFinder(token, directorypath, rawFile, start, count):    
    '''
    This function's purpose is to process faculty data using ADS data to determine each researcher's astronomical expertise. To achieve this goal, the function first must be given an ADS API token ('token'), a .csv file with the data to be processed ('fileName'), the starting row index of that data where the function will begin processing (start), and the amount of rows following that start point to continue processing (count). The reason these last two arguments are included is to limit the number of queries this function processes; ADS API has a limit of 5000 queries per token per day, which if exceeded, will result in a loss of data from this function. 
    
    The steps followed throughout this function will be explained as they come along.
    
    NOTE: This version of the expertiseFinder function only queries people's names (and no affs) in ADS, but DOES use name and institution as an important condition in the post-query section (STEP 6). This can be considered the function with medium strictness in its search criteria.
    '''
    
    # STEP 1: Import original data file. This file should be a .csv with columns representing at LEAST LastName, FirstName and Institution Name. According to the start and count values taken at Step 0 of this program, in this step, I select only the desired indecies of the data frame.
    ads.config.token = token
    
    rawDf = rawFile
    
    end = start+count
    rawDf = rawDf[start:end]
    
    # STEP 2: Once the data file is imported, pull out the important data:
    rawNames = list(rawDf['LastName, FirstName'])
    rawInsts = list(rawDf['Institution Name'])
    
    # STEP 3: Search ADS API to find queries matching the first author requirement.  
    queryData = []
    queryNames = []
    queryInsts = []
    for i in range(len(rawNames)):
        name = rawNames[i]
        inst = rawInsts[i]
        
        queries = ads.SearchQuery(first_author = name, property = 'refereed', sort = 'citation_count')
        
        queryData.append(queries)
        queryNames.append(name)
        queryInsts.append(inst)
        
    searchQueries = [queryNames, queryInsts, queryData]
    
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
            ## print(abstract)
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
    
    #for row in paperSearchDf.values:
        #bibcode = row[3]
        #year = row[5]
        #if year < 1979:
            #paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
    
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
    ## print(cleanDataDf)
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

    # STEP 8: Find the top 10 words, bigrams, and trigrams of the mergedDataDf.
    top10Dict = {'Top 10 Words':[], 
                 'Top 10 Bigrams':[],
                 'Top 10 Trigrams':[]}
     
    for row in mergedDataDf.values:
        abstracts = row[8]
         
        top10words = topwords(abstracts)
        top10bigrams = topbigrams(abstracts)
        top10trigrams = toptrigrams(abstracts)
         
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
         
        top10words = topwords(abstracts)
        top10bigrams = topbigrams(abstracts)
        top10trigrams = toptrigrams(abstracts)
         
        top10DirtyDict['Top 10 Words'].append(top10words)
        top10DirtyDict['Top 10 Bigrams'].append(top10bigrams)
        top10DirtyDict['Top 10 Trigrams'].append(top10trigrams)
        
    top10DirtyDf = mergedDirtyDf
    top10DirtyDf['Top 10 Words'] = top10DirtyDict['Top 10 Words']
    top10DirtyDf['Top 10 Bigrams'] = top10DirtyDict['Top 10 Bigrams']
    top10DirtyDf['Top 10 Trigrams'] = top10DirtyDict['Top 10 Trigrams']
    
    # STEP 9: Return that Data Frame ! (And the dirty one.)
    return top10Df, top10DirtyDf

################################################################################################################################################################################################################################################################################################################################################################################################

def expertiseFinderName(token, directorypath, rawFile, start, count):    
    '''
    This function's purpose is to process faculty data using ADS data to determine each researcher's astronomical expertise. To achieve this goal, the function first must be given an ADS API token ('token'), a .csv file with the data to be processed ('fileName'), the starting row index of that data where the function will begin processing (start), and the amount of rows following that start point to continue processing (count). The reason these last two arguments are included is to limit the number of queries this function processes; ADS API has a limit of 5000 queries per token per day, which if exceeded, will result in a loss of data from this function. 
    
    The steps followed throughout this function will be explained as they come along.
    
    NOTE: This version of the expertiseFinder function only queries people's names (and no affs), and does not use affiliation and name at the same time in the post-query section (STEP 6). This can be considered the function with the least strict query criteria. 
    '''
    
    # STEP 1: Import original data file. This file should be a .csv with columns representing at LEAST LastName, FirstName and Institution Name. According to the start and count values taken at Step 0 of this program, in this step, I select only the desired indecies of the data frame.
    ads.config.token = token
    
    rawDf = rawFile
    
    end = start+count
    rawDf = rawDf[start:end]
    
    # STEP 2: Once the data file is imported, pull out the important data:
    rawNames = list(rawDf['LastName, FirstName'])
    rawInsts = list(rawDf['Institution Name'])
    
    # STEP 3: Search ADS API to find queries matching the first author requirement.  
    queryData = []
    queryNames = []
    queryInsts = []
    for i in range(len(rawNames)):
        name = rawNames[i]
        inst = rawInsts[i]
        
        queries = ads.SearchQuery(first_author = name, property = 'refereed', sort = 'citation_count')
        
        queryData.append(queries)
        queryNames.append(name)
        queryInsts.append(inst)
        
    searchQueries = [queryNames, queryInsts, queryData]
    
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
            ## print(abstract)
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
    
    #for row in paperSearchDf.values:
        #bibcode = row[3]
        #year = row[5]
        #if year < 1979:
            #paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
            
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
    ## print(cleanDataDf)
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

    # STEP 8: Find the top 10 words, bigrams, and trigrams of the mergedDataDf.
    top10Dict = {'Top 10 Words':[], 
                 'Top 10 Bigrams':[],
                 'Top 10 Trigrams':[]}
     
    for row in mergedDataDf.values:
        abstracts = row[8]
         
        top10words = topwords(abstracts)
        top10bigrams = topbigrams(abstracts)
        top10trigrams = toptrigrams(abstracts)
         
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
         
        top10words = topwords(abstracts)
        top10bigrams = topbigrams(abstracts)
        top10trigrams = toptrigrams(abstracts)
         
        top10DirtyDict['Top 10 Words'].append(top10words)
        top10DirtyDict['Top 10 Bigrams'].append(top10bigrams)
        top10DirtyDict['Top 10 Trigrams'].append(top10trigrams)
        
    top10DirtyDf = mergedDirtyDf
    top10DirtyDf['Top 10 Words'] = top10DirtyDict['Top 10 Words']
    top10DirtyDf['Top 10 Bigrams'] = top10DirtyDict['Top 10 Bigrams']
    top10DirtyDf['Top 10 Trigrams'] = top10DirtyDict['Top 10 Trigrams']
    
    # STEP 9: Return that Data Frame ! (And the dirty one.)
    return top10Df, top10DirtyDf

################################################################################################################################################################################################################################################################################################################################################################################################

def expertiseFinderInst(token, directorypath, rawFile, start, count):
    '''
    This function's purpose is to process faculty data using ADS data to determine each researcher's astronomical expertise. To achieve this goal, the function first must be given an ADS API token ('token'), a .csv file with the data to be processed ('fileName'), the starting row index of that data where the function will begin processing (start), and the amount of rows following that start point to continue processing (count). The reason these last two arguments are included is to limit the number of queries this function processes; ADS API has a limit of 5000 queries per token per day, which if exceeded, will result in a loss of data from this function. 
    
    The steps followed throughout this function will be explained as they come along.
    
    NOTE: This version of the expertiseFinder function queries ADS with BOTH NAME AND AFFILIATION (aff), but does not use affiliation and name at the same time in the post-query section (STEP 6). It can be considered the function with the strictest query criteria. 
    '''
    
    # STEP 1: Import original data file. This file should be a .csv with columns representing at LEAST LastName, FirstName and Institution Name. According to the start and count values taken at Step 0 of this program, in this step, I select only the desired indecies of the data frame.
    ads.config.token = token
    
    rawDf = rawFile
    
    end = start+count
    rawDf = rawDf[start:end]
    
    # STEP 2: Once the data file is imported, pull out the important data:
    rawNames = list(rawDf['LastName, FirstName'])
    rawInsts = list(rawDf['Institution Name'])
    
    # STEP 3: Search ADS API to find queries matching the first author requirement.  
    queryData = []
    queryNames = []
    queryInsts = []
    for i in range(len(rawNames)):
        name = rawNames[i]
        inst = rawInsts[i]
        
        queries = ads.SearchQuery(first_author = name, aff = inst, property = 'refereed', sort = 'citation_count')
        
        queryData.append(queries)
        queryNames.append(name)
        queryInsts.append(inst)
        
    searchQueries = [queryNames, queryInsts, queryData]
    
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
            ## print(abstract)
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
    
    #for row in paperSearchDf.values:
        #bibcode = row[3]
        #year = row[5]
        #if year < 1979:
            #paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
    
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
         
        if firstauthor in trueauthor:
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
    ## print(len(paperSearchDf))
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
    ## print(len(cleanDict))
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
    ## print(cleanDataDf)
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

    # STEP 8: Find the top 10 words, bigrams, and trigrams of the mergedDataDf.
    top10Dict = {'Top 10 Words':[], 
                 'Top 10 Bigrams':[],
                 'Top 10 Trigrams':[]}
     
    for row in mergedDataDf.values:
        abstracts = row[8]
         
        top10words = topwords(abstracts)
        top10bigrams = topbigrams(abstracts)
        top10trigrams = toptrigrams(abstracts)
         
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
         
        top10words = topwords(abstracts)
        top10bigrams = topbigrams(abstracts)
        top10trigrams = toptrigrams(abstracts)
         
        top10DirtyDict['Top 10 Words'].append(top10words)
        top10DirtyDict['Top 10 Bigrams'].append(top10bigrams)
        top10DirtyDict['Top 10 Trigrams'].append(top10trigrams)
        
    top10DirtyDf = mergedDirtyDf
    top10DirtyDf['Top 10 Words'] = top10DirtyDict['Top 10 Words']
    top10DirtyDf['Top 10 Bigrams'] = top10DirtyDict['Top 10 Bigrams']
    top10DirtyDf['Top 10 Trigrams'] = top10DirtyDict['Top 10 Trigrams']
    
    # STEP 9: Return that Data Frame ! (And the dirty one.)
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
