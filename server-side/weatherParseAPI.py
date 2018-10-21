from apixu.client import ApixuClient, ApixuException
import json
import urllib.request

api_key = '1bcfea3b96ff42caa84234603182010'
client = ApixuClient(api_key)

def openURL(url):
    """
    Opens the argument url using urllib.request.urlopen
    Returns a dictionary created from the JSON data from the Launch Library Reading API
    :param url: string that contains the current url need to be read
    :return: a dictionary parsed from the JSON data from the Launch Library Reading API
    """

    #check if you can open the URL.  passes back errors if URL does not open properly
    try:
        jsonFile = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print(e.code)
    except urllib.error.URLError as e:
        print(e.args)

    # reads the JSON into a string
    jsonStr = jsonFile.read()
    # decodes the JSON string into a format we can use in python
    parsed_json = json.loads(jsonStr)

    return parsed_json

def getWeatherDict(locationDict):
    count = 1
    forecast = {}

    for location in locationDict:
        strLocation = str(locationDict[count]['latitude']) + ', ' + str(locationDict[count]['longitude'])
        ###########################
        # forecast weather
        ###########################

        forecast[count] = {}
        forecast[count] = client.getForecastWeather(q=strLocation, days=7)
        print(forecast)
        count += 1
        # "forecast" is a dict with a structure like this:
        '''
        {
            'current': {
                ...
            },
            'location': {
                ...
            },
            'forecast': {
                'forecastday': [{
                    'astro': {
                        'moonrise': '06:07 PM',
                        'moonset': '03:33 AM',
                        'sunrise': '05:29 AM',
                        'sunset': '08:32 PM'
                    },
                    'date': '2015-06-29',
                    'date_epoch': 1435536000,
                    'day': {
                        'avgtemp_c': 21.7,
                        'avgtemp_f': 71.1,
                        'condition': {
                            'code': 1063,
                            'icon': 'http://www.apixu.com/static/weather/64x64/day/176.png',
                            'text': 'Patchy rain nearby'
                        },
                        'maxtemp_c': 27.6,
                        'maxtemp_f': 81.7,
                        'maxwind_kph': 25.2,
                        'maxwind_mph': 15.7,
                        'mintemp_c': 17.5,
                        'mintemp_f': 63.5,
                        'totalprecip_in': 0.01,
                        'totalprecip_mm': 0.2
                    },
                    'hour': [{
                        'cloud': 16,
                        'condition': {
                            'code': 1000,
                            'icon': 'http://www.apixu.com/static/weather/64x64/night/113.png',
                            'text': 'Clear '
                        },
                        'dewpoint_c': 15.1,
                        'dewpoint_f': 59.2,
                        'feelslike_c': 18.4,
                        'feelslike_f': 65.1,
                        'heatindex_c': 18.4,
                        'heatindex_f': 65.1,
                        'humidity': 81,
                        'precip_in': 0.0,
                        'precip_mm': 0.0,
                        'pressure_in': 30.2,
                        'pressure_mb': 1007.0,
                        'temp_c': 18.4,
                        'temp_f': 65.1,
                        'time': '2015-06-29 00:00',
                        'time_epoch': 1435536000,
                        'will_it_rain': 0,
                        'will_it_snow': 0,
                        'wind_degree': 255,
                        'wind_dir': 'WSW',
                        'wind_kph': 25.6,
                        'wind_mph': 15.9,
                        'windchill_c': 18.4,
                        'windchill_f': 65.1
                    }]
                }]
            },
        }
        '''

    return forecast

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
        print(parsed_json)

        # Count keeps track of the total number of launches in the current JSON
        count = parsed_json['count']

        for i in range(count):
            # currentCount keeps track of the current launch given from our API
            currentCount = j * 10 + i + 1

            # creates a dictionary for the current count
            infoJson[currentCount] = {}

            infoJson[currentCount]['locationid'] = parsed_json['launches'][i]['location']['pads'][0]['id']

            # print(parsed_json['launches'][i]['location']['pads'][0]['latitude'])
            infoJson[currentCount]['latitude'] = parsed_json['launches'][i]['location']['pads'][0]['latitude']
            # print(parsed_json['launches'][i]['location']['pads'][0]['longitude'])
            infoJson[currentCount]['longitude'] = parsed_json['launches'][i]['location']['pads'][0]['longitude']

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

    # the dictionary we are going to put all the launch information into
    infoJson = {}

    # Iterate through every page (currently 196 as of 2018-10-19
    for j in range(pageCount):
        print(j)

        # a new call of openURL(launchURL) for each 10 launches
        parsed_json = openURL(launchURL)

        # Count keeps track of the total number of launches in the current JSON
        count = parsed_json['count']

        for i in range(count):
            # currentCount keeps track of the current launch given from our API
            currentCount = j * 10 + i + 1

            # creates a dictionary for the current count
            infoJson[currentCount] = {}

            infoJson[currentCount]['locationid'] = parsed_json['launches'][i]['location']['pads'][0]['id']

            # print(parsed_json['launches'][i]['location']['pads'][0]['latitude'])
            infoJson[currentCount]['latitude'] = parsed_json['launches'][i]['location']['pads'][0]['latitude']
            # print(parsed_json['launches'][i]['location']['pads'][0]['longitude'])
            infoJson[currentCount]['longitude'] = parsed_json['launches'][i]['location']['pads'][0]['longitude']
        offset += 10
        launchURL = "https://launchlibrary.net/1.4/launch/2018-10-20?offset=%d" % offset


    return infoJson

dict = getWeatherDict(locationID())
print(dict)