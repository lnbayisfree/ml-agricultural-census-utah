# Import relevant packages
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import os

# Store the relevant url and storage path
url = "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/county/time-series/UT-007/tavg/12/0/1990-2024?base_prd=true&begbaseyear=1901&endbaseyear=2000"
save_path = '/Users/lincolnbay/Desktop/484_feat/weather_data'

# Download and store all of the weather data from all relevant years for all Utah counties
with sync_playwright() as my_playwright:

    # Open the browser and open the page
    browser = my_playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url, timeout=60000)

    # Store the addresses of all the important elements on the page
    param_select = page.locator("#parameter")
    ts_select = page.locator("#timescale")
    loc_select = page.locator("#location")
    sub_butt = page.locator("#submit")
    csv_butt = page.locator("#csv-download")
    locations = loc_select.locator("option").all()

    # In the case that the website shows all counties of all states (which it does sometimes), 
    #     assemble the locators of the Utah county menu options
    rel_locs = []
    utah_found = False
    for location in locations:
        if "Beaver" in location.inner_text():
            utah_found = True
        if utah_found == True:
            rel_locs.append(location)
        if "Weber" in location.inner_text():
            break

    # Iterate through all the relevant counties
    for loc in rel_locs:

        # Get the county name and report progress
        county_orig = loc.inner_text()
        print(county_orig)

        # Open the county's page and adapt the county's name for storage
        loc_select.select_option(county_orig)
        time.sleep(1)
        county_name = county_orig.casefold().replace(" ","_")

        # Iterate through each recorded aspect of the weather
        for parameter in param_select.locator("option").all():

            # Take the name of the weather aspect and transform it as appropriate
            param_t = parameter.inner_text()
            param_name = param_t.replace(" ","_").casefold()
            param_select.select_option(param_t)

            # Ask the website to report the average over the last 12 months
            if "Palmer" not in param_t:
                ts_select.select_option("12-Month")
            time.sleep(2)
            sub_butt.click()
            time.sleep(2)

            # Download the file
            expect(csv_butt).to_be_visible(timeout=240000)
            with page.expect_download() as download_info:
                csv_butt.hover()
                csv_butt.click()

            # Save the file
            download = download_info.value
            if not os.path.exists(f'{save_path}/{county_name}'):
                os.makedirs(f'{save_path}/{county_name}')
            os.chdir(f'{save_path}/{county_name}')
            download.save_as(f'{param_name}.csv')
            time.sleep(2)
            
            
                
            
        

