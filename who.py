import pandas as pd  # Daten
from matplotlib import pyplot as plt  # plots
from matplotlib.ticker import FuncFormatter  # Numberformat plot ticks
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from datetime import date  # todays date

# import seaborn as sns

import os

now = datetime.now()

Programm_Name = "WHO"  # 04.01.2021 - Time Series Impffdaten erstellen

Laufwerk = "D:\\"
name_output_df = 'Dataframes\\data_WHO_data.csv'

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
name_5_1 = "plot_5-1_cases_est_ger"
name_5_2 = "plot_5-2_deaths_est_ger"

# Datum einstellen
minticks = 14
maxticks = 14

today = date.today().strftime("%d.%m.%Y")

# Timestamp definieren  YYYY-MM-DD
# ts = pd.to_datetime('2020-10-18', utc=True)

print(datetime.today())

ts_x = str(datetime.today() - timedelta(140))
ts = pd.to_datetime(ts_x, utc=True)
print(ts)

# Webabruf - CSV einlesen
data = pd.read_csv("https://covid19.who.int/WHO-COVID-19-global-data.csv")

# gleitender Mittelwert der cases und deaths, 7 Tage
data['MA'] = data['New_cases'].rolling(window=7, min_periods=1).mean()
data['MA_deaths'] = data['New_deaths'].rolling(window=7, min_periods=1).mean()

data['MSTD_cases'] = data['New_cases'].rolling(window=7, min_periods=1).std()
data['MSTD_deaths'] = data['New_deaths'].rolling(window=7, min_periods=1).std()

data['OTG_cases'] = data['MA'] + data['MSTD_cases']
data['UTG_cases'] = data['MA'] - data['MSTD_cases']

data['OTG_deaths'] = data['MA_deaths'] + data['MSTD_deaths']
data['UTG_deaths'] = data['MA_deaths'] - data['MSTD_deaths']

# Date_reported in eine Datumsspalte umwandeln
data['Date_reported'] = pd.to_datetime(data.Date_reported, utc=True)

# Zeit eingrenzen
data = data.loc[data.Date_reported >= ts, :]

data = data.drop(columns=['Country_code', 'WHO_region', 'Cumulative_deaths'])

data.head(1)

# Linien Stärke
lws = 3
lwb = 7
# Bezugsschriftgröße
size = 25

# output größe der bilder
h = 16 * 1.1
v = 9
dpi = 200
pE = 100_000

ger = data[data.Country == 'Germany']
ger = ger[ger.New_cases != 0]
fr = data[data.Country == 'France']
fr = fr[fr.New_cases != 0]
at = data[data.Country == 'Austria']
at = at[at.New_cases != 0]
pl = data[data.Country == 'Poland']
pl = pl[pl.New_cases != 0]
cz = data[data.Country == 'Czechia']
cz = cz[cz.New_cases != 0]
ch = data[data.Country == 'Switzerland']
ch = ch[ch.New_cases != 0]
it = data[data.Country == 'Italy']
it = it[it.New_cases != 0]
es = data[data.Country == 'Spain']
es = es[es.New_cases != 0]
gb = data[data.Country == 'The United Kingdom']
gb = gb[gb.New_cases != 0]

isr = data[data.Country == 'Israel']
isr = isr[isr.New_cases != 0]
se = data[data.Country == 'Sweden']
se = se[se.New_cases != 0]
usa = data[data.Country == 'United States of America']
usa = usa[usa.New_cases != 0]
spa = data[data.Country == 'Spain']
spa = spa[spa.New_cases != 0]
ita = data[data.Country == 'Italy']
ita = ita[ita.New_cases != 0]
rus = data[data.Country == 'Russian Federation']
rus = rus[rus.New_cases != 0]

est = data[data.Country == 'Estonia']
est = est[est.New_cases != 0]

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

E_fr = 66_012_908
E_pl = 38_659_927
E_ger = 83_020_000
E_cz = 10_586_651
E_at = 8_902_600
E_ch = 8_847_020
E_gb = 66_650_000

E_isr = 8_884_000
E_usa = 328_200_000
E_rus = 144_500_000
E_ita = 60_360_000
E_spa = 46_940_000
E_se = 10_230_000

E_est = 1_329_000

# Größe im 16:9 format und mit Umrechnungsfaktor 1.2 (durch Test ermittelt) für PowerPoint angepasst
# plt.figure(figsize=(h,v))

plt.style.use('seaborn')

