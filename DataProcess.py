# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 14:13:28 2020

@author: marcelo.oliveira
"""
import pandas as pd 
pd.set_option('display.float_format', '{:.2f}'.format)


def audience_treatment(audiencePath):
    #lê o arquivo de audiencia
    audienceDf = pd.read_csv(audiencePath,sep=',')
    
    #Aqui são criados alguns campos necessários para o calculo final
    audienceDf['date'] = pd.to_datetime(audienceDf['exhibition_date'])
    audienceDf['weekday'] = audienceDf['date'].dt.day_name()
    audienceDf['dayofWeek'] = audienceDf['date'].dt.dayofweek
    audienceDf['month'] = audienceDf['date'].dt.month
    
    #Ao agrupar por mes e semana, é possivel calcular a mediana para os mesmos dias da semana para cada programa e sinal
    audienceGrouped = audienceDf.groupby(['signal','program_code','month','weekday'],as_index=False)['average_audience'].median()   
    audienceGrouped.rename(columns={'average_audience':'predicted_audience'},inplace=True)
    #Ao agrupar foi gerado um novo dataframe que contem a mediana, nesse caso é necessário fazer um novo merge com o dataframe original para obter a mediana
    audiencePredictedDf = audienceDf.merge(audienceGrouped, on=['signal','program_code','month','weekday'])
   
    return audiencePredictedDf

def merge_dataframes(inventoryPath, audienceDf):
    #Lê o arquivo de inventário
    inventoryDf = pd.read_csv(inventoryPath,sep=';')
    inventoryDf['date'] = pd.to_datetime(inventoryDf['date'])
    
    #O dataframe final é criado 
    finalDf= pd.merge(audienceDf[['signal','program_code','date','weekday','predicted_audience']], inventoryDf[['signal','program_code','date','available_time']], on=['signal','program_code','date'])
    finalDf['date']= finalDf['date'].dt.strftime('%Y-%m-%d')
    
    return finalDf
    
    
def convert_df_to_json(dataframeFinal):
    import json
    d = dataframeFinal.to_dict(orient='records')
    j = json.dumps(d)
    l = json.loads(j)
    dict_final = dict(list(enumerate(l)))
    return dict_final
   
    
'''
Métodos para busca de valores dentro do dataframe 
'''

'''
    Busca dentro do dataframe signal e program_code e ao validar retorna um objeto Json 
'''
def fetch_by_program_signal(dataframe, signal,program_code):
    #pesquisa se o signal e program_code estão no dataframe
    signal, program_code = str.upper(signal),str.upper(program_code)
    resultJsonDf = dataframe[(dataframe['signal']==signal) & (dataframe['program_code']==program_code)]
    #converte o dataframe em json 
    if resultJsonDf.empty:
        return 'Signal ou program_code não encontrados'
    else:
        return convert_df_to_json(resultJsonDf)

'''
    Busca dentro do dataframe o periodo filtrado e ao validar retorna um objeto Json 
'''    
def fetch_signal_program_by_date(dataframe, data_inicial , data_final):
    import numpy as np
    #pesquisa se o signal e program_code estão no dataframe

    #Valida se data final é maior que a data inicial
    validaData = (pd.to_datetime(data_final)-pd.to_datetime(data_inicial))
    validaData = validaData / np.timedelta64(1,'D')
    
    if validaData > 0:
        resultJsonDf = dataframe[(dataframe['date']>=data_inicial) & (dataframe['date']<=data_final)]                                                                  
        #converte o dataframe em json 
        if resultJsonDf.empty:
            return 'Signal ou program_code não encontrados'
        else:
            return convert_df_to_json(resultJsonDf)
    else:
        return 'Data Invalida'
                             
                             
#-------------------------------------------------------#                             
                             

inventoryPath = 'tvaberta_inventory_availability.csv'
audiencePath = 'tvaberta_program_audience.csv'
           
            
audienceDf = audience_treatment(audiencePath)
dfFinal = merge_dataframes(inventoryPath,audienceDf)
dict_final = convert_df_to_json(dfFinal) 

