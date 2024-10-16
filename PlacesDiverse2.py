API_KEY =''



import requests
import csv
import time
import random
import os
from datetime import datetime

MAX_RESULTS = 300
query = 'Luxury goods'

# Initialize counters for API calls
text_search_api_calls = 0
details_api_calls = 0

# Cities for diversity
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
        text_search_api_calls += 1

        params = {
            'query': query,
            'location': location,
            'region': 'in',
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
            time.sleep(random.uniform(2, 4))
        else:
            break
    print("total entieries we are returning",len(places))
    return places

def get_place_details(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    global details_api_calls
    details_api_calls += 1
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,formatted_phone_number,website,user_ratings_total,rating',
        'key': API_KEY
    }

    response = requests.get(url, params=params)
    result = response.json()

    if 'result' in result:
        return result['result']
    return None

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

def filter_places(places, min_reviews=2, max_reviews=500, min_rating=3.5):
    return [
        place for place in places
        if min_reviews <= place.get('user_ratings_total', 0) <= max_reviews
        and place.get('rating', 0) >= min_rating
    ]

def main():
    global text_search_api_calls, details_api_calls
    
    all_places = []

    for city in INDIA_CITIES:
        places = search_places(query, city)
        filtered_places = filter_places(places)
        all_places.extend(filtered_places)
        if len(all_places) >= MAX_RESULTS:
            break
        time.sleep(random.uniform(1, 2))

    all_places = list({place['place_id']: place for place in all_places}.values())  # removes duplicates

    with open('Diverse300LG.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address', 'Phone', 'Website', 'Google Maps Link', 'Rating', 'Number of Reviews']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        i=0
        for place in all_places[:MAX_RESULTS]:
            details = get_place_details(place['place_id'])
            time.sleep(random.uniform(0.5, 1))
            if details:
                maps_link = f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
                writer.writerow({
                    'Name': details.get('name', ''),
                    'Address': details.get('formatted_address', ''),
                    'Phone': details.get('formatted_phone_number', ''),
                    'Website': details.get('website', ''),
                    'Google Maps Link': maps_link,
                    'Rating': details.get('rating', ''),
                    'Number of Reviews': details.get('user_ratings_total', '')
                })
                i+=1
                print("detail added:",i)

    log_api_calls()

    print(f"Text Search API calls made: {text_search_api_calls}")
    print(f"Details API calls made: {details_api_calls}")
    print(f"Total API calls made: {text_search_api_calls + details_api_calls}")

if __name__ == '__main__':
    main()