# Neue Fälle pro Tag pro 100.000 Einwohner - 02.12.2020

fig, ax = plt.subplots(figsize=(h, v))

ax3 = plt.plot(fr.Date_reported, fr['MA'] * (pE / E_fr), color=c_fr, linestyle='dashed', linewidth=lws,
               label="1.) Frankreich")
ax2 = plt.plot(se.Date_reported, se['MA'] * (pE / E_se), color=c_se, linestyle='dashed', linewidth=lws,
               label="2.) Schweden")
ax6 = plt.plot(at.Date_reported, at['MA'] * (pE / E_at), color=c_at, linestyle='solid', linewidth=lws,
               label="3.) Österreich")
ax8 = plt.plot(ger.Date_reported, ger['MA'] * (pE / E_ger), color=c_ger, linestyle='solid', linewidth=lwb,
               label="4.) Deutschland")
ax7 = plt.plot(ch.Date_reported, ch['MA'] * (pE / E_ch), color=c_ch, linestyle='solid', linewidth=lws,
               label="5.) Schweiz")
ax4 = plt.plot(usa.Date_reported, usa['MA'] * (pE / E_usa), color=c_usa, linestyle='dashed', linewidth=lws,
               label="6.) USA")
ax1 = plt.plot(isr.Date_reported, isr['MA'] * (pE / E_isr), color=c_isr, linestyle='dashed', linewidth=lws,
               label="7.) Israel")
ax5 = plt.plot(gb.Date_reported, gb['MA'] * (pE / E_gb), color=c_gb, linestyle='dashed', linewidth=lws,
               label="8.) Großbritannien")

plt.legend(loc='upper center',
           bbox_to_anchor=(0.5, -0.2),
           fancybox=True,
           shadow=True,
           ncol=3,
           fontsize=size)

# Schriftgrößen x und y achsenwerte
plt.xticks(fontsize=size - 10, rotation=0)
plt.yticks(fontsize=size - 4)

plt.ylabel('Neue Fälle', fontsize=size)
plt.xlabel('Zeit', fontsize=size)

plt.title('Neue Fälle pro Tag - pro 100.000 Einwohner (WHO-Daten)\n', fontsize=size + 10)
plt.suptitle(today + ' PW', fontsize=size - 5, y=0.92)

locator = mdates.AutoDateLocator(minticks=minticks, maxticks=maxticks)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

# date_form = DateFormatter("%Y-%m")
# ax.xaxis.set_major_formatter(date_form)

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + name_1_2, dpi=dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + name_1_2, dpi=dpi, bbox_inches='tight')

# Größe im 16:9 format und mit Umrechnungsfaktor 1.2 (durch Test ermittelt) für PowerPoint angepasst
# plt.figure(figsize=(h,v))


# Todesfälle pro 100.000 Einwohner 02.12.2020


fig, ax = plt.subplots(figsize=(h, v))
plt.style.use('seaborn')
plt.grid(True)

ax3 = plt.plot(fr.Date_reported, fr['MA_deaths'] * (pE / E_fr), color=c_fr,
               linestyle='dashed', linewidth=lws, label="1.) Frankreich")

ax2 = plt.plot(usa.Date_reported, usa['MA_deaths'] * (pE / E_usa), color=c_usa,
               linestyle='dashed', linewidth=lws, label="2.) USA")

ax6 = plt.plot(at.Date_reported, at['MA_deaths'] * (pE / E_at), color=c_at,
               linestyle='solid', linewidth=lws, label="3.) Österreich")

ax4 = plt.plot(ger.Date_reported, ger['MA_deaths'] * (pE / E_ger), color=c_ger,
               linestyle='solid', linewidth=lwb, label="4.) Deutschland")

ax5 = plt.plot(isr.Date_reported, isr['MA_deaths'] * (pE / E_isr), color=c_isr,
               linestyle='dashed', linewidth=lws, label="5.) Israel")

ax1 = plt.plot(gb.Date_reported, gb['MA_deaths'] * (pE / E_gb), color=c_gb,
               linestyle='dashed', linewidth=lws, label="6.) Großbritannien")

ax7 = plt.plot(ch.Date_reported, ch['MA_deaths'] * (pE / E_ch), color=c_ch,
               linestyle='solid', linewidth=lws, label="7.) Schweiz")

ax8 = plt.plot(se.Date_reported, se['MA_deaths'] * (pE / E_se), color=c_se,
               linestyle='dashed', linewidth=lws, label="8.) Schweden")

