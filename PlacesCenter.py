#center of  india


API_KEY =''
query = 'boutique watch'

import requests
import csv
import time
maxsearch = 10

def search_places(query, location):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    places = []
    next_page_token = None

    while len(places) < maxsearch:
        params = {
            'query': query,
            'location': location,
            'region': 'in',  #  India only
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
            time.sleep(2)  
        else:
            break

    return places[:maxsearch]  

def get_place_details(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
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

def main():
    
    location = '20.5937,78.9629'  # ~ center of India co-ordinates

    places = search_places(query, location)

    with open('center.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address', 'Phone', 'Website','Google Maps Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for place in places:
            details = get_place_details(place['place_id'])
            if details:
                maps_link = f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
                writer.writerow({
                    'Name': details.get('name', ''),
                    'Address': details.get('formatted_address', ''),
                    'Phone': details.get('formatted_phone_number', ''),
                    'Website': details.get('website', ''),
                    'Google Maps Link': maps_link
                })

if __name__ == '__main__':
    main()