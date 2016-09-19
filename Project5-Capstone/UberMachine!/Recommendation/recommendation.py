
# coding: utf-8

# In[398]:

import pandas as pd
import numpy as np
import datetime
import sklearn.cross_validation as cv
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn import ensemble
from requests_forecast import Forecast
import operator
import simplejson, urllib
import re


# In[ ]:

randomForest = ensemble.RandomForestClassifier()
np.random.seed(23)

data = pd.read_csv('D:\\ubermachine.csv')
neighbor_lsit = sorted(data['Neighborhood'].unique())

data.drop(['Unnamed: 0'], 1, inplace=True)
data['Temp'] = (data.Max+data.Min)/2
data.drop(['Min','Max'], 1, inplace=True)


data['Neighborhood'].replace(to_replace= sorted(data['Neighborhood'].unique())
                             , value = range(1,len(data['Neighborhood'].unique())+1)
                             , inplace= True)


Total_Order = data.Total_Order
data.drop(['Total_Order','Taxi_Order','Uber_Order','Date'], 1, inplace=True)

amodel = randomForest.fit(data, Total_Order)


# In[425]:

current_location = [40.7081156, -73.9570696]
radius = 2


# In[429]:

recommendation(current_location, radius)


# In[426]:

def recommendation(current_location, radius):
    
    near_neighbor_table = get_neighborhoods(current_location, radius)
    near_neighbor_table = pd.DataFrame(near_neighbor_table).transpose().reset_index()
    near_neighbor_table.columns = ['Neighborhood', 'Lat', 'Lon']
    demand_table = pd.DataFrame([neighbor_lsit, get_demand_list()]).transpose()
    demand_table.columns = ['Neighborhood', 'Order']

    recommend = pd.merge(near_neighbor_table, demand_table, how='left', on='Neighborhood')

    travel_list = pd.DataFrame([])
    for i in range(len(recommend)):
        traval = get_distance(current_location, recommend['Lat'][i], recommend['Lon'][i])
        travel_list = travel_list.append(traval)
        travel_list.reset_index(drop=True, inplace=True)

    recommendation = pd.concat([recommend, travel_list], axis = 1)
    recommendation['Traffic'] = recommendation['Distance'].map(lambda x:float(x))/recommendation['Travel_Time'].map(lambda x:float(x))
    recommendation.drop(['Lat', 'Lon'], 1, inplace=True)
    recommendation.sort_values(by='Order', ascending=False, inplace=True)
    
    return recommendation


# In[15]:

def get_current_conditions():
    time = (datetime.datetime.now().hour * 6) + (datetime.datetime.now().minute/10)
    day = datetime.datetime.now().weekday() + 1
    if day == 6 or day == 7:
        weekend = 1
    else:
        weekend = 0


# In[346]:

