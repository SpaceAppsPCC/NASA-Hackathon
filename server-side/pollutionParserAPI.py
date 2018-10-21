import json
import urllib.request

def openURL(url):
    """
    Opens the argument url using urllib.request.urlopen
    Returns a dictionary created from the JSON data from the Launch Library Reading API
    :param url: string that contains the current url need to be read
    :return: a dictionary parsed from the JSON data from the Launch Library Reading API
    """

    #check if you can open the URL.  passes back errors if URL does not open properly
    try:            jsonFile = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print(e.code)
    except urllib.error.URLError as e:
        print(e.args)

    # reads the JSON into a string
    jsonStr = jsonFile.read()
    # decodes the JSON string into a format we can use in python
    parsed_json = json.loads(jsonStr)

    return parsed_json

def locationID():
    # Initial URL in string that we will use to get the first launch JSON data after 2018-10-20
    launchURL = "https://launchlibrary.net/1.4/launch/2018-10-20?offset=0"

    # offset keeps track of which launch number you receive from the JSON
    offset = 0

    # calls openURL(url) to get a format we can read in python
    # currently, returns a dictionary that have list values
    parsed_json = openURL(launchURL)

    total = parsed_json['total']

    # Can only get 10 launches per JSON
    # pageCount keeps track of total number of pages we need to open
    pageCount = total // 10
    if total % 10 > 0:
        pageCount += 1
    print(pageCount)

    # the dictionary we are going to put all the launch information into
    infoJson = {}

    # Iterate through every page (currently 196 as of 2018-10-19
    for j in range(pageCount):
        print(j)

        # a new call of openURL(launchURL) for each 10 launches
        parsed_json = openURL(launchURL)

        # Count keeps track of the total number of launches in the current JSON
        count = parsed_json['count']
        # print("count: " + str(count))

        for i in range(count):
            # currentCount keeps track of the current launch given from our API
            currentCount = j * 10 + i + 1

            # creates a dictionary for the current count
            infoJson[currentCount] = {}
            if(parsed_json['launches'][i]['location']['pads'] != []):
                infoJson[currentCount]['status'] = "AVAILABLE"
                infoJson[currentCount]['latitude'] = parsed_json['launches'][i]['location']['pads'][0]['latitude']
                infoJson[currentCount]['longitude'] = parsed_json['launches'][i]['location']['pads'][0]['longitude']
            else:
                # print("Error i: " + str(i))
                infoJson[currentCount]['status'] = "NOT_AVAILABLE"
                # print(parsed_json['launches'][i])

        offset += 10
        launchURL = "https://launchlibrary.net/1.4/launch/2018-10-20?offset=%d" % offset

    return infoJson

def aqiConvert(aqi):
    if(0 <= aqi and aqi <= 50):
        return "Good"
    elif(51 <= aqi and aqi <=100):
        return "Moderate"
    elif(101 <= aqi and aqi <= 150):
        return "Unhealthy for sensitive group"
    elif(151 <= aqi and aqi <= 200):
        return "Unhealthy"
    elif(201 <= aqi and aqi <= 300):
        return "Very unhealthy"
    else:
        return "Hazardous"


#Token key: 6c894193647dce8de89b9323650390f2a585e22e
def pollutionParser(dict):
    infoJson = {}
    for i in range(1,len(dict) + 1):
        # print("i begin:" + str(i))
        if(dict[i]['status'] != "NOT_AVAILABLE"):
            # infoJson[i] = i
            tokenKey = "cc69b5ca235fde1325f578d5758741dd64e12b0b"
            pollutionURL = "https://api.waqi.info/feed/"
            pollutionURL += "geo:" + str(dict[i]['latitude']) + ";" + str(dict[i]['longitude']) + "/?token=" + tokenKey

            # print(":" + pollutionURL)
            parsed_json = openURL(pollutionURL)

            infoJson[i] = {}

            infoJson[i]['status'] = "AVAILABLE"
            infoJson[i]['airrate'] = str(parsed_json['data']['aqi'])
            infoJson[i]['airquality'] = aqiConvert(parsed_json['data']['aqi'])
            infoJson[i]['dominentpol'] = parsed_json['data']['dominentpol']
            infoJson[i]['timemeasure'] = parsed_json['data']['time']['s']
            infoJson[i]['timezone'] = parsed_json['data']['time']['tz']
            infoJson[i]['station'] = parsed_json['data']['city']['name']
            infoJson[i]['stationID'] = parsed_json['data']['idx']
            infoJson[i]['latitude'] = str(parsed_json['data']['city']['geo'][0])
            infoJson[i]['longitude'] = str(parsed_json['data']['city']['geo'][1])
        else:
            infoJson[i] = {}
            infoJson[i]['status'] = "NOT_AVAILABLE"


        print("i: " + str(i))
        print(infoJson[i])
        print()

    return infoJson



# dict = {1:{'latitude': 68.478, 'longtitude': 28.30123},2:{'latitude': 150, 'longtitude': 300}}

dict = locationID()
# dict = {1: {'latitude': 5.239, 'longitude': -52.768}}
info = pollutionParser(dict)
print(info)






