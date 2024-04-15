import os
import csv

base_path = '/Users/lincolnbay/Desktop/484_feat/weather_data'
out_path = '/Users/lincolnbay/Desktop/484_feat'
files = os.listdir(base_path)
counties = []

for county in files:
    if "." not in county:
        counties.append(county)
        
all_data = dict()

for county in counties:
    files = os.listdir(f'{base_path}/{county}')
    county_vars = []

    for county_var in files:
        if "." not in county:
            county_vars.append(county_var)

    all_data[county] = dict()

    for county_var in county_vars:
        var_name = county_var[:-4]

        with open(f'{base_path}/{county}/{county_var}', newline='') as work_file:
            var_data = csv.reader(work_file, delimiter=',')

            for row in var_data:
                if row[0][-2:]=="12":
                    year = row[0][:4]
                    if year not in list(all_data[county].keys()):
                        all_data[county][year] = dict()

                    all_data[county][year][var_name] = row[1]

var_list = list(all_data[list(all_data.keys())[0]][list(all_data[list(all_data.keys())[0]].keys())[0]].keys())
final_data = [['county','year']+var_list]

for county in list(all_data.keys()):
    for year in list(all_data[county].keys()):
        row = [county.replace('_',' '),year]
        for var_name in var_list:
            row.append(all_data[county][year][var_name])
        final_data.append(row)

with open(f'{out_path}/county_weather_data.csv','w') as work_file:
    for row in final_data:
        text_row = ''
        for item in row:
            text_row = text_row + str(item) + ','
        text_row = text_row[:-1]+'\n'
        work_file.write(text_row)

        
