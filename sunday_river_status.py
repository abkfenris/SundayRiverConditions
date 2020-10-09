#!/usr/bin/env python
import requests
import pandas as pd


DESKTOP_SUNDAY_RIVER_CONDITIONS_URL = "https://vicomap-cdn.resorts-interactive.com/api/details/1422"
MOBILE_SUNDAY_RIVER_CONDITIONS_URL = "http://spotlio-snowconditions.s3.amazonaws.com/sundayriver/status.json"

# Load the data from S3
response = requests.get(MOBILE_SUNDAY_RIVER_CONDITIONS_URL)
json = response.json()

def flatten_item(item):
    """ Returns a flattened version of the item """
    output = {}
    for key in item.keys():
        if key not in ["status", "properties"]:
            output[key] = item[key]
            
    for status in item["status"]:
        output[status['status_name']] = status['status_value']
        
    for key, obj in item["properties"].items():
        if key == "features":
            for feature_key, feature_obj in obj.items():
                output[feature_key] = feature_obj
            
        else:
            output[key] = obj
    
    return output


# Create Pandas DataFrames for both trails and lifts
trails_df = pd.DataFrame([flatten_item(item) 
                       for item in json 
                       if "type" in item 
                       and item["type"] == "trail"])
lifts_df = pd.DataFrame([flatten_item(item) 
                      for item in json 
                      if "type" in item 
                      and item["type"] == "lift"])

# Sort and write trail CSV
trails_df = trails_df.sort_values("name")
trails_df.to_csv("trails.csv", index=False)

# Sort and write lift CSV
lifts_df = lifts_df.sort_values("name")
lifts_df.to_csv("lifts.csv", index=False)
