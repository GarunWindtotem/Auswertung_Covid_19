import pandas as pd #Daten
from matplotlib import pyplot as plt # plots
#import matplotlib as mpl
from matplotlib.ticker import FuncFormatter   # Numberformat plot ticks
# import matplotlib.ticker as ticker
import matplotlib.dates as mdates
# from matplotlib.dates import DateFormatter
import numpy as np

# performance
import datetime
from datetime import datetime, timedelta
from datetime import date # todays date

#import seaborn as sns

import os
now = datetime.now()

# Linien Stärke
lws = 3
lwb = 7
# Bezugsschriftgröße
size = 25


# output größe der bilder
h = 16*1.2
v = 9
dpi = 200

# heutiges datum
today = date.today().strftime("%d.%m.%Y")

# Datum einstellen 
minticks = 14
maxticks = 14

Laufwerk = "D:\\"
name_output_df = 'Dataframes\\data_WHO_data.csv'

name_input_VOC = "Virusvarianten.csv"
name_input_VOC_GGS = "Virusvarianten_Gesamtgenomsequenzierung.csv"
name_output_df_VOC = 'Dataframes\\df_VOC.csv'

pfad_output = "Github\\Auswertung_Covid_19\\output\\"
pfad_onedrive = "OneDrive\\Auswertung_Covid_19\\"
pfad_input = "Github\\Auswertung_Covid_19\\input\\"
name_performance = 'Dataframes\\df_performance.csv'

name_6_1 = "plot_6-1_Änderungsrate MW cases"
name_6_2 = "plot_6-2_VOC"
name_9 = "plot_9_Anteil_VOC_ger.png" # Variants of Concern

# Webabruf - CSV einlesen
data = pd.read_csv("https://covid19.who.int/WHO-COVID-19-global-data.csv")

data['Date_reported'] = pd.to_datetime(data.Date_reported, utc=True)


# Preprocessing

# Filter: Country
df = data[data.Country == 'Germany']

# Referenzdatum
ts = pd.to_datetime('2021-01-15', utc=True)   # YYYY-MM-DD

# Spalten entfernen
df = df.drop(columns=['Country_code', 'WHO_region', 'Country', 
                      'Cumulative_cases', 'New_deaths', 
                      'New_deaths', 'Cumulative_deaths'])

#Datum Filter
df = df.loc[df.Date_reported >= ts, :]

# df["Country"].unique()

# Mittelwert
df["MA"] = df["New_cases"].rolling(window=7, min_periods=1).mean()
df.head(1)


df["change_1"] = 100 * df["MA"].pct_change(periods=1)   # Berechnung OK - 20.02.2021 PW

df["change_1_MW"] = df["change_1"].rolling(window=7, min_periods=1, center=True).mean()  # OK 20.02.2021 PW

df["MSTD"] = df["change_1"].rolling(window=7,min_periods=1).std()

df["change_1_MW_std+"] = df["change_1_MW"] + df["MSTD"]
df["change_1_MW_std-"] = df["change_1_MW"] - df["MSTD"]

# ger_change["change_1_MW_std+"] = ger_change["change_1_MW"] + 
# ger_change["change_1_MW_std-"] = 

df["week_isocalendar"] = df["Date_reported"].dt.isocalendar().week 

df["R1"] = 0

#df



plt.style.use('seaborn')
fig, ax = plt.subplots(figsize=(h, v*1.2))

# # Neue Fälle pro Tag pro 100.000 Einwohner - 02.12.2020 

# Datenpunkte
ax1 = plt.plot(df.Date_reported,df['change_1'], color="grey", linestyle = '',
               marker='.', markersize = size,
               label = "Änderung: 1 Tag")

# Grenzlinie
ax5 = plt.plot(df.Date_reported,df['R1'], color="red", linestyle = 'dashed', linewidth = lwb, 
               label = "Keine Änderung")

# Mittelwert
ax6 = plt.plot(df.Date_reported,df['change_1_MW'], color="black", linestyle = '-', linewidth = lwb, 
               label = "Änderung: Mittelwert 7 Tage")

# # sigma
# ax6 = plt.plot(df.Date_reported,df['change_1_MW_std+'], color="grey", linestyle = '-', linewidth = lwb, 
#                label = "± 1 sigma")

# ax6 = plt.plot(df.Date_reported,df['change_1_MW_std-'], color="grey", linestyle = '-', linewidth = lwb, 
#                label = "")


