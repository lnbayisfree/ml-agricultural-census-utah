cd /Users/lincolnbay/Desktop/484_feat/to_include

import delimited PopEstimates2000-2022, clear
drop if county == "Utah"
replace county = strlower(county)
replace county = subinstr(county," county","",.)
drop if year < 2002
drop if year > 2022
save pop_estimates, replace

import delimited wheat_prices, clear
rename value wheatprice
keep year wheatprice
sort year
gen wheatprice_l1 = wheatprice[_n-1]
gen wheatprice_l2 = wheatprice[_n-2]
drop if year < 2002
drop if year > 2022
save wheat_prices, replace

import delimited county_weather_data, clear
replace county = subinstr(county," county","",.)
sort year
gen precipitation_l1 = precipitation[_n-1]
gen precipitation_l2 = precipitation[_n-2]
drop if year < 2002
drop if year > 2022
save county_weather_data, replace

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

import delimited wheat_production, clear
replace county = strlower(county)
replace value = "" if value == " (D)"
replace value = subinstr(value,",","",.)
destring value, gen(wheatprod)
keep year county countyansi wheatprod
drop if year < 2002
drop if year > 2022
save wheat_production, replace

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

gen logwheatprod = log(wheatprod)
tabulate countyansi, generate(county)
tabulate year, generate(year)

save wheat_prod_feat, replace
export delimited wheat_prod_feat, replace

drop if missing(wheatprod)
export delimited wheat_prod_labeled, replace

use wheat_prod_feat, clear
keep if missing(wheatprod)
export delimited wheat_prod_unlabeled, replace
