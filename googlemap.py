import requests
import os


def searchPlaceID(textQuery):
    apiEndpoint = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={INPUT}&inputtype=textquery&key={API_KEY}"
    r = requests.get(apiEndpoint.format(INPUT=textQuery,API_KEY=getAPIKey()))
    r.raise_for_status()
    return r.json()['candidates'][0]['place_id']

def getPlaceCoords(placeID):
    apiEndpoint = "https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&key={API_KEY}"
    r = requests.get(apiEndpoint.format(PLACE_ID=placeID,API_KEY=getAPIKey()))
    r.raise_for_status()
    return r.json()['result']['geometry']['location']

def getAPIKey():
    return os.getenv("GCP_MAPS_API_KEY")