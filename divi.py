# IMPORT LIBRARIES
import pandas as pd  # Daten
from matplotlib import pyplot as plt  # plots
from matplotlib.ticker import FuncFormatter  # Numberformat plot ticks
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from datetime import date  # todays date
import os

Programm_Name = "DIVI"

Laufwerk = "D:\\"
name_input = 'data-UIdqI.csv'
name_output_df = 'Dataframes\\df_divi2.csv'

pfad_output = "Github\\Auswertung_Covid_19\\output\\"
pfad_onedrive = "OneDrive\\Auswertung_Covid_19\\"
pfad_input = "Github\\Auswertung_Covid_19\\input\\"
name_performance = 'Dataframes\\df_performance.csv'

name_1_1 = "plot_1-1_cases_absolute numbers.png"  # cases absoulte zahlen EU
name_1_2 = "plot_1-2_cases.png"  # cases pro 100.000 Einwohner EU
name_2 = "plot_2_intensiv.png"  # intensiv Deutschland
name_2_2 = "plot_2_2_intensiv_gesamt.png"  # intensiv Deutschland covid und nicht covid
name_2_3 = "plot_2_3_intensiv_covid-19.png"  # intensiv Deutschland covid
name_3_1 = "plot_3-1_deaths_absolute numbers.png"  # deaths absolute zahlen EU
name_3_2 = "plot_3-2_deaths.png"  # deaths pro 100.000 Einwohner EU
name_4_1 = "plot_4-1_cases_ger.png"  # cases Deutschland
name_4_2 = "plot_4-2_deaths_ger.png"  # deaths Deutschland
name_5 = "performance_dist_plot.png"  # Performance Plot
name_6 = "plot_6_Positivenquote_ger.png"  # Positivenquote
name_6_2 = "plot_6-2_Anzahl_Testungen_ger.png"  # Anzahl Testungen
name_7 = "plot_7_Impfquote_ger.png"  # Impfquote Deutschland Bundesländer
name_7_2 = "plot_7-2_Impfungen_Timeseries_ger.png"  # Impfungen Timeseries Deutschland
name_7_3 = "plot_7-3_Impfungen_Timeseries_ger.png"  # Impfungen Timeseries Deutschland

now = datetime.now()

# Datum einstellen
minticks = 14
maxticks = 14

# LINIEN UND SCHRIFTGRÖSSEN
# Linien Stärke
lws = 3
lwb = 7
# Bezugsschriftgröße
size = 25

# output größe der bilder
h = 16 * 1
v = 9
dpi = 200

today = date.today().strftime("%d.%m.%Y")

c_fr = '#f80d0d'  # rot
c_pl = '#25e5e5'  # cyan
c_isr = '#25e5e5'
c_ger = '#0721ff'  # dunkelblau
c_cz = '#bb8fce'  # lila
c_usa = '#bb8fce'
c_at = '#18c213'  # grün
c_rus = '#18c213'
c_se = '#18c213'
c_ch = '#000000'  # schwarz
c_ita = '#000000'
c_gb = '#faac2b'  # orange

# Lokal - CSV einlesen
df_divi2 = pd.read_csv(Laufwerk + pfad_input + name_input)
df_divi2['date'] = pd.to_datetime(df_divi2.date, utc=True)
# df_divi2 = df.loc[df.date >= ts, :]

# Timestamp definieren  YYYY-MM-DD
# ts = pd.to_datetime('2020-10-14', utc=True)

print(datetime.today())
ts_x = str(datetime.today() - timedelta(140))
ts = pd.to_datetime(ts_x, utc=True)
print(ts)

# Zeit eingrenzen

df_divi2 = df_divi2.loc[df_divi2.date >= ts, :]


# df_divi2.head(1)

# Größe im 16:9 format und mit Umrechnungsfaktor 1.2 (durch Test ermittelt) für PowerPoint angepasst
# plt.figure(figsize=(19,9))

def y_axis_thousands(x, pos):
    # 'The two args are the value and tick position'
    return '{:0,d}'.format(int(x)).replace(",", ".")


formatter = FuncFormatter(y_axis_thousands)
plt.style.use('seaborn')

fig, ax = plt.subplots(figsize=(h, v))

ax.yaxis.set_major_formatter(formatter)

plt.style.use('seaborn')
plt.grid(True)

# plt.plot(df_divi2.date,df_divi2['Belegte Betten'], color = 'blue', linewidth = lws, label = "nicht-Covid-19")
ax1 = plt.plot(df_divi2.date, df_divi2['COVID-19-Fälle'], color='red', linewidth=lws,
               label="Intensivbelegungen mit Covid-19")

plt.legend(loc='upper center',
           bbox_to_anchor=(0.5, -0.1),
           fancybox=True,
           shadow=True,
           ncol=2,
           fontsize=size)

# Schriftgrößen x und y achsenwerte
plt.xticks(fontsize=size - 10, rotation=0)
plt.yticks(fontsize=size - 4)

# plt.xticks([])
plt.ylabel('Anzahl Personen', fontsize=size)
plt.xlabel('Zeit', fontsize=size)
# plt.title('DIVI-Intensivregister (www.intensivregister.de)  \n Stand: ' + today, fontsize=size)

plt.title('Intensivstationen in Deutschland (DIVI-Daten)\n', fontsize=size + 10)
plt.suptitle(today + ' PW', fontsize=size - 5, y=0.92)

# fill area between
plt.fill_between(df_divi2.date, df_divi2['COVID-19-Fälle'], color='red', alpha=0.5)
# plt.fill_between(df_divi2.date, df_divi2['COVID-19-Fälle'], df_divi2['Belegte Betten'], color='blue',alpha=0.5)

locator = mdates.AutoDateLocator(minticks=minticks, maxticks=maxticks)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + name_2_3, dpi=dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + name_2_3, dpi=dpi, bbox_inches='tight')

# plt.show()

df_divi2.to_csv(Laufwerk + pfad_output + name_output_df, index=False)

pc = os.environ['COMPUTERNAME']
now2 = datetime.now()

# Laufzeit
x = now2 - now
x = round(x.total_seconds(), 2)

# Performance CSV einlesen


print(f'performance {pc} = {x} seconds')
