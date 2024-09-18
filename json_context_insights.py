import json
import os
from collections import Counter

import pandas as pd

# Directory containing JSON files
json_directory = r"./json_outputs"

# Directory to save output CSV files
output_csv_directory = r"./output_csv"

# Ensure the output directory exists
os.makedirs(output_csv_directory, exist_ok=True)

# Initialize counters and dictionaries to aggregate data
keyword_counter = Counter()
context_time_counter = Counter()
context_location_counter = Counter()
context_action_counter = Counter()
instances_single_counter = Counter()
instances_few_counter = Counter()
instances_many_counter = Counter()

# Loop through all JSON files in the directory
for json_filename in os.listdir(json_directory):
    if not json_filename.endswith(".json"):
        continue

    json_path = os.path.join(json_directory, json_filename)

    # Load JSON data
    with open(json_path, "r") as json_file:
        data = json.load(json_file)

        # Aggregate keywords
        keywords = data.get("keywords", [])
        keyword_counter.update(keywords)

        # Aggregate context data
        context = data.get("context", {})
        context_time_counter.update([context.get("time", "unknown")])
        context_location_counter.update([context.get("location", "unknown")])
        context_action_counter.update([context.get("action", "unknown")])

        # Aggregate instances data
        instances = data.get("instances", {})
        instances_single_counter.update(instances.get("single", []))
        instances_few_counter.update(instances.get("few", []))
        instances_many_counter.update(instances.get("many", []))

# Convert counters to dataframes for better visualization
keyword_df = pd.DataFrame(keyword_counter.most_common(), columns=["Keyword", "Count"])
context_time_df = pd.DataFrame(
    context_time_counter.most_common(), columns=["Time", "Count"]
)
context_location_df = pd.DataFrame(
    context_location_counter.most_common(), columns=["Location", "Count"]
)
context_action_df = pd.DataFrame(
    context_action_counter.most_common(), columns=["Action", "Count"]
)
instances_single_df = pd.DataFrame(
    instances_single_counter.most_common(), columns=["Single Instance", "Count"]
)
instances_few_df = pd.DataFrame(
    instances_few_counter.most_common(), columns=["Few Instances", "Count"]
)
instances_many_df = pd.DataFrame(
    instances_many_counter.most_common(), columns=["Many Instances", "Count"]
)

# Display the dataframes
print("Keyword Frequency:")
print(keyword_df)

print("\nContext Time Frequency:")
print(context_time_df)

print("\nContext Location Frequency:")
print(context_location_df)

print("\nContext Action Frequency:")
print(context_action_df)

print("\nSingle Instances Frequency:")
print(instances_single_df)

print("\nFew Instances Frequency:")
print(instances_few_df)

print("\nMany Instances Frequency:")
print(instances_many_df)

# Save the dataframes to CSV files in the output directory
keyword_df.to_csv(
    os.path.join(output_csv_directory, "keyword_frequency.csv"), index=False
)
context_time_df.to_csv(
    os.path.join(output_csv_directory, "context_time_frequency.csv"), index=False
)
context_location_df.to_csv(
    os.path.join(output_csv_directory, "context_location_frequency.csv"), index=False
)
context_action_df.to_csv(
    os.path.join(output_csv_directory, "context_action_frequency.csv"), index=False
)
instances_single_df.to_csv(
    os.path.join(output_csv_directory, "single_instances_frequency.csv"), index=False
)
instances_few_df.to_csv(
    os.path.join(output_csv_directory, "few_instances_frequency.csv"), index=False
)
instances_many_df.to_csv(
    os.path.join(output_csv_directory, "many_instances_frequency.csv"), index=False
)
