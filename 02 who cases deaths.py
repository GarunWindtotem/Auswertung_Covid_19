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
tage = days_between(a, "2021-05-15")

ts_x = str(datetime.today() - timedelta(tage))
ts = pd.to_datetime(ts_x, utc=True)

# Linien Stärke
lws = 3
lwb = 7
# Bezugsschriftgröße
size = 30

# output größe der bilder
h = 16
v = 9
dpi = 150
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
    # "1": "France",
    # "2": "Austria",
    # "3": "Poland",
    # "4": "Czechia",
    # "5": "Switzerland",
    # "6": "India",
    # "7": "Italy",
    # "8": "Spain",
    "9": "The United Kingdom",
    # "10": "Israel",
    # "11": "Sweden",
    # "12": "United States of America",
    # "13": "Spain",
    # "14": "Italy",
    # "15": "Russian Federation",
    # "16": "Estonia",
    "17": "Netherlands",
    # "18:": "Greece",
    # "19": "Denmark",
}


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
    df = data.loc[data.Country == name_country]
    df['MA'] = df['New_cases'].rolling(window=7, min_periods=1).mean()
    df['MSTD_cases'] = df['New_cases'].rolling(window=7, min_periods=1).std()
    df['OTG_cases'] = df['MA'] + df['MSTD_cases']
    df['UTG_cases'] = df['MA'] - df['MSTD_cases']

    df['MA_d'] = df['New_deaths'].rolling(window=7, min_periods=1).mean()
    df['MSTD_deaths'] = df['New_deaths'].rolling(window=7, min_periods=1).std()
    df['OTG_deaths'] = df['MA_d'] + df['MSTD_deaths']
    df['UTG_deaths'] = df['MA_d'] - df['MSTD_deaths']
    df.to_csv(f'{Laufwerk}{pfad_output}//Dataframes//df_{dictCountries[i]}.csv')

    Kopplung = "no Value"

    Zeitpunkt22C = float(df["MA"].iloc[-22])
    print(f'Zeitpunkt22C {Zeitpunkt22C} {df["Date_reported"].iloc[-22]}')
    Zeitpunkt20C = float(df["MA"].iloc[-20])
    print(f'Zeitpunkt20C {Zeitpunkt20C} {df["Date_reported"].iloc[-20]}')
    Zeitpunkt18C = float(df["MA"].iloc[-18])
    print(f'Zeitpunkt18C {Zeitpunkt18C} {df["Date_reported"].iloc[-18]}')

    Zeitpunkt7D = float(df["MA_d"].iloc[-7])
    print(f'Zeitpunkt7D {Zeitpunkt7D} {df["Date_reported"].iloc[-7]}')
    Zeitpunkt1D = float(df["MA_d"].iloc[-1])
    print(f'Zeitpunkt1D {Zeitpunkt1D} {df["Date_reported"].iloc[-1]}')

    if Zeitpunkt1D > Zeitpunkt7D:
        SteigungD = True
    else:
        SteigungD = False

    if Zeitpunkt18C > Zeitpunkt20C > Zeitpunkt22C:
        SteigungC = True
    else:
        SteigungC = False

    if SteigungD is True and SteigungC is True:
        Kopplung = "D an C gekoppelt"
    else:
        Kopplung = "D NICHT an C gekoppelt"

    try:
        number_cases = str(round(df["MA"].iloc[-1], 0))
        chart_cases(df, name_country, number_cases, Kopplung)
    except IndexError:
        print("PW IndexError")
        pass
    except UnboundLocalError:
        print("PW: UnboundLocalError")
        pass

    return df, name_country, number_cases, Kopplung


def chart_cases(df, name_country, number_cases, Kopplung):
    def y_axis_thousands(x, pos):
        # 'The two args are the value and tick position'
        return '{:0,d}'.format(int(x)).replace(",", ".")

    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(h, v))
    formatter = FuncFormatter(y_axis_thousands)
    ax.yaxis.set_major_formatter(formatter)

    # locator = mdates.AutoDateLocator(minticks=minticks, maxticks=maxticks)
    # formatter = mdates.ConciseDateFormatter(locator)
    # ax.xaxis.set_major_locator(locator)
    # ax.xaxis.set_major_formatter(formatter)

    plt.plot(df.Date_reported, df['New_cases'], color="blue", alpha=0.7, marker=".", markersize=size * 0.5,
             linestyle="", label="cases")
    plt.plot(df.Date_reported, df['MA'], color="blue", marker="", linestyle="solid", label="cases (7-Tage Mittel)",
             linewidth=size * 0.2)

    ax.set_xlabel("time", fontsize=size)
    ax.set_ylabel("cases", color="blue", fontsize=size)

    ax.tick_params(labelsize=size * 0.5)

    plt.legend(loc='upper right',
               bbox_to_anchor=(0.5, -0.15),
               fancybox=True,
               shadow=True,
               ncol=1,
               fontsize=size)

    # twin object for two different y-axis on the sample plot
    ax2 = ax.twinx()
    ax2.grid(None)

    locator = mdates.AutoDateLocator(minticks=minticks, maxticks=maxticks)
    formatter = mdates.ConciseDateFormatter(locator)
    ax2.xaxis.set_major_locator(locator)
    ax2.xaxis.set_major_formatter(formatter)

    ax.set_ylim(ymin=0)

    ax2.plot(df.Date_reported, df['MA_d'], color="red", marker="", linestyle="solid", label="deaths (7-Tage Mittel)",
             linewidth=size * 0.2)
    ax2.set_ylabel("deaths", color="red", fontsize=size)

    # ax2.axis["right"].label.set_fontsize(size*0.5)
    ax2.tick_params(labelsize=size * 0.5)
    # for tick in ax2.get_major_ticks():
    #     tick.label.set_fontsize(size * 0.5)

    plt.title(f'{name_country} - {Kopplung}  (WHO-Daten) \n', fontsize=size)
    plt.legend(loc='upper left',
               bbox_to_anchor=(0.5, -0.15),
               fancybox=True,
               shadow=True,
               ncol=2,
               fontsize=size)
    plt.suptitle(f'{today} PW',
                 fontsize=size * 0.7, y=0.92)
    plt.savefig(Laufwerk + pfad_output + number_cases + " cases " + name_country + ".png", dpi=dpi, bbox_inches='tight')


for i in dictCountries:
    create_df(i)

pc = os.environ['COMPUTERNAME']
now2 = datetime.now()
# Laufzeit
x = now2 - now
x = round(x.total_seconds(), 2)
print(f'performance {pc} = {x} seconds')
