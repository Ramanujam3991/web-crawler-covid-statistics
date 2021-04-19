import pymongo
from datetime import date
import numpy as np
from scipy import stats

DB_URL = "mongodb+srv://dev:dev@cluster0.73vby.mongodb.net/sampleDB?retryWrites=true&w=majority"
DB_NAME = "sampleDB"
COLLECTION_NAME = "web_crawler"

databaseServers = pymongo.MongoClient(DB_URL)
database = databaseServers[DB_NAME]
collection = database[COLLECTION_NAME]
collection_3rd_day = database[COLLECTION_NAME+'_3rd_day']
collection_yesterday = database[COLLECTION_NAME+'_yesterday']
collection_4th_day = database[COLLECTION_NAME+'_4th_day']
collection_5th_day = database[COLLECTION_NAME+'_5th_day']
collection_future = database[COLLECTION_NAME+'_future']
countries =[]

def clear_data():
    print('Backing up data...')
    move_data(collection_4th_day, collection_5th_day)
    move_data(collection_3rd_day, collection_4th_day)
    move_data(collection_yesterday, collection_3rd_day)
    move_data(collection, collection_yesterday)
    print('Backing up Completed...')

    print('Clearing data....')
    collection.delete_many({})
    collection_future.delete_many({})
    print('Cleared data....')



def insertIntoDb(dictarr, table_name=''):
    global collection
    print('table_name>>>',table_name)
    if table_name=='':
        collection.insert_many(dictarr)
    else:
        print('table_name::',table_name)
        collection = database[COLLECTION_NAME+'_'+table_name]
        collection.insert_many(dictarr)


def move_data(source, destination):
    # Remove all documents, or make modifications.
    destination.remove({})
    docs = np.array([source.find({})])
    # Restore documents from the source collection.
    try:
        for doc in docs:
            destination.insert(doc)
        print('success in moving data')
    except:
        print('Exception in moving data')

