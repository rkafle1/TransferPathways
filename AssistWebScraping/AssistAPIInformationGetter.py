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
