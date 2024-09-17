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
    photo_urls = photo_urls.apply(lambda x: x[0]['photo']['url'] if x != [] else "NA")
    zomato = zomato.assign(photo_urls=photo_urls.values)
    events = pd.concat([events.drop(columns="restaurant.zomato_events"), zomato], axis = 1)

    # Write out to CSV
    to_write = events[["event.event_id", "restaurant.id", "restaurant.name", 
                       "photo_urls", "event.title", "event.start_date", "event.end_date"]].copy()
    to_write.to_csv("restaurant_events.csv", index=False)

    # Question 3

    """
    Assumptions made:
    1. The data where the country Ids do not much are not being used
    2. Restaurants which have fake reviews should not be counted into the threshold value to prevent
    skewing of data
    3. The Threshold of the ratings is determined by the lowest value of that particular rating
    """
    # Obtain columns that have user rating information
    user_ratings = res_df.filter(regex="user_rating")

    # Remove those restaurants with fake reviews
    mask = user_ratings["restaurant.user_rating.has_fake_reviews"].apply(lambda x: True if x == 0 else False)
    user_ratings = user_ratings[mask]

    # Store the minimum value of each rating in a dictionary
    rating_threshold = {}
    for index, row in user_ratings.iterrows():
        rating = row["restaurant.user_rating.aggregate_rating"]
        text = row["restaurant.user_rating.rating_text"]
        if text not in rating_threshold:
            rating_threshold[text] = rating
        else:
            rating_threshold[text] = min(rating, rating_threshold[text])
    
    # Display required ratings in a table.
    required_rating = ["Excellent", "Very Good", "Good", "Average", "Poor"]
    print(f"{"Threshold": <12} {"Value"}")
    for rating in required_rating:
        print(f"{rating + ":": <12} {rating_threshold[rating]}")
    
if __name__ == "__main__":
    country_data = Excel_Reader("https://github.com/Papagoat/brain-assessment/blob/main/Country-Code.xlsx?raw=true")
    restaurant_data = Json_Reader("https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json")
    main(restaurant_data, country_data)