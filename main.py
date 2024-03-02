import requests
import redis
import json
import matplotlib.pyplot as plt
from redis.commands.json.path import Path
from conn import get_redis_connection

class TVShowDataProcessor:
    
    def __init__(self, api_url):
        self.api_url = api_url
        self.redis_client = get_redis_connection()


    #This is the function for fetching json data from given API
    def fetch_data_from_api(self):
        params = {'limit': 30}
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data from the API. Status code: {response.status_code}")


    #This is the function for inserting json data into redis using RedisJson
    def insert_into_redis(self, data):   
        self.redis_client.json().set('tv_show_data', Path.root_path(), data)


    #This is the function for processing data/perform operations as per the question
    def process_data(self, data): 
        # Displaying basic information about the TV shows
        print("Basic Information about TV Shows:")
        for item in data:
            show = item['show']
            print(f"Name: {show['name']}")
            print(f"Type: {show['type']}")
            print(f"Language: {show['language']}")
            print(f"Premiered: {show['premiered']}")
            print(f"Rating: {show['rating']['average']}")
            print()

        # Searching for a specific TV show
        search_term = 'Golden Girls'
        print(f"\nSearching for TV show: {search_term}")
        found = False
        for item in data:
            show = item['show']
            print(f"Checking show: {show['name']}")  
            if search_term.lower() in show['name'].lower():
                print(f"Found TV show: {show['name']}")
                found = True
                break
        if not found:
            print(f"TV show '{search_term}' not found.")


    def run(self):
        # Here, fetching data from the API(function call)
        json_data = self.fetch_data_from_api()

        # Here, inserting data into Redis(function call)
        self.insert_into_redis(json_data)

        # Here, Processing data(function call)
        self.process_data(json_data)


if __name__ == "__main__":
    api_url = 'http://api.tvmaze.com/search/shows?q=golden%20girls'
    processor = TVShowDataProcessor(api_url)
    processor.run()
