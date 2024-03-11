import pandas as pd
import requests

def collect_data(countryCode, per_page, start_year, end_year):
    num_attributes = len(INDICATORS)
    num_year = end_year - start_year + 1
    
    indicator = [[] for _ in range(num_attributes + 2)] # init empty list for each attribute
    
    for i in range(num_attributes):
        url = f'{BASE_URL}countries/{countryCode}/indicators/{INDICATORS[i]}' # url corresponding to each feature
        url += f'?date={start_year}:{end_year}&per_page={per_page}&format=json'
        
        response = requests.get(url) # get the response
        if response.status_code == 200: # 200 OK
            json_file = response.json()[1] # dataframe formatted in json 
            for j in range(num_year):
                try: 
                    indicator[i].append(float(json_file[j]['value']))
                except:
                    indicator[i].append('None') # not a number

                if i == num_attributes - 1: # at the last attribute, append the value of Year and Country
                    try:
                        indicator[-2].append(json_file[j]['date'])
                    except:
                        indicator[-2].append('None')

                    try:
                        indicator[-1].append(json_file[j]['country']['value'])
                    except:
                        indicator[-1].append('None')
            
        else: # the response is not 200 OK
            print('Request URL failed: ', response.status_code)
            
    # convert the array of list to dataframe
    data = pd.DataFrame({'Country': indicator[-1],
                         'Year': indicator[-2],
                         'Population': indicator[0],
                         'Life Expectancy': indicator[1],
                         'Birth Rate': indicator[2], 
                         'Death Rate': indicator[3],
                         'Unemployment': indicator[4],
                         'Employment in Industry': indicator[5],
                         'Employment in Agriculture': indicator[6],
                         'GDP': indicator[7],
                            'Compulsory Education': indicator[8],
                            'Internet Users': indicator[9],
                            'National Income per Capita': indicator[10],
                            'Net Income from Abroad': indicator[11],
                            'Trade in Services': indicator[12],
                            'Imports of Goods and Services': indicator[13],
                            'Exports of Goods and Services': indicator[14]
                        })
    
    return data

def generate_world_dataset():
    all_countries_url = f'{BASE_URL}countries?format=json&per_page=300'
    response = requests.get(all_countries_url)

    if response.status_code == 200:
        countries_list = [country['id'] for country in response.json()[1]]
        data = pd.DataFrame()

        for country in enumerate(countries_list):
            data = pd.concat([data, collect_data(countryCode=country, per_page=100, start_year=1995, end_year=2022)], axis=0)

        return data
    else:
        print('Failed to retrieve list of countries: ', response.status_code)
        return None

BASE_URL = 'http://api.worldbank.org/v2/'
INDICATORS = ['SP.POP.TOTL', #population
                #status
                'SP.DYN.LE00.IN', #life expectancy
                'SP.DYN.CBRT.IN', #birth rate
                'SP.DYN.CDRT.IN', #death rate
                'SL.UEM.TOTL.ZS', #Unemployment
                'SL.IND.EMPL.ZS', #industry
                'SL.AGR.EMPL.ZS', #agriculture
                'NY.GDP.MKTP.CD', #GDP
                'SE.COM.DURS', #Compulsory education (years)
                'IT.NET.USER.ZS', #internet users
                'NY.ADJ.NNTY.PC.KD.ZG', #national income per capita
                'NY.GSR.NFCY.CD', #net income from abroad
                'BG.GSR.NFSV.GD.ZS', #trade in services
                'NE.IMP.GNFS.ZS', #imports of goods and services
                'NE.EXP.GNFS.ZS', #exports of goods and services
            ]

data = generate_world_dataset()

if data is not None:
    data.to_csv('world_data.csv', index=False)