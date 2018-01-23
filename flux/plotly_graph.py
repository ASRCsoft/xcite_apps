#version 4 with plotly
# run from terminal with:                                                                            
# export FLASK_APP=flaskFluxV4.py                                                                          
# python3 -m flask run --host=0.0.0.0 -p 9097 --with-threads
import plotly.plotly as py
from plotly.graph_objs import *
import plotly
import json
import io
import pandas as pd
import datetime
import re
from datetime import date, timedelta
from flux.models import Nysmesonet
#!flask/bin/python
# from flask import Flask, jsonify , request, make_response
# from flask_cors import CORS, cross_origin
# app = Flask(__name__)
# outside_sites = ['http://pireds.asrc.cestm.albany.edu']
# cors = CORS(app, resources={r"/*": {'origins': outside_sites}})

#change the actual units
units = {
    'FC_mass': 'mg m-2s-1',
    'LE': 'W m-2',
    'H': 'W m-2',
    'Rn': 'W m-2',
    'TAU': 'kg m-1 s-2',
    'Bowen_ratio': '',
    'USTAR': 'm s-1',
    'TKE': 'm2 s-2',
    'ZL': '',
    'MO_LENGTH': '',
    'U': 'm s-1',
    'V': 'm s-1',
    'W': 'm s-1',
    'T_SONIC': '°C',
    'CO2': 'μmolCO2 mol-1 (ppm)',
    'H2O': 'mmolCO2 mol-1',
    'SW_IN': 'W m-2',
    'SW_OUT': 'W m-2',
    'LW_IN': 'W m-2',
    'LW_OUT': 'W m-2',
    'G_6cm': 'W m-2'
}


#app = Flask(__name__)

def formatTime(params):
    dates = params['dates']
    datesF = datetime.datetime.strftime(dates, '%Y/%m/%dT')

def getCSV(params, dates):
    #timeMin = params['time_min']
    #timeMax = params['time_max']
    date = params['dates']
    datesStrp = dates.replace("/","")
    #20170909_FLUX_BURT_Flux_NYSMesonet.csv
    

    
    print('/flux/' + dates +'/' +datesStrp + '_FLUX_BURT_Flux_NYSMesonet.csv')

    # replace this code with database function!!
    df = pd.read_csv('/flux/' + dates + '/' + datesStrp + '_FLUX_BURT_Flux_NYSMesonet.csv')
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    
    
#    print(df.head())
#    print(df['CO2'])
    a = "arnold"
    df2 = pd.DataFrame() #creating an empty dataframe
    df2['datetime'] = pd.to_datetime(df['datetime'])
    df2['justDate']= df2['datetime'].dt.date
    df2['justHour'] = df2['datetime'].dt.hour
    df2['CO2']= df.loc[:,'CO2']
    
    datesNew = params['dates']
    df2['days_from'] = df2['datetime'] - datesNew
    df2['intDay'] = df2.days_from.dt.days 
    print(df2['justDate'])
    print(df2['justHour'])
    print(df2['intDay'])
    print(df2.tail())
    #df.set_index(['datetime'],inplace=True)
    #dfJson = df.loc[:,'justDate','justHour','CO2'].to_json()
    dfJson = df2.to_json()
    return dfJson