def get_neighborhoods(current_location, radius):
    all_neighborhoods = {'Financial District': [40.7074909, -74.0112764], 'Williamsburg': [40.7081156, -73.9570696], 'South Bronx': [40.81767000000001, -73.91842609999999], 'Westerleigh-Castleton': [40.6342976, -74.1202417], 'Ridgewood': [40.7043986, -73.9018292], 'Huguenot': [41.4178712, -74.63099489999999], 'Clearview': [40.7804859, -73.7977928], 'Williams Bridge': [40.8780352, -73.8710014], 'Cobble Hill': [40.686536, -73.9962255], 'Inwood': [40.6220487, -73.74679890000002], 'Rossville': [40.5509808, -74.2032581], 'Harlem': [40.8115504, -73.9464769], 'Auburndale': [40.75411500000001, -73.7860276], 'Gramercy': [40.7376885, -73.98193619999999], 'Chelsea': [40.7465004, -74.00137370000002], 'Todt Hill': [40.6014342, -74.103441], 'University Heights': [40.85958610000001, -73.9109977], 'Greenwood': [42.13507, -77.6483236], 'Woodhaven-Richmond Hill': [40.6012236, -74.10949459999999], 'Park Slope': [40.6681038, -73.9805817], 'Chinatown': [40.7157509, -73.9970307], 'Bloomfield-Chelsea-Travis': [40.593718, -74.1662715], 'Corona': [40.7449859, -73.8642613], 'West Village': [40.735781, -74.0035709], 'Sunny Side': [40.7432759, -73.9196324], 'Soho': [40.723301, -74.0029883], 'Dyker Heights': [40.6187181, -74.0153231], 'Upper West Side': [40.7870106, -73.9753676], 'Queens Village': [40.7282239, -73.7948516], 'Bay Ridge': [40.6261638, -74.03294989999999], 'Wakefield-Williamsbridge': [40.8626913, -73.8578916], 'Jamaica': [40.702677, -73.7889689], "Prince's Bay": [40.5232804, -74.20032309999999], 'Bedford Park': [40.8700999, -73.8856912], 'East Village': [40.7264773, -73.98153370000001], 'Hunts Point': [40.8120246, -73.8801301], 'Gravesend-Sheepshead Bay': [40.5976048, -73.96513829999999], 'South Beach': [40.58290239999999, -74.0738631], 'Lower East Side': [40.715033, -73.9842724], 'Mapleton-Flatlands': [40.6193264, -73.9382998], 'Baychester': [40.8693862, -73.83308439999999], 'Upper East Side': [40.7735649, -73.9565551], 'Mariners Harbor': [40.6336287, -74.156292], 'Woodlawn-Nordwood': [42.797778, -78.8469439], 'Central Park': [40.7711329, -73.97418739999999], 'Woodside': [40.7512123, -73.90364869999999], 'Greenwich Village': [40.7335719, -74.0027418], 'Forest Hills': [40.718106, -73.8448469], 'Middle Village': [40.717372, -73.87425], 'Woodrow': [40.5394173, -74.19151769999999], 'Downtown': [40.7230084, -74.00063279999999], 'Morris Heights': [40.8515872, -73.9154069], 'Steinway': [40.7745459, -73.9037477], 'Rosebank': [40.6131912, -74.0726044], 'Utopia': [41.0988022, -74.1132145], 'Boerum Hill': [40.6848689, -73.9844722], 'Fort Green': [40.6920638, -73.97418739999999], 'Brownsville': [40.66308, -73.9095279], 'Bushwick': [40.6944282, -73.92128579999999], 'Ettingville': [40.5394463, -74.156292], 'Clinton': [43.0484029, -75.3785034], 'City Island': [40.8468202, -73.7874983], 'Midland Beach': [40.57149, -74.0931627], 'Borough Park': [40.6323009, -73.9888797], 'Parkchester': [40.8382522, -73.8566087], 'Astoria-Long Island City': [40.764202, -73.9150178], 'Garment District': [40.7547072, -73.9916342], 'Morningside Heights': [40.8089564, -73.96243270000001], 'Richmondtown': [40.5605312, -74.1474846], 'Flushing': [40.7674987, -73.833079], 'Union Port': [40.82754740000001, -73.8507279], 'East Harlem': [40.7957399, -73.93892129999999], 'Mott Haven': [40.8091068, -73.9228881], 'Washington Heights': [40.8417082, -73.9393554], 'Carroll Gardens': [40.6795331, -73.9991637], 'Tottensville': [40.5083408, -74.23554039999999], 'Flatbush': [40.6409217, -73.96243270000001], 'Laurelton': [40.6740861, -73.74484369999999], 'Canarsie': [40.6402325, -73.9060579], 'Tribeca': [40.7162692, -74.0086323], 'The Rockaways': [40.592658, -73.7977928], 'High Bridge': [40.8384699, -73.9271644], 'Midtown': [40.7549309, -73.9840195], 'Saintalbans': [40.6894086, -73.7654367], 'Queensboro Hill': [40.7553867, -73.951104], 'Tremont': [40.8447416, -73.8933596], 'Bensonhurst': [40.6112691, -73.9976946], 'Carnegie Hill': [40.7844653, -73.9550857], 'Douglastown-Little Neck': [40.7612957, -73.7330753], 'Murray Hill': [40.7478792, -73.9756567], 'Annandale': [42.0218762, -73.9095279], 'East Brooklyn': [40.6781784, -73.9441579], 'Nkew Gardens': [40.705695, -73.8272029], 'Oakwood': [40.5584751, -74.11518699999999], 'Battery Park': [40.7032775, -74.0170279], 'Springfield Gardens': [40.6626441, -73.7683784], 'Hamilton Heights': [40.8259597, -73.9496079], 'Charlestown-Richmond Valley': [42.3782065, -71.0602131], 'Great Kills': [40.5543273, -74.156292], 'Jackson Heights': [40.7556818, -73.8830701], 'Bedford-Stuyvesant': [40.6872176, -73.9417735], 'Morris Park': [40.8522006, -73.8507279], 'Sunset Park': [40.645532, -74.0123851], 'Country Club': [40.8430539, -73.8213213], 'Maspeth': [40.7294018, -73.9065883], 'Throggs Neck': [40.818399, -73.8213213], 'North Sutton Area': [40.7580204, -73.96016689999999], 'Soundview': [40.8251411, -73.86836970000002], 'Glendale': [40.698994, -73.8804427], 'Little Italy': [40.7191413, -73.9973273], 'Riverdale': [40.8940853, -73.9109977], 'Fordham': [40.8614705, -73.8905444], 'Eastchester': [40.95956049999999, -73.8095574], 'Clifton': [43.052284, -77.81472939999999], 'Yorkville': [43.1128475, -75.2709991], 'Kings Bridge': [40.8787108, -73.9051362], 'Spuyten Duyvil': [40.88116369999999, -73.9154069], 'New Brighton': [40.6404369, -74.090226]}
    available_neighborhoods = {}
    for neighborhood in all_neighborhoods:
        
        latitude_change =  (all_neighborhoods[neighborhood][0] - current_location[0]) * 69
        longitude_change = (all_neighborhoods[neighborhood][1] - current_location[1]) * 53
        distance = ((latitude_change)**2 + (longitude_change)**2)**.5
        
        if distance < radius:
            available_neighborhoods[neighborhood] = all_neighborhoods[neighborhood]
    return available_neighborhoods