plt.fill_between(df.Date_reported, df['change_1_MW_std+'], df['change_1_MW_std-'] , 
                 color='grey',alpha=0, interpolate=True)

# fill area between lines
plt.fill_between(df.Date_reported, df['change_1_MW'], df['R1'], label = "Verringerung Neuinfektionen", 
                 color='green',alpha=0.5, interpolate=True, where = df['change_1_MW'] < 0 )

plt.fill_between(df.Date_reported, df['change_1_MW'], df['R1'], label = "Erhöhung Neuinfektionen", 
                 color='red',alpha=0.5, interpolate=True, where = df['change_1_MW'] > 0 )


# # fill area between lines
# plt.fill_between(df.Date_reported, df['change_1_MW_std-'], df['R1'], label = "Verringerung Neuinfektionen", 
#                  color='green',alpha=0.5, interpolate=True, where = df['change_1_MW_std-'] < 0 )

# plt.fill_between(df.Date_reported, df['change_1_MW_std+'], df['R1'], label = "Erhöhung Neuinfektionen", 
#                  color='red',alpha=0.5, interpolate=True, where = df['change_1_MW_std+'] > 0 )



plt.legend(loc='upper center', 
           bbox_to_anchor=(0.5, -0.1),
           fancybox=True, 
           shadow=True, 
           ncol=3, 
           fontsize=size)

# Schriftgrößen x und y achsenwerte
plt.xticks(fontsize=size - 3, rotation = 0)
plt.yticks(fontsize=size -3)

plt.ylabel('Änderungsrate Neuinfektionen [%]', fontsize=size)
plt.xlabel('Zeit', fontsize=size)

plt.title('Änderungsrate Neuinfektionen [%] (WHO-Daten)\n', fontsize=size+10)
plt.suptitle(today + ' PW', fontsize=size-5, y=0.92)

# ax.set_ylim(ymin=-30)
# ax.set_ylim(ymax=30)

locator = mdates.AutoDateLocator(minticks=minticks, maxticks=maxticks)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)


# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output +  name_6_1, dpi = dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive +  name_6_1, dpi = dpi, bbox_inches='tight')




# plt.show()
# plt.close()


# Größe im 16:9 format und mit Umrechnungsfaktor 1.2 (durch Test ermittelt) für PowerPoint angepasst
# plt.figure(figsize=(h*1.4,v))

def y_axis_thousands(x, pos):
   # 'The two args are the value and tick position'
    return '{:0,d}'.format(int(x)).replace(",",".")
formatter = FuncFormatter(y_axis_thousands)

fig, ax = plt.subplots(figsize=(h, v))

ax.yaxis.set_major_formatter(formatter)


# Neue Fälle pro Tag pro 100.000 Einwohner - 02.12.2020 
ax1 = plt.plot(df.Date_reported,df['MA'], color="blue", linestyle = 'solid', linewidth = lwb, 
               label = "Deutschland\n(7-Tage Mittel)")
ax2 = plt.plot(df.Date_reported,df['New_cases'], marker='.', linestyle='', color="black", markersize = 20)


plt.legend(loc='upper center', 
           bbox_to_anchor=(0.5, -0.3),
           fancybox=True, 
           shadow=True, 
           ncol=3, 
           fontsize=size)

# Schriftgrößen x und y achsenwerte
plt.xticks(fontsize=size - 3, rotation = 0)
plt.yticks(fontsize=size -3)

plt.ylabel('Neue Fälle', fontsize=size)
plt.xlabel('Zeit', fontsize=size)

plt.title('Neue Fälle pro Tag - Deutschland (WHO-Daten)\n', fontsize=size+10)
plt.suptitle(today + ' PW', fontsize=size-5, y=0.92)

# fill area between lines
# plt.fill_between(df.Date_reported, ger['OTG_cases'], ger['UTG_cases'] , color='red',alpha=0.5)

ax.set_ylim(ymin=0)

locator = mdates.AutoDateLocator(minticks=minticks, maxticks=maxticks)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)


# Diagramm als Bild exporieren und Auflösung definieren
# plt.savefig(Laufwerk + pfad_output +  name_4_1, dpi = dpi, bbox_inches='tight')
# plt.savefig(Laufwerk + pfad_onedrive +  name_4_1, dpi = dpi, bbox_inches='tight')

# plt.show()
# plt.close()


# Datenimport VOC
df_VOC = pd.read_csv(Laufwerk + pfad_input + name_input_VOC, sep=";", decimal=".")