# Legende
plt.legend(loc='upper center',
           bbox_to_anchor=(0.5, -0.2),
           fancybox=True,
           shadow=True,
           ncol=3,
           fontsize=size)

# Schriftgrößen x und y achsenwerte
plt.xticks(fontsize=size - 10, rotation=0)
plt.yticks(fontsize=size - 4)
plt.ylabel('Todesfälle', fontsize=size)
plt.xlabel('Zeit', fontsize=size)

plt.title('Todesfälle pro Tag - pro 100.000 Einwohner (WHO-Daten)\n', fontsize=size + 10)
plt.suptitle(today + ' PW', fontsize=size - 5, y=0.92)

locator = mdates.AutoDateLocator(minticks=minticks, maxticks=maxticks)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + name_3_2, dpi=dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + name_3_2, dpi=dpi, bbox_inches='tight')

ts = pd.to_datetime('2021-01-15', utc=True)  # YYYY-MM-DD

# dataframe reduzieren
ger_change = data[data.Country == 'Germany']
ger_change = ger_change.loc[ger_change.Date_reported >= ts, :]

ger_change = ger_change.drop(columns=['Cumulative_cases',
                                      'New_deaths', 'MA_deaths',
                                      'MSTD_cases', 'MSTD_deaths',
                                      'OTG_cases', 'UTG_cases',
                                      'OTG_deaths', 'UTG_deaths'])

ger_change["change_1"] = 100 * ger_change["MA"].pct_change(periods=1)
ger_change["change_1_MW"] = ger_change["change_1"].rolling(window=3, min_periods=1, center=True).mean()

ger_change["MSTD"] = ger_change["change_1"].rolling(window=7, min_periods=1).std()

# ger_change["change_1_MW_std+"] = ger_change["change_1_MW"] +
# ger_change["change_1_MW_std-"] =


# ger_change["change_4"] = 100 * ger_change["MA"].pct_change(periods=4)
# ger_change["change_7"] = 100 * ger_change["MA"].pct_change(periods=7)
# ger_change["change_14"] = 100 * ger_change["MA"].pct_change(periods=14)

ger_change["R1"] = 0

ger_change.head(10)


# Größe im 16:9 format und mit Umrechnungsfaktor 1.2 (durch Test ermittelt) für PowerPoint angepasst
# plt.figure(figsize=(h*1.4,v))

def y_axis_thousands(x, pos):
    # 'The two args are the value and tick position'
    return '{:0,d}'.format(int(x)).replace(",", ".")


formatter = FuncFormatter(y_axis_thousands)

fig, ax = plt.subplots(figsize=(h, v))

ax.yaxis.set_major_formatter(formatter)

# Neue Fälle pro Tag pro 100.000 Einwohner - 02.12.2020
ax1 = plt.plot(ger.Date_reported, ger['MA'], color=c_ger, linestyle='solid', linewidth=lwb,
               label="Deutschland\n(7-Tage Mittel)")
ax2 = plt.plot(ger.Date_reported, ger['New_cases'], marker='.', linestyle='', color=c_ger, markersize=20)
ax3 = plt.plot(ger.Date_reported, ger['OTG_cases'], color='red', linestyle='dashed', linewidth=lws, label="±1 sigma")
ax4 = plt.plot(ger.Date_reported, ger['UTG_cases'], color='red', linestyle='dashed', linewidth=lws, label="")

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

plt.title('Neue Fälle pro Tag - Deutschland (WHO-Daten)\n', fontsize=size + 10)
plt.suptitle(today + ' PW', fontsize=size - 5, y=0.92)

# fill area between lines
plt.fill_between(ger.Date_reported, ger['OTG_cases'], ger['UTG_cases'], color='red', alpha=0.5)

ax.set_ylim(ymin=0)

locator = mdates.AutoDateLocator(minticks=minticks, maxticks=maxticks)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + name_4_1, dpi=dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + name_4_1, dpi=dpi, bbox_inches='tight')


# Größe im 16:9 format und mit Umrechnungsfaktor 1.2 (durch Test ermittelt) für PowerPoint angepasst
# plt.figure(figsize=(16,9))


def y_axis_thousands(x, pos):
    # 'The two args are the value and tick position'
    return '{:0,d}'.format(int(x)).replace(",", ".")


formatter = FuncFormatter(y_axis_thousands)

ffig, ax = plt.subplots(figsize=(h, v))