# In[347]:

def get_current_conditions():
    time = (datetime.datetime.now().hour * 6) + (datetime.datetime.now().minute/10)
    day = datetime.datetime.now().weekday()
    if day == 6 or day == 7:
        weekend = 1
    else:
        weekend = 0

    # Using the dark skies API to get current temperture and if it's raining
    forecast = Forecast(apikey='7e616dba73de03ba9222e6ed09a3e88e', latitude=40.7246, longitude=-74.0021)
    current = forecast.get_currently()
    mean = current['temperature']
    rain = current['precipIntensity'] * 24

    conditions = [time, rain, day, weekend, mean]

    conditions  = np.array(conditions)
    conditions = conditions.reshape(1, -1)
    return conditions


# In[405]:

def get_distance(current_location, dest_lat, dest_lon):
    
    orig_coord = '{0},{1}'.format(current_location[0], current_location[1])
    dest_coord = '{0},{1}'.format(dest_lat, dest_lon)
    key = 'AIzaSyBU2bHLWxzS3JPTIEmP4tBQ-DrG6Xeb1AA'
    url_distance = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&departure_time=now&language=en-EN&key={2}".format(str(orig_coord),str(dest_coord),str(key))

    result= simplejson.load(urllib.urlopen(url_distance))

    driving_distanct_km = result['rows'][0]['elements'][0]['distance']['text']
    driving_distanct_mile = '{0}'.format(round(float(driving_distanct_km.split(' ')[0])*0.621371, 1))
    driving_time_traffic = result['rows'][0]['elements'][0]['duration_in_traffic']['text']
    driving_time_traffic = re.sub("[^0-9]", "", driving_time_traffic)
    df = pd.DataFrame([driving_distanct_mile, driving_time_traffic]).transpose()
    df.columns = ['Distance', 'Travel_Time']
    return df


# In[307]:

def get_demand_list():
    demand_list = []
    current = get_current_conditions()[0].tolist()
    for i in range(1,121):
        list = [i] + current
        demand = amodel.predict(np.array(list).reshape(1, -1))[0]
        demand_list.append(demand)

    return demand_list