# Prozente der Varianten ausrechnen
df_VOC["n_B_1_617"] = 100 * ( df_VOC["B_1_617"] / df_VOC["Testanzahl_VOC"] )
df_VOC["n_B_1_1_7"] = 100 * ( df_VOC["B_1_1_7"] / df_VOC["Testanzahl_VOC"] )
df_VOC["n_B_1_351"] = 100 * ( df_VOC["B_1_351"] / df_VOC["Testanzahl_VOC"] )
df_VOC["n_P_1"] = 100 * ( df_VOC["P_1"] / df_VOC["Testanzahl_VOC"] )
df_VOC["n_alle_anderen"] = 100 - df_VOC["n_B_1_1_7"] - df_VOC["n_B_1_351"] - df_VOC["n_P_1"] - df_VOC["n_B_1_617"]
df_VOC


plt.figure(figsize=(h,v*1.22))
plt.style.use('seaborn')

w=0.40

x=df_VOC["KW"].tolist()
bar1 = np.arange(len(x))
bar2 = [i+w for i in bar1]


p1 = plt.bar(x=bar1, height=df_VOC["n_B_1_1_7"], width = 0.4, 
             align = 'center', color = "blue", label = "Alpha - B.1.1.7 (Großbritannien)")

p2 = plt.bar(x=bar1, height=df_VOC["n_B_1_617"], width = 0.4, ###
             align = 'center', color = "red", 
             bottom= df_VOC["n_B_1_1_7"], 
             label = "Delta - B.1.617 (Indien)")

p3 = plt.bar(x=bar1, height=df_VOC["n_B_1_351"], width = 0.4, 
             align = 'center', color = "black", 
             bottom= np.array(df_VOC["n_B_1_1_7"]) + np.array(df_VOC["n_B_1_617"]), 
             label = "Beta - B.1.351 (Südafrika)")

p4 = plt.bar(x=bar1, height=df_VOC["n_P_1"], width = 0.4, ###
             align = 'center', color = "yellow", 
             bottom=  np.array(df_VOC["n_B_1_1_7"]) + np.array(df_VOC["n_B_1_617"]) + np.array(df_VOC["n_B_1_351"]), 
             label = "Gamma - P.1 (Amazonas)")

p5 = plt.bar(x=bar1, height=df_VOC["n_alle_anderen"], width = 0.4, ###
             align = 'center', color = "grey", 
             bottom=  np.array(df_VOC["n_B_1_1_7"]) + np.array(df_VOC["n_B_1_617"]) + np.array(df_VOC["n_B_1_351"]) + np.array(df_VOC["n_P_1"]), 
             label = "Anteil alle anderen")



# # Schriftgrößen x und y achsenwerte
plt.xticks(bar1, x,fontsize=size - 5, rotation=45)
plt.yticks(fontsize=size -4)

plt.yticks(np.arange(0, 100+1, 10))


plt.ylabel('Anteil Virusvariante [in %]', fontsize=size)
plt.xlabel('Zeit', fontsize=size, rotation=0)

plt.title('Deutschland: Anteil "Variants of Concern" RKI-Testzahlenerfassung [in %]\n', fontsize=size)
plt.suptitle(today + ' PW', fontsize=size-5, y=0.91)


plt.legend(loc='upper center', 
           bbox_to_anchor=(0.5, -0.15),
           fancybox=True, 
           shadow=True, 
           ncol=2, 
           fontsize=size)

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + name_9, dpi = dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + name_9, dpi = dpi, bbox_inches='tight')

# plt.show()
#plt.show()


# Datenimport VOC
df_VOC = pd.read_csv(Laufwerk + pfad_input + name_input_VOC_GGS, sep=";", decimal=".")

# Prozente der Varianten ausrechnen
df_VOC["Testanzahl_VOC"] = df_VOC["Alle_Anderen"] + df_VOC["B_1_1_7"] + df_VOC["B_1_351"] + df_VOC["P_1"] + df_VOC["B_1_617"]
df_VOC["n_B_1_1_7"] = 100 * ( df_VOC["B_1_1_7"] / df_VOC["Testanzahl_VOC"] )
df_VOC["n_B_1_617"] = 100 * ( df_VOC["B_1_617"] / df_VOC["Testanzahl_VOC"] )
df_VOC["n_B_1_351"] = 100 * ( df_VOC["B_1_351"] / df_VOC["Testanzahl_VOC"] )
df_VOC["n_P_1"] = 100 * ( df_VOC["P_1"] / df_VOC["Testanzahl_VOC"] )
df_VOC["n_alle_anderen"] = 100 - df_VOC["n_B_1_1_7"] - df_VOC["n_B_1_351"] - df_VOC["n_P_1"] - df_VOC["n_B_1_617"]
df_VOC=df_VOC.dropna()
df_VOC