ax.yaxis.set_major_formatter(formatter)
plt.style.use('seaborn')
plt.grid(True)
# Todesfälle pro 100.000 Einwohner 02.12.2020

ax1 = plt.plot(ger.Date_reported, ger['MA_deaths'], color=c_ger, linestyle='solid', linewidth=lwb,
               label="Deutschland\n(7-Tage Mittel)")  # blau, linie, dick
ax2 = plt.plot(ger.Date_reported, ger['New_deaths'], marker='.', linestyle='', color=c_ger, markersize=20)

ax3 = plt.plot(ger.Date_reported, ger['OTG_deaths'], color='red', linestyle='dashed', linewidth=lws, label="±1 sigma")
ax4 = plt.plot(ger.Date_reported, ger['UTG_deaths'], color='red', linestyle='dashed', linewidth=lws, label="")

ax.set_ylim(ymin=0)

# Legende
plt.legend(loc='upper center',
           bbox_to_anchor=(0.5, -0.1),
           fancybox=True,
           shadow=True,
           ncol=3,
           fontsize=size)

# Schriftgrößen x und y achsenwerte
plt.xticks(fontsize=size - 10, rotation=0)
plt.yticks(fontsize=size - 4)
plt.ylabel('Todesfälle', fontsize=size)
plt.xlabel('Zeit', fontsize=size)

plt.title('Todesfälle pro Tag - Deutschland (WHO-Daten)\n', fontsize=size + 10)
plt.suptitle(today + ' PW', fontsize=size - 5, y=0.92)

# fill area between lines
plt.fill_between(ger.Date_reported, ger['OTG_deaths'], ger['UTG_deaths'], color='red', alpha=0.5)

locator = mdates.AutoDateLocator(minticks=minticks, maxticks=maxticks)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + name_4_2, dpi=dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + name_4_2, dpi=dpi, bbox_inches='tight')

# ger = ger.drop(columns=['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ])


data.to_csv(Laufwerk + pfad_output + name_output_df, index=False)

ger.to_csv(Laufwerk + pfad_output + "\\Dataframes\\ger.csv", index=False)
fr.to_csv(Laufwerk + pfad_output + "\\Dataframes\\fr.csv", index=False)
at.to_csv(Laufwerk + pfad_output + "\\Dataframes\\at.csv", index=False)
pl.to_csv(Laufwerk + pfad_output + "\\Dataframes\\pl.csv", index=False)
cz.to_csv(Laufwerk + pfad_output + "\\Dataframes\\cz.csv", index=False)
ch.to_csv(Laufwerk + pfad_output + "\\Dataframes\\ch.csv", index=False)
it.to_csv(Laufwerk + pfad_output + "\\Dataframes\\it.csv", index=False)
es.to_csv(Laufwerk + pfad_output + "\\Dataframes\\es.csv", index=False)
gb.to_csv(Laufwerk + pfad_output + "\\Dataframes\\gb.csv", index=False)
isr.to_csv(Laufwerk + pfad_output + "\\Dataframes\\isr.csv", index=False)
se.to_csv(Laufwerk + pfad_output + "\\Dataframes\\se.csv", index=False)
usa.to_csv(Laufwerk + pfad_output + "\\Dataframes\\usa.csv", index=False)
spa.to_csv(Laufwerk + pfad_output + "\\Dataframes\\spa.csv", index=False)
ita.to_csv(Laufwerk + pfad_output + "\\Dataframes\\ita.csv", index=False)
rus.to_csv(Laufwerk + pfad_output + "\\Dataframes\\rus.csv", index=False)

pc = os.environ['COMPUTERNAME']
now2 = datetime.now()

# Laufzeit
x = now2 - now
x = round(x.total_seconds(), 2)

# Performance CSV einlesen
d = pd.read_csv(Laufwerk + pfad_output + name_performance)

# Neues Dateframe für die Performance definieren
now = datetime.now()

d2 = {'Date': [now],
      'PC': [pc],
      'Laufzeit_in_s': [x],
      'Version': [Programm_Name]}

# Datum Spalte formatieren
df2 = pd.DataFrame(d2)
df2['Date'] = df2['Date'].dt.strftime('%Y-%m-%d %r')

# Performance mit dem CSV verbinden
d = d.append(df2, ignore_index=True)

# Datenexport Performance
d.to_csv(Laufwerk + pfad_output + name_performance, index=False)

print(f'performance {pc} = {x} seconds')
