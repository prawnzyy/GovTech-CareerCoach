import pandas as pd

class Excel_Reader():

    # Initialise the Excel Reader Object with corresponding excel url and data
    def __init__(self, url):
        self.url = url
        try:
            self.df = pd.read_excel(url)
        except:
            print("Unable to read from online excel")
        
    def set_url(self, url):
        self.url = url
        try:
            self.df = pd.read_excel(url)
        except:
            print("Unable to read from online excel")

    def get_url(self):
        return self.url
    
    def get_df(self):
        return self.df
        
    