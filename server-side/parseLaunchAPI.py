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

def parseLaunch():

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
            #currentCount keeps track of the current launch given from our API
            currentCount = j * 10 + i + 1

            #creates a dictionary for the current count
            infoJson[currentCount] = {}

            # The information we care about currently is the launch name, launch start time, launch location name, coordinates
            # and mission description if applicable

            infoJson[currentCount]['name'] = parsed_json['launches'][i]['name']
            # print(parsed_json['launches'][i]['name'])
            infoJson[currentCount]['launchStart'] = parsed_json['launches'][i]['windowstart']
            # print(parsed_json['launches'][i]['windowstart'])
            infoJson[currentCount]['launchEnd'] = parsed_json['launches'][i]['windowend']
            # print(parsed_json['launches'][i]['location']['pads'][0]['name'])
            infoJson[currentCount]['location'] = parsed_json['launches'][i]['location']['pads'][0]['name']
            # print(parsed_json['launches'][i]['location']['pads'][0]['latitude'])
            infoJson[currentCount]['latitude'] = parsed_json['launches'][i]['location']['pads'][0]['latitude']
            # print(parsed_json['launches'][i]['location']['pads'][0]['longitude'])
            infoJson[currentCount]['longitude'] = parsed_json['launches'][i]['location']['pads'][0]['longitude']

            try:
                print(parsed_json['launches'][i]['missions'][0]['description'])
                infoJson[currentCount]['mission'] = parsed_json['launches'][i]['missions'][0]['description']
            except IndexError:
                infoJson[currentCount]['mission'] = 'No mission information provided'

        offset += 10
        launchURL = "https://launchlibrary.net/1.4/launch/2018-10-20?offset=%d"%offset

    return infoJson



parseLaunch()