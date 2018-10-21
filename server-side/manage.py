import json
import urllib.request
import sqlite3
from parseLaunchAPI import parseLaunch
import parseLaunchAPI
import simplejson

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
    # print("createStr: " + createStr)
    cursorObj.execute(createStr)


    for i in range(1, len(parsedJSON) + 1): #len(parsedJSON) + 1
        valueStr = ""
        first = True
        for key in dictKeys:
            # print("key: " ,key) 
            # print("value: ", parsedJSON[i][key])
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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getFromDB(dbname):
    conn = sqlite3.connect(dbname)
    conn.row_factory = dict_factory
    cursorObj = conn.cursor()

    # selectStr = '''SELECT * FROM  ''' + dbname
    selectStr = '''SELECT * FROM launchInfo DESC LIMIT 3'''
    obj = cursorObj.execute(selectStr) 
    jsonOutput = obj.fetchall()
    # print("\n\nEND\n\n")
    # print(jsonOutput)
    # print("\n\nEND\n\n")
    # print(jsonOutput[0]['net'])
    newJSON = simplejson.dumps(jsonOutput)
    print("\n\nEND\n\n")
    print(newJSON)
    # for row in obj:
    #     print(row)
    return obj
# URL = "https://launchlibrary.net/1.4/launch/next/5"
# parsedJSON = readParseJSON(URL)
parsedJSON = parseLaunch()

# insertIntoDB(parsedJSON, "launchInfo")
jsonOutput = getFromDB("launchInfo")
print("\n\n\n\n\n========\n\n")
print(jsonOutput)
