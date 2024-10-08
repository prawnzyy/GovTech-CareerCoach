import pandas as pd
import json
import urllib.request

class Json_Reader():
    def __init__(self, url):
        self.url = url
        try:
            self.urllib_url = urllib.request.urlopen(url)

            self.data = json.load(self.urllib_url)
            self.restaurant_df = pd.json_normalize(self.data, record_path=['restaurants'])

            # Read the unflattened one
            self.df = pd.read_json(url)
        
        except ValueError:
            print("This is not a valid URL. Please use a valid one!")

    def set_url(self, url):
        self.url = url
        try:
            self.urllib_url = urllib.request.urlopen(url)

            self.data = json.load(self.urllib_url)
            self.restaurant_df = pd.json_normalize(self.data, record_path=['restaurants'])

            # Read the unflattened one
            self.df = pd.read_json(url)
        
        except ValueError:
            print("This is not a valid URL. Please use a valid one!")

    def get_url(self):
        return self.url
    
    def get_df(self):
        return self.df
    
    def get_restaurant_df(self):
        return self.restaurant_df