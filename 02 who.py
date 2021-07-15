import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
import datetime
from datetime import datetime, timedelta
from datetime import date
import os

now = datetime.now()

Laufwerk = "D:\\"
name_output_df = 'Dataframes\\data_WHO_data.csv'

pfad_output = "Github\\Auswertung_Covid_19\\output\\"
# pfad_onedrive = "OneDrive\\Auswertung_Covid_19\\"
pfad_input = "Github\\Auswertung_Covid_19\\input\\"

Programm_Name = "WHO"

# Datum einstellen
minticks = 14
maxticks = 14

today = date.today().strftime("%d.%m.%Y")


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


a = str(date.today().strftime("%Y-%m-%d"))
# tage = days_between(a, "2020-03-01")
tage = days_between(a, "2021-06-15")

ts_x = str(datetime.today() - timedelta(tage))
ts = pd.to_datetime(ts_x, utc=True)

# Linien Stärke
lws = 3
lwb = 7
# Bezugsschriftgröße
size = 25

# output größe der bilder
h = 16 * 1.1
v = 9
dpi = 200
# pE = 100_000



#


# Webabruf - CSV einlesen
data = pd.read_csv("https://covid19.who.int/WHO-COVID-19-global-data.csv")
data = data.drop(columns=['Country_code', 'WHO_region', 'Cumulative_deaths'])
data['Date_reported'] = pd.to_datetime(data.Date_reported, utc=True)
data = data.loc[data.Date_reported >= ts, :]
data = data[data.New_cases != 0]

dictCountries = {
    "0": "Germany",
    "1": "France",
#     "2": "Austria",
#     "3": "Poland",
#     "4": "Czechia",
#     "5": "Switzerland",
#     "6": "India",
    "7": "Italy",
    "8": "Spain",
    "9": "The United Kingdom",
    "10": "Israel",
#     "11": "Sweden",
#     "12": "United States of America",
    "13": "Spain",
    "14": "Italy",
#     "15": "Russian Federation",
#     "16": "Estonia"
}
#
# # get list of all countries
# listCountries = data["Country"].unique()
# # create dict out of list
# dictCountries = {i: listCountries[i] for i in range(0, len(listCountries))}
# # print(dictCountries)


# Dataframes erzeugen

def create_df(i):
    print(i)
    print(dictCountries[i])
    name_country = str(dictCountries[i])
    df = data[data.Country == name_country]
    df['MA'] = df['New_cases'].rolling(window=7, min_periods=1).mean()
    df['MSTD_cases'] = df['New_cases'].rolling(window=7, min_periods=1).std()
    df['OTG_cases'] = df['MA'] + df['MSTD_cases']
    df['UTG_cases'] = df['MA'] - df['MSTD_cases']

    df['MA_d'] = df['New_deaths'].rolling(window=7, min_periods=1).mean()
    df['MSTD_deaths'] = df['New_deaths'].rolling(window=7, min_periods=1).std()
    df['OTG_deaths'] = df['MA_d'] + df['MSTD_deaths']
    df['UTG_deaths'] = df['MA_d'] - df['MSTD_deaths']
    # df.to_csv(f'{Laufwerk}{pfad_output} df_{dictCountries[i]}.csv')
    number_cases = str(round(df["MA"].iloc[-1], 0))
    chart_cases(df, name_country, number_cases)
    # chart_deaths(df, name_country)
    return df, name_country, number_cases


def chart_cases(df, name_country, number_cases):
    def y_axis_thousands(x, pos):
        # 'The two args are the value and tick position'
        return '{:0,d}'.format(int(x)).replace(",", ".")

    formatter = FuncFormatter(y_axis_thousands)
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(h, v * 1.2))
    ax.yaxis.set_major_formatter(formatter)

    # Neue Fälle pro Tag pro 100.000 Einwohner - 02.12.2020
    ax1 = plt.plot(df.Date_reported, df['New_cases'], marker='.', linestyle='', color="blue", markersize=20)
    ax2 = plt.plot(df.Date_reported, df['MA'], color="black", linestyle='solid', linewidth=lwb,
                   label=f'{name_country}\n(7-Tage Mittel)')
    plt.legend(loc='upper center',
               bbox_to_anchor=(0.5, -0.1),
               fancybox=True,
               shadow=True,
               ncol=3,
               fontsize=size)
    # Schriftgrößen x und y achsenwerte
    plt.xticks(fontsize=size - 10, rotation=0)
    plt.yticks(fontsize=size - 4)
    plt.ylabel('Neue Fälle', fontsize=size)
    plt.xlabel('Zeit', fontsize=size)
    plt.title(f'Neue Fälle pro Tag - {name_country} (WHO-Daten)\n', fontsize=size + 10)
    plt.suptitle(today + ' PW', fontsize=size - 5, y=0.92)
    # fill area between lines
    plt.fill_between(df.Date_reported, df['OTG_cases'], df['UTG_cases'], color='grey', alpha=0.5)
    ax.set_ylim(ymin=0)
    locator = mdates.AutoDateLocator(minticks=minticks, maxticks=maxticks)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    # Diagramm als Bild exporieren und Auflösung definieren
    plt.savefig(Laufwerk + pfad_output + number_cases + " cases " + name_country + ".png", dpi=dpi, bbox_inches='tight')


def chart_deaths(df, name_country):
    def y_axis_thousands(x, pos):
        # 'The two args are the value and tick position'
        return '{:0,d}'.format(int(x)).replace(",", ".")

    formatter = FuncFormatter(y_axis_thousands)
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(h, v * 1.2))
    ax.yaxis.set_major_formatter(formatter)
    # Neue Fälle pro Tag pro 100.000 Einwohner - 02.12.2020
    ax1 = plt.plot(df.Date_reported, df['New_deaths'], marker='.', linestyle='', color="blue", markersize=20)
    ax2 = plt.plot(df.Date_reported, df['MA_d'], color="black", linestyle='solid', linewidth=lwb,
                   label=f'{name_country}\n(7-Tage Mittel)')
    plt.legend(loc='upper center',
               bbox_to_anchor=(0.5, -0.1),
               fancybox=True,
               shadow=True,
               ncol=3,
               fontsize=size)
    # Schriftgrößen x und y achsenwerte
    plt.xticks(fontsize=size - 10, rotation=0)
    plt.yticks(fontsize=size - 4)
    plt.ylabel('Neue Todesfälle', fontsize=size)
    plt.xlabel('Zeit', fontsize=size)
    plt.title(f'Neue Todesfälle pro Tag - {name_country} (WHO-Daten)\n', fontsize=size + 10)
    plt.suptitle(today + ' PW', fontsize=size - 5, y=0.92)
    # fill area between lines
    plt.fill_between(df.Date_reported, df['OTG_deaths'], df['UTG_deaths'], color='grey', alpha=0.5)
    ax.set_ylim(ymin=0)
    locator = mdates.AutoDateLocator(minticks=minticks, maxticks=maxticks)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    # Diagramm als Bild exporieren und Auflösung definieren
    plt.savefig(Laufwerk + pfad_output + "plot deaths " + name_country + ".png", dpi=dpi, bbox_inches='tight')


for i in dictCountries:
    create_df(i)

pc = os.environ['COMPUTERNAME']
now2 = datetime.now()

# Laufzeit
x = now2 - now
x = round(x.total_seconds(), 2)
print(f'performance {pc} = {x} seconds')
