import urllib.request, urllib.parse, urllib.error
import ssl
import json
from urllib.request import urlopen

# I'm not sure what this does, but it was in lecture materials and it works
service_url = 'https://nominatim.openstreetmap.org/search?'
osm_format = 'geojson'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    lat = input("Enter latitude:")
    lng = input("Enter longitude:")
    address = lat + "," + lng
    if len(address) < 1:
        break
    url = service_url + urllib.parse.urlencode({'q': address, 'format': osm_format})
    print("Retrieving", address)
    uh = urllib.request.urlopen(url, context = ctx)
    data = uh.read().decode()

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'features' not in js:
        print('==== Failure to retrieve ====')
        print(data)
        continue

# This exctracts 'osm_id', 'osm_type' and category from the searched location
    try:
       osm_id = js['features'][0]['properties']['osm_id']
       category = js['features'][0]['properties']['category']
       osm_type = js['features'][0]['properties']['osm_type']
       osm_type = osm_type[0].upper()
    except:
        print('Sorry, I cannot find such a place')
        osm_id = ""
        category = ""
        osm_type = ""

    if osm_id == "" or category == "" or osm_type == "":
        break

# For every searched location on 'nominatim.openstreetmap.org' under the search bar there is link to
# 'data from API request', which has a lot of information of the location. For all locations the 'API request'
# url is the same except for three parts of the url - osm_id, osm_type and category. So this part of the code
# 'assembles' the url to access the 'info' page of the searched location.
    part_one = "https://nominatim.openstreetmap.org/details.php?osmtype="
    part_two = "&osmid="
    part_three = "&class="
    part_four = "&addressdetails=1&hierarchy=0&group_hierarchy=1&format=json"
    info_address = part_one + osm_type + part_two + str(osm_id) + part_three + category + part_four

    response = urlopen(info_address)
    info = json.loads(response.read().decode())

# Extracts the needed information about the location
    type = info['type']
    postcode = info['calculated_postcode']
    country_code = info['country_code']
    house_number = info['housenumber']
    try:
        name = info['names']['name:en']
    except:
        name = info['localname']
    try:
        street_name = info['addresstags']['street']
    except:
        street_name = "None"
    try:
        city = info['addresstags']['city']
    except:
        city = ""   
    try:
        country = info['addresstags']['country']
    except:
        country = ""
        
    print("Name of the location - ", name)
    print("City - ", city)
    print("Street name - ", street_name)
    print("House number - ", house_number)
    print("Type - ", type)
    print("Postcode - ", postcode)
    print("Country - ", country)
    print("Country code - ", country_code)
    break