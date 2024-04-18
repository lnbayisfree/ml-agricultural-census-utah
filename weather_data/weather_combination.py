# Import relevant packages
import os
import csv

# Store relevant paths and generate a list of the county folders
base_path = '/Users/lincolnbay/Desktop/484_feat/weather_data'
out_path = '/Users/lincolnbay/Desktop/484_feat'
files = os.listdir(base_path)
counties = []

# Shorten the list to only the county folders (i.e., leave out system files)
for county in files:
    if "." not in county:
        counties.append(county)

# Iterate through each county
all_data = dict()
for county in counties:

    # Generate a list of variable files for each county
    files = os.listdir(f'{base_path}/{county}')
    county_vars = []
    for county_var in files:
        if "." not in county:
            county_vars.append(county_var)

    # Iterate through the individual variable files in each county
    all_data[county] = dict()
    for county_var in county_vars:
        var_name = county_var[:-4]

        # Read the data in to a CSV files
        with open(f'{base_path}/{county}/{county_var}', newline='') as work_file:
            var_data = csv.reader(work_file, delimiter=',')

            # Iterate through each row in the data and store the information in one large dictionary
            for row in var_data:
                if row[0][-2:]=="12":
                    year = row[0][:4]
                    if year not in list(all_data[county].keys()):
                        all_data[county][year] = dict()
                    all_data[county][year][var_name] = row[1]

# Generate a list of the variables
var_list = list(all_data[list(all_data.keys())[0]][list(all_data[list(all_data.keys())[0]].keys())[0]].keys())

# Generate the nested list that will include all the data, beginning with the header
final_data = [['county','year']+var_list]

# By county, add the data to the nested list
for county in list(all_data.keys()):
    for year in list(all_data[county].keys()):
        row = [county.replace('_',' '),year]
        for var_name in var_list:
            row.append(all_data[county][year][var_name])
        final_data.append(row)

# Export the nested list as a CSV file
with open(f'{out_path}/county_weather_data.csv','w') as work_file:
    for row in final_data:
        text_row = ''
        for item in row:
            text_row = text_row + str(item) + ','
        text_row = text_row[:-1]+'\n'
        work_file.write(text_row)

        
