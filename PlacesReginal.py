API_KEY =''





keyword = "Luxury goods"
city = '18.5204,73.8567',  # Pune
location = "Bhubaneswar,India"
max_results = 200  

INDIA_CITIES = [
    '20.2961,85.8245',  # Bhubaneswar
    '28.4595, 77.0266',  # Gurgaon
    '28.6315,77.2167',  #  Delhi
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

# Initialize counters for API calls
text_search_api_calls = 0
details_api_calls = 0




import requests
import pandas as pd
import time
import os
from datetime import datetime
import csv




def search_places(keyword, location):
    global text_search_api_calls

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": keyword,
        "region": location,
        "location": city,
        "key": API_KEY
    }
    results = []
    next_page_token = None

    while len(results) < max_results:
        text_search_api_calls += 1  # Increment text search API call counter

        if next_page_token:
            params["pagetoken"] = next_page_token
            time.sleep(1)  # Pause to prevent rate limiting

        response = requests.get(url, params=params)
        data = response.json()

        if "results" in data:
            results.extend(data['results'])

        if "next_page_token" in data:
            next_page_token = data['next_page_token']
            time.sleep(2)  # Pause to wait for the next page token to activate
        else:
            break

        if len(results) >= max_results:
            break
    print("total results",len(results))
    return results[:max_results]

def get_place_details(place_id):
    global details_api_calls
    details_api_calls += 1  # Increment details API call counter
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,international_phone_number,website",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json().get('result', {})

def create_google_maps_link(place_id):
    return f"https://www.google.com/maps/place/?q=place_id:{place_id}"

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
    # Get initial list of places
    places = search_places(keyword, location)
    global text_search_api_calls, details_api_calls

    
    if not places:
        print("No places found.")
        return
    
    # Fetch detailed information for each place

    detailed_places = []
    i= 0
    for place in places:
        
        place_id = place['place_id']
        details = get_place_details(place_id)
        detailed_places.append({
            "Name": details.get("name"),
            "Address": details.get("formatted_address"),
            "Phone Number": details.get("international_phone_number"),
            "Website": details.get("website"),
            "Google Maps Link": create_google_maps_link(place_id)
        })
        time.sleep(1)  # Pause between detail requests to avoid rate limiting
        i+=1
        print("entry added :",i)
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(detailed_places)
    df.to_csv("RE_pune.csv", index=False)
    print("Saved data as .csv")


    # Log the API calls to the CSV file
    log_api_calls()

    print(f"Text Search API calls made: {text_search_api_calls}")
    print(f"Details API calls made: {details_api_calls}")
    print(f"Total API calls made: {text_search_api_calls + details_api_calls}")






if __name__ == "__main__":
    main()
