
import requests
import redis
import json
import matplotlib.pyplot as plt
from redis.commands.json.path import Path
from conn import get_redis_connection

class aggregate:
    
    def __init__(self, api_url):
        
        self.api_url = api_url
        self.redis_client = get_redis_connection()

    def fetch_data_from_api(self):
        
        params = {'limit': 30}
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data from the API. Status code: {response.status_code}")


    def insert_into_redis(self, data):
        
        self.redis_client.json().set('tv_show_data', Path.root_path(), data)


    def process_data(self, data):
        genres_count = {}
        for item in data:
            for genre in item['show']['genres']:
                genres_count[genre] = genres_count.get(genre, 0) + 1

        ratings = [item['show']['rating']['average'] for item in data if item['show']['rating']['average'] is not None]
        total_shows = len(data)
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        print(f"Total number of TV shows: {total_shows}")
        print(f"Average rating of TV shows: {average_rating:.2f}")
        print("Genre-wise show count:")
        for genre, count in genres_count.items():
            print(f"{genre}: {count}")


    def run(self):
        
        # Fetch data from the API
        json_data = self.fetch_data_from_api()

        # Insert data into Redis
        self.insert_into_redis(json_data)

        # Process data
        self.process_data(json_data)


if __name__ == "__main__":
    api_url = 'http://api.tvmaze.com/search/shows?q=golden%20girls'
    processor = aggregate(api_url)
    processor.run()
