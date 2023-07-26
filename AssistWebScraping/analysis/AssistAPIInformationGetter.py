import requests



# gets the API data
def getAPIData(APIType):
    BacicURL = "https://assist.org/api/"
    endpoint = APIType
    data = requests.get(BacicURL + endpoint).json()
    return data


# gets the id for the university or CC given the name from the Assist API. If there is an error in this returns -1
def getSchoolID(schoolName):
    # get the dictionary for the institution data
    data = getAPIData("institutions")
    # find the instituion in the dictionary and get the id
    for i in range(len(data)):
        NamesList = data[i].get("names")
        for names in NamesList:
            if schoolName == names.get('name'):
                return data[i].get('id')
             
    return -1

def getCCIdList():
    CCids = []
    # get the dictionary for the institution data
    data = getAPIData("institutions")
    # find the instituion in the dictionary and get the id
    for i in range(len(data)):
        if data[i].get("isCommunityCollege"):
            CCids.append(data[i].get("id"))
    return CCids       

def getCCNameList():
    CCIds = getCCIdList()
    CCNames = []
    for ccid in CCIds:
        CCNames.append(getSchoolFromID(ccid))
    return CCNames
def getSchoolFromID(id):
    data = getAPIData("institutions")
    # find the id and then get the institution
    for i in range(len(data)):
        if id == data[i].get("id"):
            NamesList = data[i].get("names")
            return NamesList[0].get('name')
             
    return -1

def getCCListWithAggreements(UniName):
    URL = "https://assist.org/api/institutions/" + str(getSchoolID(UniName)) + "/agreements"
    data = requests.get(URL).json()
    CClst = []
    for cc in data:
        if cc["isCommunityCollege"] and 73 in cc["sendingYearIds"] and cc["institutionName"] not in CClst:
            CClst.append(cc["institutionName"])
    return CClst


