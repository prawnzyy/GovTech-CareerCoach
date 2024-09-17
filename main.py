import datetime

import pandas as pd

from excel_reader import Excel_Reader
from json_reader import Json_Reader

def main(res_data, country_data):

    # Question 1

    # Open the CSV file
    res_df = res_data.get_restaurant_df()
    country_df = country_data.get_df()

    # Iterate through the rows and remove rows where the country_id does not match
    mask = res_df["restaurant.location.country_id"].isin(country_df["Country Code"])
    res_df = res_df[mask]
    res_df = pd.merge(left=res_df, right=country_df, left_on="restaurant.location.country_id", right_on="Country Code")
    # print(res_df.columns.to_list())
    
    # Write all the rows into the csv file
    to_write = res_df[[
        "restaurant.id", "restaurant.name", "Country", "restaurant.location.city", 
        "restaurant.user_rating.votes", "restaurant.user_rating.aggregate_rating", "restaurant.zomato_events"]].copy()
    to_write.to_csv("restaurant_details.csv", index=False)

    # Question 2
    
    # First obtain all events from the restaurants that have events
    events = res_df[["restaurant.id", "restaurant.name", "restaurant.zomato_events"]].dropna()
    events = events.explode("restaurant.zomato_events")
    events = events.reset_index(drop=True)

    # Filter out the events do not have april 19 within its duration
    dateline = datetime.datetime.strptime("2019-04", "%Y-%m")
    events_mask = events["restaurant.zomato_events"].apply(lambda x: True if datetime.datetime.strptime(x["event"]["start_date"][0:7], "%Y-%m") <= dateline and dateline <= datetime.datetime.strptime(x["event"]["end_date"][0:7], "%Y-%m") else False)
    events = events[events_mask]
    events = events.reset_index(drop=True)
    
    # Prepare DF to write to CSV
    zomato = pd.json_normalize(events["restaurant.zomato_events"])
    photo_urls = zomato["event.photos"]
    photo_urls = photo_urls.apply(lambda x: x[0]['photo']['url'] if x != [] else "Na")
    zomato = zomato.assign(photo_urls=photo_urls.values)
    events = pd.concat([events.drop(columns="restaurant.zomato_events"), zomato], axis = 1)

    # Write out to CSV
    to_write = events[["event.event_id", "restaurant.id", "restaurant.name", 
                       "photo_urls", "event.title", "event.start_date", "event.end_date"]].copy()
    to_write.to_csv("restaurant_events.csv", index=False)

if __name__ == "__main__":
    country_data = Excel_Reader("https://github.com/Papagoat/brain-assessment/blob/main/Country-Code.xlsx?raw=true")
    restaurant_data = Json_Reader("https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json")
    main(restaurant_data, country_data)