AnzahlWochen = len(df_VOC["KW"])
print(AnzahlWochen)

HeightChart1 = df_VOC



plt.figure(figsize=(h,v*1.22))
plt.style.use('seaborn')

w=0.40

x=df_VOC["KW"].tolist()
bar1 = np.arange(len(x))
bar2 = [i+w for i in bar1]


p1 = plt.bar(x=bar1, height=df_VOC["n_B_1_1_7"], width = 0.4, 
             align = 'center', color = "blue", label = "Alpha - B.1.1.7 (Großbritannien)")

p2 = plt.bar(x=bar1, height=df_VOC["n_B_1_617"], width = 0.4, ###
             align = 'center', color = "red", 
             bottom= df_VOC["n_B_1_1_7"], 
             label = "Delta - B.1.617 (Indien)")

p3 = plt.bar(x=bar1, height=df_VOC["n_B_1_351"], width = 0.4, 
             align = 'center', color = "black", 
             bottom= np.array(df_VOC["n_B_1_1_7"]) + np.array(df_VOC["n_B_1_617"]), 
             label = "Beta - B.1.351 (Südafrika)")

p4 = plt.bar(x=bar1, height=df_VOC["n_P_1"], width = 0.4, ###
             align = 'center', color = "yellow", 
             bottom=  np.array(df_VOC["n_B_1_1_7"]) + np.array(df_VOC["n_B_1_617"]) + np.array(df_VOC["n_B_1_351"]), 
             label = "Gamma - P.1 (Amazonas)")

p5 = plt.bar(x=bar1, height=df_VOC["n_alle_anderen"], width = 0.4, ###
             align = 'center', color = "grey", 
             bottom=  np.array(df_VOC["n_B_1_1_7"]) + np.array(df_VOC["n_B_1_617"]) + np.array(df_VOC["n_B_1_351"]) + np.array(df_VOC["n_P_1"]), 
             label = "Anteil alle anderen")



# # Schriftgrößen x und y achsenwerte
plt.xticks(bar1, x,fontsize=size - 5, rotation=45)
plt.yticks(fontsize=size -4)

plt.yticks(np.arange(0, 100+1, 10))


plt.ylabel('Anteil Virusvarianten [in %]', fontsize=size)
plt.xlabel('Zeit', fontsize=size, rotation=0)

plt.title('Deutschland: Anteil "Variants of Concern" RKI-Gesamtgenomsequenzierung [in %]\n', fontsize=size)
plt.suptitle(today + ' PW', fontsize=size-5, y=0.91)


plt.legend(loc='upper center', 
           bbox_to_anchor=(0.5, -0.15),
           fancybox=True, 
           shadow=True, 
           ncol=2, 
           fontsize=size)

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + "GGS" + name_9, dpi = dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + "GGS" + name_9, dpi = dpi, bbox_inches='tight')

# plt.show()
#plt.show()


# y-achse finde die MAX höhe
df_VOC["n_alleVOC"] = df_VOC["n_B_1_617"] + df_VOC["n_B_1_351"] + df_VOC["n_P_1"]
max_höhe = round(df_VOC["n_alleVOC"].max(),0)
print(max_höhe)

plt.figure(figsize=(h,v*1.22))
plt.style.use('seaborn')

w=0.40

x=df_VOC["KW"].tolist()
bar1 = np.arange(len(x))
bar2 = [i+w for i in bar1]


# p1 = plt.bar(x=bar1, height=df_VOC["n_B_1_1_7"], width = 0.4, 
#              align = 'center', color = "blue", label = "Alpha - B.1.1.7 (Großbritannien)")

p2 = plt.bar(x=bar1, height=df_VOC["n_B_1_617"], width = 0.4, ###
             align = 'center', color = "red",  
             label = "Delta - B.1.617 (Indien)")

p3 = plt.bar(x=bar1, height=df_VOC["n_B_1_351"], width = 0.4, 
             align = 'center', color = "black", 
             bottom= np.array(np.array(df_VOC["n_B_1_617"])), 
             label = "Beta - B.1.351 (Südafrika)")

