import pandas as pd

class Excel_Reader():

    # Initialise the Excel Reader Object with corresponding excel url and data
    def __init__(self, url):
        self.url = url
        self.df = pd.read_excel(url)
        
    def set_url(self, url):
        self.url = url
        self.df = pd.read_excel(url)

    def get_url(self):
        return self.url
    
    def get_df(self):
        return self.df
        
    