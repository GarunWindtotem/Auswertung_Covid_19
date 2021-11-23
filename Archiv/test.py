# dictCountries = {
#     "0": "Germany",
#     "1": "France"
# }
#
# for i in dictCountries:
#     print(i)
#     print(dictCountries[i])

import pandas as pd

data = pd.read_csv("https://covid19.who.int/WHO-COVID-19-global-data.csv")
data = data.drop(columns=['Country_code', 'WHO_region', 'Cumulative_deaths'])
data['Date_reported'] = pd.to_datetime(data.Date_reported, utc=True)
data = data[data.New_cases != 0]

# get list of all countries
listCountry = data["Country"].unique()
# create dict out of list
dictCountry = {i: listCountry[i] for i in range(0, len(listCountry))}
print(dictCountry)