p4 = plt.bar(x=bar1, height=df_VOC["n_P_1"], width = 0.4, ###
             align = 'center', color = "yellow", 
             bottom=  np.array(np.array(df_VOC["n_B_1_617"]) + np.array(df_VOC["n_B_1_351"])), 
             label = "Gamma - P.1 (Amazonas)")

# p5 = plt.bar(x=bar1, height=df_VOC["n_alle_anderen"], width = 0.4, ###
#              align = 'center', color = "grey", 
#              bottom=  np.array(df_VOC["n_B_1_1_7"]) + np.array(df_VOC["n_B_1_617"]) + np.array(df_VOC["n_B_1_351"]) + np.array(df_VOC["n_P_1"]), 
#              label = "Anteil alle anderen")



# # Schriftgrößen x und y achsenwerte
plt.xticks(bar1, x,fontsize=size - 5, rotation=45)
plt.yticks(fontsize=size -4)

# y-achse soll 10% höher sein als der max Wert und immer in 10 Teile teilen
plt.yticks(np.arange(0, max_höhe+max_höhe/10, max_höhe/10))


plt.ylabel('Anteil Virusvarianten [in %]', fontsize=size)
plt.xlabel('Zeit', fontsize=size, rotation=0)

plt.title('Deutschland: Anteil "Variants of Concern" RKI-Gesamtgenomsequenzierung [in %]\n', fontsize=size)
plt.suptitle(today + ' PW', fontsize=size-5, y=0.91)


plt.legend(loc='upper center', 
           bbox_to_anchor=(0.5, -0.15),
           fancybox=True, 
           shadow=True, 
           ncol=2, 
           fontsize=size)

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + "GGS2" + name_9, dpi = dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + "GGS2" + name_9, dpi = dpi, bbox_inches='tight')

# plt.show()
#plt.show()

plt.figure(figsize=(h,v*1.22))
plt.style.use('seaborn')

w=0.40

x=df_VOC["KW"].tolist()
bar1 = np.arange(len(x))
bar2 = [i+w for i in bar1]


# p1 = plt.bar(x=bar1, height=df_VOC["n_B_1_1_7"], width = 0.4, 
#              align = 'center', color = "blue", label = "Alpha - B.1.1.7 (Großbritannien)")

p2 = plt.bar(x=bar1, height=df_VOC["B_1_617"], width = 0.4, ###
             align = 'center', color = "red",  
             label = "Delta - B.1.617 (Indien)")

p3 = plt.bar(x=bar1, height=df_VOC["B_1_351"], width = 0.4, 
             align = 'center', color = "black", 
             bottom= np.array(np.array(df_VOC["B_1_617"])), 
             label = "Beta - B.1.351 (Südafrika)")

p4 = plt.bar(x=bar1, height=df_VOC["P_1"], width = 0.4, ###
             align = 'center', color = "yellow", 
             bottom=  np.array(np.array(df_VOC["B_1_617"]) + np.array(df_VOC["B_1_351"])), 
             label = "Gamma - P.1 (Amazonas)")

# p5 = plt.bar(x=bar1, height=df_VOC["n_alle_anderen"], width = 0.4, ###
#              align = 'center', color = "grey", 
#              bottom=  np.array(df_VOC["n_B_1_1_7"]) + np.array(df_VOC["n_B_1_617"]) + np.array(df_VOC["n_B_1_351"]) + np.array(df_VOC["n_P_1"]), 
#              label = "Anteil alle anderen")



# # Schriftgrößen x und y achsenwerte
plt.xticks(bar1, x,fontsize=size - 5, rotation=45)
plt.yticks(fontsize=size -4)

plt.yticks(np.arange(0, 250+1, 25))


plt.ylabel('Virusvarianten - Absolute Zahlen', fontsize=size)
plt.xlabel('Zeit', fontsize=size, rotation=0)

plt.title('Deutschland: "Variants of Concern" RKI-Gesamtgenomsequenzierung\n', fontsize=size)
plt.suptitle(today + ' PW', fontsize=size-5, y=0.91)


plt.legend(loc='upper center',
           bbox_to_anchor=(0.5, -0.15),
           fancybox=True, 
           shadow=True, 
           ncol=2, 
           fontsize=size)

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + "GGS3" + name_9, dpi = dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + "GGS3" + name_9, dpi = dpi, bbox_inches='tight')

# plt.show()
# plt.show()