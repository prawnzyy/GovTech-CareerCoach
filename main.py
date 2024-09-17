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
    print(res_df.columns.to_list())
    
    # Write all the rows into the csv file
    to_write = res_df[[
        'restaurant.id', 'restaurant.name', 'Country', 'restaurant.location.city', 
        'restaurant.user_rating.votes', 'restaurant.user_rating.aggregate_rating', 'restaurant.zomato_events']].copy()
    to_write.to_csv("restaurant_details.csv", index=False)

if __name__ == "__main__":
    country_data = Excel_Reader("https://github.com/Papagoat/brain-assessment/blob/main/Country-Code.xlsx?raw=true")
    restaurant_data = Json_Reader("https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json")
    main(restaurant_data, country_data)