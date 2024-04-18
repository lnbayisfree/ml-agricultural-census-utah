// Change this address as appropriate
cd **/initial_analysis

// Save population estimates in a merge-able format
import delimited PopEstimates2000-2022, clear
drop if county == "Utah"
replace county = strlower(county)
replace county = subinstr(county," county","",.)
drop if year < 2002
drop if year > 2022
save pop_estimates, replace

// Save wheat price data in a merge-able format, including past years
import delimited wheat_prices, clear
rename value wheatprice
keep year wheatprice
sort year
gen wheatprice_l1 = wheatprice[_n-1]
gen wheatprice_l2 = wheatprice[_n-2]
drop if year < 2002
drop if year > 2022
save wheat_prices, replace

// Save weather data in a merge-able format
import delimited county_weather_data, clear
replace county = subinstr(county," county","",.)
sort year
gen precipitation_l1 = precipitation[_n-1]
gen precipitation_l2 = precipitation[_n-2]
drop if year < 2002
drop if year > 2022
save county_weather_data, replace

// Save county GDP data in a merge-able format, separating county and year and completing partial county names
import delimited utah_countys_pop_gdp, clear
gen year = regexs(0) if(regexm(countyyear, "\d{4}"))
gen county = strlower(subinstr(county, year, "", .))
drop if county == "utah" & pop > 702434
replace county = "box elder" if county == "box"
replace county = "salt lake" if county == "salt"
replace county = "san juan" if county == "san"
drop countyyear pop
egen countycode = group(county)
destring year, replace
foreach var of varlist _all {
if "`var'" ~= "countycode" {
if "`var'" ~= "year" {
if "`var'" ~= "county" {
replace `var' = "" if `var'=="S"
replace `var' = subinstr(`var',",","",.)
destring `var', replace

// Impute GDP values for each indicator for all missing years in each county
gen loggy = log(`var')
reg loggy year i.countycode
predict pred
replace `var' = round(exp(pred)) if missing(`var')
drop pred
drop loggy
}
}
}
}
save county_gdp_data, replace

// Import and pre-process wheat production data
import delimited wheat_production, clear
replace county = strlower(county)
replace value = "" if value == " (D)"
replace value = subinstr(value,",","",.)
destring value, gen(wheatprod)
keep year county countyansi wheatprod
drop if year < 2002
drop if year > 2022
save wheat_production, replace

// Merge in population estimates, wheat prices (including lags), weather data, and GDP data
merge 1:1 county year using pop_estimates 
keep if _merge == 3
drop _merge
merge m:1 year using wheat_prices
keep if _merge == 3
drop _merge
merge 1:1 county year using county_weather_data
keep if _merge == 3
drop _merge
merge 1:1 county year using county_gdp_data
keep if _merge == 3
drop _merge

// Generate a new variable for the log of wheat product and indicator variables for each year and county
gen logwheatprod = log(wheatprod)
tabulate countyansi, generate(county)
tabulate year, generate(year)

// Save and export the full dataset
save wheat_prod_feat, replace
export delimited wheat_prod_feat, replace

// Split up and export the data set into the labeled training data and the unlabeled data for prediction
drop if missing(wheatprod)
export delimited wheat_prod_labeled, replace

use wheat_prod_feat, clear
keep if missing(wheatprod)
export delimited wheat_prod_unlabeled, replace
