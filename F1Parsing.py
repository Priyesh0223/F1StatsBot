import requests
import json

#Get Driver Standing For A Given Year And Return A List Containing The Data
def driverStandingList(year):
    url = "http://ergast.com/api/f1/"+year+"/driverStandings.json"
    req = requests.get(url)
    driverDict = req.json()
    driverDict = driverDict.get('MRData').get('StandingsTable').get('StandingsLists')
    driverList = []

    for item in driverDict[0]['DriverStandings']:
        driverList.append({'position'   :item['position'],
                           'name'       :item['Driver']['givenName'] 
                                 + " " + item['Driver']['familyName'],
                           'constructor':item['Constructors'][0]['name'],
                           'points'     :item['points'],
                           'wins'       :item['wins']})
    return driverList
        
#Get Constructor Standing For A Given Year And Return A List Containing The Data        
def constructorStandingList(year):
    url = "http://ergast.com/api/f1/"+year+"/constructorStandings.json"
    req = requests.get(url)
    constructorDict = req.json()
    constructorDict = constructorDict.get('MRData').get('StandingsTable').get('StandingsLists')
    constructorList = []

    for item in constructorDict[0]['ConstructorStandings']:
        constructorList.append({'position'   :item['position'],
                                'constructor':item['Constructor']['name'],
                                'points'     :item['points'],
                                'wins'       :item['wins']})
    return constructorList


#Return Reddit Formatted String
def driverStanding(list):
    str = ("Pos|Driver|Constructor|Points|Wins" + "\n" +
           ":--|:--|:--|:--|:--" + "\n")
    for item in list:
        str = str + (item.get('position')+"|"+
                    item.get('name')+"|"+
                    item.get('constructor')+"|"+
                    item.get('points')+"|"+
                    item.get('wins')+ "\n")
    return str

#Return Reddit Formatted String    
def constructorStandings(list):
    str = ("Pos|Constructor|Points|Wins" + "\n" +
           ":--|:--|:--|:--" + "\n")
    for item in list:
        str = str + (item.get('position')+"|"+
                    item.get('constructor')+"|"+
                    item.get('points')+"|"+
                    item.get('wins')+ "\n")
    return str
