import json
import urllib.request
import sqlite3
from parseLaunchAPI import parseLaunch

def readParseJSON(url):
    #this is only for test purposes
    #gets a URL and parse the JSON
    #return a parsed JSON
    #test url for launches: "https://launchlibrary.net/1.4/launch/next/5"
    jsonFile = urllib.request.urlopen(url)
    jsonStr = jsonFile.read()
    parsed_json = json.loads(jsonStr)

    return parsed_json

def insertIntoDB(parsedJSON, dbname):
    #this is only for test purposes
    #gets a JSON, database name, and list of fields 
    #for now field names are hard coded
    #add items to the db
    #return void

    conn = sqlite3.connect(dbname)
    cursorObj = conn.cursor()

    #This only works for launch info
    launches = parsedJSON['launches']

    # Create table with id, missionname, windowstart, and windowend
    
    cursorObj.execute('''CREATE TABLE IF NOT EXISTS launchinfo (id INTEGER PRIMARY KEY,missionname text, windowstart text, windowend text)''')

    for i in range(len(launches)):
        idnum = int(parsedJSON['launches'][i]['id'])
        name = str(parsedJSON['launches'][i]['name'])
        windowstart = str(parsedJSON['launches'][i]['windowstart'])
        windowend = str(parsedJSON['launches'][i]['windowend'])
        executableStr = "INSERT INTO launchinfo ('id', 'missionname', 'windowstart', 'windowend') VALUES (%d, '%s', '%s', '%s')" % (idnum, name, windowstart, windowend)
        cursorObj.execute(executableStr)

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

url = "https://launchlibrary.net/1.4/launch/next/5"
parsedJSON = readParseJSON(url)
insertIntoDB(parsedJSON, "launchInfo.db")