def testCSV(dateStartList, dateEndList, select, par):
    #timeMin = params['time_min']                                                                                                                                                    
    #timeMax = params['time_max']                                                                                                                                                    
    #date = params['dates']

    print(select)
    print("*********************")
    print(dateStartList)
    print("end list: ")
    print(dateEndList)
    print("*********************")
    

    fileExists = False
    
    #getting range of dates
    def perdelta(start, end, delta):
        curr = start
        while curr < end:
            yield curr
            curr += delta
            #ex date(2017, 10, 10)
    dfList = []
    #getting all of the selected csv files according to date and sotring them into a list

    # x=0
    # last = datetime.date(int(dateEndList[0]), int(dateEndList[1]), int(dateEndList[2]))
    # lastPlus = last + timedelta(days=1)
    # for curDate in perdelta(datetime.date(int(dateStartList[0]),int(dateStartList[1]),int(dateStartList[2])), lastPlus, timedelta(days=1)):
    #     try:
    #         #print(curDate)
    #         #curDateSTR = datetime.datetime.strptime(dates, '%Y/%m/%d')
    #         curDateSTR = curDate.strftime('%Y/%m/%d')
    #         #print(curDateSTR)
    #         #curDateInt = int(curDateSTR)
    #         dateSlash = curDateSTR.replace("-","/")
    #         dateStrp = curDateSTR.replace("/","")
    #         df74 = pd.read_csv('/flux/' + dateSlash + '/' + dateStrp + '_FLUX_'+ select +'_Flux_NYSMesonet.csv')
    #         df74['x_index'] = x
    #         dfList.append(df74)
    #         #print(dfList)
            
    #         fileExists = True
            
    #     except FileNotFoundError as e:
    #         print(e)
    #         x+=1

    # if(not fileExists):
    #     raise FileNotFoundError("no data found at all!!!")
    
    # #Combine a list of pandas dataframes to one pandas dataframe
    
    # dfFull = pd.concat(dfList)
    
    # print(dfFull.head())
    '''
    #changinge format for directries
    datesStrp = dates.replace("/","")
    #20170909_FLUX_BURT_Flux_NYSMesonet.csv
    print("*********************")
    print(datesStrp)
    print("*********************")
    
    
    print('/flux/' + dates +'/' +datesStrp + '_FLUX_BURT_Flux_NYSMesonet.csv')
    df = pd.read_csv('/flux/' + dates + '/' + datesStrp + '_FLUX_BURT_Flux_NYSMesonet.csv')

#    print(df.head())                                                                                                                                                                
    #    print(df['CO2'])                                                                          '''                                                                                      
    a = "arnold"

    first = datetime.date(int(dateStartList[0]),int(dateStartList[1]),int(dateStartList[2]))
    last = datetime.date(int(dateEndList[0]), int(dateEndList[1]), int(dateEndList[2]))
    lastPlus = last + timedelta(days=1)
    db_list = list(Nysmesonet.objects.filter(datetime__range=(first, lastPlus),
                                             stid__stid=select).values('datetime', par.lower()))
    #print(db_list)
    dfFull = pd.DataFrame(db_list)
    print(dfFull.head())
    print(par)
    print(select)

    
    df2 = pd.DataFrame() #creating an empty dataframe                                                                                                                                
    df2['datetime'] = pd.to_datetime(dfFull['datetime'])
    df2['justDate']= df2['datetime'].dt.date
    df2['justHour'] = df2['datetime'].dt.hour
    df2['justHour'] += df2['datetime'].dt.minute / 60 
    # df2['y_index'] = df2['justHour'] * 2
    # df2['x_index'] = dfFull['x_index']
    #df2['CO2']= dfFull.loc[:,'CO2']
    df2[str(par.lower())] = dfFull.loc[:,str(par.lower())]

    '''
    datesNew = params['dates']
    df2['days_from'] = df2['datetime'] - datesNew
    df2['intDay'] = df2.days_from.dt.days
    print(df2['justDate'])
    print(df2['justHour'])
    print(df2['intDay'])
    print(df2.tail())
    #df.set_index(['datetime'],inplace=True)                                                                                                                                         #[ [0.0.-0.7] ] day hour co2
    #dfJson = df.loc[:,'justDate','justHour','CO2'].to_json()
    '''
    
    df2.drop('datetime', axis=1, inplace=True)
    #df2.drop('intDay', axis=1, inplace=True)
    #df2.drop('days_from', axis=1, inplace=True)
    #writing to csv file
    #csvData = df2.loc[df2['justHour']>16].to_csv(header=False, index=False)

    df2.rename(columns={'justDate': 'Date', 'justHour': 'Time', str(par.lower()):'Temperature'}, inplace=True)
    csvData = df2.to_csv(header=True, index=False) 
    #dfJson = df2.to_json()

    # print(df2.head())
    
    # trace = go.Heatmap(z=df2['Temperature'],
    #                    x=df2['Date'],
    #                    y=df2['Time'])
    #print(df2.as_matrix)
    # trace = go.Heatmap(z=df2.as_matrix,
    #                    x=df2['Date'].unique(),
    #                    y=df2['Time'].unique())
    # data=trace
    # print(df2)
    z_mat = df2.pivot('Date', 'Time', 'Temperature')
    print(z_mat.head())

    data = Heatmap(z=z_mat.values.transpose().tolist(),
                   x=z_mat.index.values.tolist(),
                   y=z_mat.columns.tolist(),
                   colorscale='Viridis',
                   colorbar={'title':units[par]}
    )

    # py.iplot(data, filename='labelled-heatmap')
    layout = Layout(
        title='Heat map for site '+select+' showing '+par +' '+units[par]+' data',
        yaxis=YAxis(title='Hour'),
        xaxis=XAxis(title='Date',hoverformat='%e %b'),
        #zaxis=ZAxis(title=units[par]),
    )

    #return csvData
    #graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    dataDic = {"data":data, "layout":layout}
    # response = app.response_class(
    #     response=json.dumps(dataDic, cls=plotly.utils.PlotlyJSONEncoder),
    #     status=200,
    #     mimetype='application/json'
    # )
    return dataDic


# def plotly():
#     trace = go.Heatmap(,
#                    x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
#                    y=['Morning', 'Afternoon', 'Evening'])
#     data=[trace]
#     py.iplot(data, filename='labelled-heatmap')

# @app.route('/plot', methods=['GET'])
def flux_plot(request):
    # organize the request params
    #select = request.form.get('site')
    url_pars = request.GET
    
    par = url_pars['par']
    
    select = url_pars['site']
    #params = {}
    #datesOld = url_pars['dates']
    
    #multiDict = url_pars['dates']
    #print(multiDict)
    
    #multiDictF = multiDict.replace("/","")
    dateStart = url_pars['startDate']
    dateEnd = url_pars['endDate']
    dateStartList = dateStart.split("/")
    dateEndList = dateEnd.split("/")
    '''
    dfStart = pd.DataFrame() #creating an empty dataframe
                                                                                        \
                                                                                         
    dfStart['datetime'] = pd.to_datetime(df['datetime'])
    dfStart['justDate']= dfStart['datetime'].dt.date
    dfStart['justHour'] = dfStart['datetime'].dt.hour
    dateStartR = int(dateStart.replace("/",""))
    print(dateStartR)
    dateEndR = int(dateEnd.replace("/",""))
    
    #datesFull = multiDict.popitem()
    print(type(request))
    #print(datesFull)
    datesF = dates.replace("/", "")
    print(datesF)
    
    params['dates'] = datetime.datetime.strptime(dates, '%Y/%m/%d')
    #response = testCSV(params, dates)
    '''
    #response = testCSV(multiDict, dateStartR, dateEndR)
    response = testCSV(dateStartList, dateEndList, select, par)
    
    #time_min_str = request.args.get('time_min', type=str)
    #params['time_min'] = datetime.datetime.strptime(time_min_str, '%Y-%m-%dT%H:%M:00.000Z')
    #time_max_str = request.args.get('time_max', type=str)
    #params['time_max'] = datetime.datetime.strptime(time_max_str, '%Y-%m-%dT%H:%M:00.000Z')
    # response.headers['Content-Type'] = 'image/png'
    print(str(select))
    print(str(par))
    return response
