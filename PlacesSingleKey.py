import requests
import csv
import time
import random

API_KEY = "YOUR_API_KEY"
query = "boutique watch"
MAX_RESULTS = 10

# Cities across India to search
INDIA_CITIES = [
    '28.6139,77.2090',  # New Delhi
    '19.0760,72.8777',  # Mumbai
    '22.5726,88.3639',  # Kolkata
]

def search_places(query, location):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    places = []
    next_page_token = None
    
    # Limited api calls 
    while len(places) < 20:
        params = {
            'query': query,
            'location': location,
            'radius': 50000,  # 50 km radius
            'key': API_KEY
        }
        if next_page_token:
            params['pagetoken'] = next_page_token

        response = requests.get(url, params=params)
        results = response.json()

        if 'results' in results:
            places.extend(results['results'])
        
        if 'next_page_token' in results and len(places) < 20:
            next_page_token = results['next_page_token']
            time.sleep(2)  # Mandatory delay before using next_page_token
        else:
            break

    return places

def get_place_details(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,formatted_phone_number,website,rating,user_ratings_total',
        'key': API_KEY
    }

    response = requests.get(url, params=params)
    result = response.json()

    return result.get('result', None)

def rank_places(places, query):
    ranked_places = []
    query_words = query.lower().split()

    for place in places:
        details = get_place_details(place['place_id'])
        time.sleep(random.uniform(1, 2))  # Increased delay between requests

        if details:
            # Basic scoring based on ratings and relevance
            score = (details.get('rating', 0) * details.get('user_ratings_total', 0)) + \
                    sum(details.get('name', '').lower().count(word) for word in query_words)

            # Boost score if website is available
            if details.get('website'):
                score += 10

            ranked_places.append((score, details))

            # Stop if we already have enough details
            if len(ranked_places) >= MAX_RESULTS:
                break

    return sorted(ranked_places, key=lambda x: x[0], reverse=True)

def main():
    all_places = []

    for city in INDIA_CITIES:
        places = search_places(query, city)
        all_places.extend(places)
        if len(all_places) >= MAX_RESULTS:
            break
        time.sleep(random.uniform(2, 4))  # Pause between city searches

    # Remove duplicates based on place_id
    all_places = list({place['place_id']: place for place in all_places}.values())
    ranked_places = rank_places(all_places, query)

    with open(f'{query.replace(" ", "_")}_leads_india.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address', 'Phone', 'Website', 'Google Maps Link', 'Rating', 'Number of Ratings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for _, place in ranked_places[:MAX_RESULTS]:
            maps_link = f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
            writer.writerow({
                'Name': place.get('name', ''),
                'Address': place.get('formatted_address', ''),
                'Phone': place.get('formatted_phone_number', ''),
                'Website': place.get('website', ''),
                'Google Maps Link': maps_link,
                'Rating': place.get('rating', ''),
                'Number of Ratings': place.get('user_ratings_total', '')
            })

    print(f"Successfully generated {min(MAX_RESULTS, len(ranked_places))} leads for '{query}' in India.")

if __name__ == '__main__':
    main()
