import json
import urllib.request
import sqlite3
from parseLaunchAPI import parseLaunch
import parseLaunchAPI

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
    # launches = parsedJSON['launches']
    newParsedJSON = parsedJSON[1]
    dictKeys = list(newParsedJSON.keys())
    # Create table with id, missionname, windowstart, and windowend
    columnNamesTypes = "%s text," * (len(dictKeys))
    columnNamesTypes = columnNamesTypes.rstrip(",")
    columnNamesTypes = columnNamesTypes % tuple(dictKeys)
    columns = ", ".join(dictKeys)
    createStr = '''CREATE TABLE IF NOT EXISTS ''' + dbname + ''' (''' + columnNamesTypes + ''')'''
    print("createStr: " + createStr)
    cursorObj.execute(createStr)


    for i in range(1, len(parsedJSON) + 1):
        valueStr = ""
        first = True
        for key in dictKeys:
            print("key: " ,key) 
            print("value: ", parsedJSON[i][key])
            if first == True:
                
                myStr = str(parsedJSON[i][key])
                myStr = myStr.replace('"', '')
                myStr = myStr.replace("'", ' ')


                valueStr = "\"" + myStr + "\""
                first = False
            else:
                myStr = str(parsedJSON[i][key])
                myStr = myStr.replace('"', '')
                myStr = myStr.replace("'", ' ')

                valueStr = valueStr + ", \"" + myStr + "\""


        executableStr = "INSERT INTO " + dbname + " (" + columns + ") VALUES (" + valueStr + ")"
        # print("executableStr: " + executableStr)
 
        cursorObj.execute(executableStr)

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


# URL = "https://launchlibrary.net/1.4/launch/next/5"
# parsedJSON = readParseJSON(URL)
parsedJSON = parseLaunch()

insertIntoDB(parsedJSON, "launchInfo")
