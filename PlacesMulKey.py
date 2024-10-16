API_KEY =''



import requests
import csv
import time
import random
from collections import OrderedDict


MAX_RESULTS = 10

#diverse coverage
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

# keywords
SEARCH_KEYWORDS = [
    'Boutique',
    'premium watch boutique',
    'Watch Boutique',
    ' watch boutique'
]

def search_places(keyword, location):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    places = []
    next_page_token = None

    while len(places) < MAX_RESULTS:
        params = {
            'query': keyword,
            'location': location,
            'radius': 50000,  # 50km radius
            'region': 'in',  # Restrict to India
            'type': 'store',  #  stores
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

    return places

def get_place_details(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,formatted_phone_number,website,rating,user_ratings_total,opening_hours',
        'key': API_KEY
    }

    response = requests.get(url, params=params)
    result = response.json()

    if 'result' in result:
        return result['result']
    return None

def main():
    all_places = OrderedDict()

    for city in INDIA_CITIES:
        for keyword in SEARCH_KEYWORDS:
            places = search_places(keyword, city)
            for place in places:
                if place['place_id'] not in all_places and ('rating' not in place or place['rating'] >= 4.0):
                    all_places[place['place_id']] = place
            if len(all_places) >= MAX_RESULTS:
                break
            time.sleep(random.uniform(1, 2))  
        if len(all_places) >= MAX_RESULTS:
            break

    # Sorting  by rating and then by user_ratings_total
    sorted_places = sorted(all_places.values(), key=lambda x: (x.get('rating', 0), x.get('user_ratings_total', 0)), reverse=True)

    with open('MULCrtkey.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address', 'Phone', 'Website', 'Rating', 'Review Count', 'Opening Hours', 'Google Maps Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for place in sorted_places[:MAX_RESULTS]:
            details = get_place_details(place['place_id'])
            time.sleep(random.uniform(0.5, 1))  # Random delay between 0.5-1 seconds
            if details:
                maps_link = f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
                opening_hours = ', '.join(details.get('opening_hours', {}).get('weekday_text', [])) if 'opening_hours' in details else 'Not available'
                writer.writerow({
                    'Name': details.get('name', ''),
                    'Address': details.get('formatted_address', ''),
                    'Phone': details.get('formatted_phone_number', ''),
                    'Website': details.get('website', ''),
                    'Rating': details.get('rating', 'N/A'),
                    'Review Count': details.get('user_ratings_total', 'N/A'),
                    'Opening Hours': opening_hours,
                    'Google Maps Link': maps_link
                })

if __name__ == '__main__':
    main()