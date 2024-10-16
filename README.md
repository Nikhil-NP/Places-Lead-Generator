# Places-Lead-Generator
## Overview
The **Places Lead Generator** is a collection of python scripts  that utilizes the Google Places API to search and  filter businesses based on various criteria. This project   aims to generate leads for businesses across india and potentially overseas  based on keywords,this was a fun project that i decided to work on as i was not satisfied with **justdial** as often  it didnt provided valid contact details of potential businesses , this was created as a experiment to play around google places API and try to solve that.


## Table of Contents
- [Scripts](#scripts)
- [How to Use](#how-to-use)
- [API Key Configuration](#api-key-configuration)
- [Sample Data](#sample-data)


## Scripts
The project contains the following Python scripts:

1. **PlacesCenter.py**: This is the first script that i wrote on this topic this isnt perfect but it tried to Search for businesses  across India  from central location based on a given query.i made sure the centeral literally translates to actual central point in india both latitude and longitude.
2. **PlacesDiverse.py**: This follows a differnt approch than the above , it has a collection of top cities and it generates diverse leads across multiple cities using the specified query.
3. **PlacesDiverse2.py**:The above script was better than PlacesCenter.py but had issues with results the leads were not verfied like rating,reviews etc so to address that i created an enhanced version of `PlacesDiverse.py` with additional filtering options 
4. **PlacesMulKey.py**: The previos modules still lacked one problem that was i not able to provide multiple keywords to look for even more wider set of organizations ,so basically this searches for businesses based on multiple keywords simultaneously.
5. **PlacesReginal.py**: one more issue with PlacesDiverse2.py and PlacesDiverse.py was that there were targeting cities across India and not  Targets businesses in specific regions, here we target specific cities  like Banglore,Pune,Delhi,Mumbai etc..
6. **PlacesSingleKey.py**: Searches for businesses using a single keyword.(this was a primitve model which i initally created to test the api)

#### How to Use
1. Ensure you have the required Python packages:
   ```bash
   pip install requests

2. Clone this repository to your local machine using:
   ```bash
   git clone https://github.com/Nikhil-NP/Places-Lead-Generator.git


### API Key Configuration
To use the Google Places API, you must have an API key. Follow these steps to configure your API key:

1. Sign up for a Google Cloud account if you don't have one.
2. Create a new project in the Google Cloud Console.
3. Enable the Google Places API for your project.
4. Generate an API key and replace the placeholder in the scripts


### Sample data 
his project includes sample data for demonstration purposes.
