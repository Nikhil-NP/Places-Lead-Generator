#diverse 

API_KEY =''

MAX_RESULTS = 500
query = 'Luxury goods'







import requests
import csv
import time
import random
import os
from datetime import datetime


# Initialize counters for API calls
text_search_api_calls = 0
details_api_calls = 0

#cities for diversity
INDIA_CITIES = [
    '28.6139,77.2090',  # New Delhi
    '19.0760,72.8777',  # Mumbai
    '22.5726,88.3639',  # Kolkata
    '13.0827,80.2707',  # Chennai
    '17.3850,78.4867',  # Hyderabad
    '12.9716,77.5946',  # Bangalore
    '23.0225,72.5714',  # Ahmedabad
    '18.5204,73.8567',  # Pune
    '26.8467,80.9462',  # Lucknow
    '21.1702,72.8311',  # Surat
]

def search_places(query, location):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    global text_search_api_calls
    places = []
    next_page_token = None

    while len(places) < MAX_RESULTS:
        text_search_api_calls += 1  # Increment text search API call counter

        params = {
            'query': query,
            'location': location,
            'region': 'in',  # onlyIndia
            'key': API_KEY
        }
        if next_page_token:
            params['pagetoken'] = next_page_token

        response = requests.get(url, params=params)
        results = response.json()

        if 'results' in results:
            places.extend(results['results'])
        
        if 'next_page_token' in results:
            next_page_token = results['next_page_token']
            time.sleep(random.uniform(2, 4))  # Rdelays optional but i feel makes it smother
        else:
            break

    return places[:MAX_RESULTS]  

def get_place_details(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    global details_api_calls
    details_api_calls += 1  # Increment details API call counter
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,formatted_phone_number,website',
        'key': API_KEY
    }

    response = requests.get(url, params=params)
    result = response.json()

    if 'result' in result:
        return result['result']
    return None

#this will track my api calls utilizations
def log_api_calls():
    total_api_calls = text_search_api_calls + details_api_calls
    log_file = 'api_call_log.csv'
    log_exists = os.path.isfile(log_file)

    with open(log_file, 'a', newline='', encoding='utf-8') as logfile:
        fieldnames = ['Timestamp', 'Text Search API Calls', 'Details API Calls', 'Total API Calls']
        writer = csv.DictWriter(logfile, fieldnames=fieldnames)
        
        if not log_exists:
            writer.writeheader()
        
        writer.writerow({
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Text Search API Calls': text_search_api_calls,
            'Details API Calls': details_api_calls,
            'Total API Calls': total_api_calls
        })

def main():
    global text_search_api_calls, details_api_calls
    
    all_places = []

    for city in INDIA_CITIES:
        places = search_places(query, city)
        all_places.extend(places)
        if len(all_places) >= MAX_RESULTS:
            break
        time.sleep(random.uniform(1, 2))  

    all_places = list({place['place_id']: place for place in all_places}.values())  #removes duplicates

    with open('Diverse500.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address', 'Phone', 'Website', 'Google Maps Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for place in all_places[:MAX_RESULTS]:
            details = get_place_details(place['place_id'])
            time.sleep(random.uniform(0.5, 1))  #some more dealys for to make it smother experience
            if details:
                maps_link = f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
                writer.writerow({
                    'Name': details.get('name', ''),
                    'Address': details.get('formatted_address', ''),
                    'Phone': details.get('formatted_phone_number', ''),
                    'Website': details.get('website', ''),
                    'Google Maps Link': maps_link
                })

    # Log the API calls to the CSV file
    log_api_calls()

    print(f"Text Search API calls made: {text_search_api_calls}")
    print(f"Details API calls made: {details_api_calls}")
    print(f"Total API calls made: {text_search_api_calls + details_api_calls}")

    try:
    # Log the API calls to the CSV file
        log_api_calls()
    except Exception as e:
        print(e)



if __name__ == '__main__':
    main()