def forecast_logic():
    row1 = collection.find()
    row2=collection_yesterday.find()
    row3=collection_3rd_day.find()
    row4=collection_4th_day.find()
    row5=collection_5th_day.find()
    data_frame = np.array([[row1],[row2],[row3],[row4],[row5]])# 2D array
    print('Forecast Logic:::')
    for doc in row1:
        countries.append(doc.get('Country,Other'))
    # for i in range(len(data_frame)):
    #     for tables in data_frame[0][i]:
    #         for d in tables:
    #             pass
    for country in countries:
        d1 = collection.find_one({'Country,Other':country})
        d2 = collection_yesterday.find_one({'Country,Other': country})
        d3 = collection_3rd_day.find_one({'Country,Other': country})
        d4 = collection_4th_day.find_one({'Country,Other': country})
        d5 = collection_5th_day.find_one({'Country,Other': country})
        NewCasesLst=[]
        NewDeathsLst=[]
        NewRecoveredLst=[]

        #Algorithm for calculating new cases on future date using MI and sciPy

        #New Cases
        if(str(d1.get('NewCases'))!= 'nan' and '+' in d1.get('NewCases')):
            NewCasesLst.append(int(str(d1.get('NewCases')).replace('+','').replace(',','')))
        if (str(d2.get('NewCases')) != 'nan' and '+' in d2.get('NewCases')):
            NewCasesLst.append(int(str(d2.get('NewCases')).replace('+','').replace(',','')))
        if (str(d3.get('NewCases')) != 'nan' and '+' in d3.get('NewCases')):
            NewCasesLst.append(int(str(d3.get('NewCases')).replace('+','').replace(',','')))
        if (str(d4.get('NewCases')) != 'nan' and '+' in d4.get('NewCases')):
            NewCasesLst.append(int(str(d4.get('NewCases')).replace('+','').replace(',','')))
        if (str(d5.get('NewCases')) != 'nan' and '+' in d5.get('NewCases')):
            NewCasesLst.append(int(str(d5.get('NewCases')).replace('+','').replace(',','')))
        #Calculate the mean
        newCasesMean = np.mean(NewCasesLst)
        # Calculate the median
        newCasesMedian = np.median(NewCasesLst)
        # Calculate the mode
        newCasesMode = stats.mode(NewCasesLst)
        # Calculate the Standard deviation
        newCasesStd = np.std(NewCasesLst)
        print('Mean::',newCasesMean)
        print('newCasesMedian::', newCasesMedian)
        print('newCasesMode::', newCasesMode)
        print('newCasesStd::', newCasesStd)
        newCasesTomorrow = 0
        #Algorithm logic
        #if standard deviation is less than one, then take the mean.
        #if standard deviation is greater than one, then find the mean between median and mode and then finally add standard deviation to the resultant. Easy!
        if str(newCasesStd) != 'nan':
            if newCasesStd <=1:
                newCasesTomorrow = newCasesMean
            elif len(newCasesMode[0])>0:
                newCasesTomorrow = newCasesMedian+newCasesStd
            else:
                newCasesTomorrow = np.mean([newCasesMedian,newCasesMode[0][0]])+newCasesStd
        print('newCasesTomorrow::',newCasesTomorrow)


        # New Deaths
        if (str(d1.get('NewDeaths')) != 'nan' and '+' in d1.get('NewDeaths')):
            NewDeathsLst.append(int(str(d1.get('NewDeaths')).replace('+', '').replace(',', '')))
        if (str(d2.get('NewDeaths')) != 'nan' and '+' in d2.get('NewDeaths')):
            NewDeathsLst.append(int(str(d2.get('NewDeaths')).replace('+', '').replace(',', '')))
        if (str(d3.get('NewDeaths')) != 'nan' and '+' in d3.get('NewDeaths')):
            NewDeathsLst.append(int(str(d3.get('NewDeaths')).replace('+', '').replace(',', '')))
        if (str(d4.get('NewDeaths')) != 'nan' and '+' in d4.get('NewDeaths')):
            NewDeathsLst.append(int(str(d4.get('NewDeaths')).replace('+', '').replace(',', '')))
        if (str(d5.get('NewDeaths')) != 'nan' and '+' in d5.get('NewDeaths')):
            NewDeathsLst.append(int(str(d5.get('NewDeaths')).replace('+', '').replace(',', '')))
        # Calculate the mean
        newDeathsMean = np.mean(NewDeathsLst)
        # Calculate the median
        newDeathsMedian = np.median(NewDeathsLst)
        # Calculate the mode
        newDeathsMode = stats.mode(NewDeathsLst)
        # Calculate the Standard deviation
        newDeathsStd = np.std(NewDeathsLst)

        newDeathsTomorrow = 0
        # Algorithm logic
        # if standard deviation is less than one, then take the mean.
        # if standard deviation is greater than one, then find the mean between median and mode and then finally add standard deviation to the resultant. Easy!
        if str(newDeathsStd) != 'nan':
            if newDeathsStd <= 1:
                newDeathsTomorrow = newDeathsMean
            elif len(newDeathsMode[0]) > 0:
                newDeathsTomorrow = newDeathsMedian + newDeathsStd
            else:
                newDeathsTomorrow = np.mean([newDeathsMedian, newDeathsMode[0][0]]) + newDeathsStd
        print('newDeathsTomorrow::', newDeathsTomorrow)


        # New Recovered
        if (str(d1.get('NewRecovered')) != 'nan' and '+' in d1.get('NewRecovered')):
            NewRecoveredLst.append(int(str(d1.get('NewRecovered')).replace('+', '').replace(',', '')))
        if (str(d2.get('NewRecovered')) != 'nan' and '+' in d2.get('NewRecovered')):
            NewRecoveredLst.append(int(str(d2.get('NewRecovered')).replace('+', '').replace(',', '')))
        if (str(d3.get('NewRecovered')) != 'nan' and '+' in d3.get('NewRecovered')):
            NewRecoveredLst.append(int(str(d3.get('NewRecovered')).replace('+', '').replace(',', '')))
        if (str(d4.get('NewRecovered')) != 'nan' and '+' in d4.get('NewRecovered')):
            NewRecoveredLst.append(int(str(d4.get('NewRecovered')).replace('+', '').replace(',', '')))
        if (str(d5.get('NewRecovered')) != 'nan' and '+' in d5.get('NewRecovered')):
            NewRecoveredLst.append(int(str(d5.get('NewRecovered')).replace('+', '').replace(',', '')))
        # Calculate the mean
        newRecoveredMean = np.mean(NewRecoveredLst)
        # Calculate the median
        newRecoveredMedian = np.median(NewRecoveredLst)
        # Calculate the mode
        newRecoveredMode = stats.mode(NewRecoveredLst)
        # Calculate the Standard deviation
        newRecoveredStd = np.std(NewRecoveredLst)

        newRecoveredTomorrow = 0
        # Algorithm logic
        # if standard deviation is less than one, then take the mean.
        # if standard deviation is greater than one, then find the mean between median and mode and then finally add standard deviation to the resultant. Easy!
        if str(newRecoveredStd) != 'nan':
            if newRecoveredStd <= 1:
                newRecoveredTomorrow = newRecoveredMean
            elif len(newRecoveredMode[0]) > 0:
                newRecoveredTomorrow = newRecoveredMedian + newRecoveredStd
            else:
                newRecoveredTomorrow = np.mean([newRecoveredMedian, newRecoveredMode[0][0]]) + newRecoveredStd
        print('newRecoveredTomorrow::', newRecoveredTomorrow)

        data = {'Country,Other':country,'NewCases':newCasesTomorrow,'NewDeaths':newDeathsTomorrow,'newRecoveredTomorrow':newRecoveredTomorrow}
        collection_future.insert_one(data)