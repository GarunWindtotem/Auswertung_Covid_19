import pandas as pd  # Daten
from matplotlib import pyplot as plt  # plots
import numpy as np

# performance
from datetime import datetime
from datetime import date  # todays date

########################################################################################################################
import os

print('__file__:    ', __file__)
print('basename:    ', os.path.basename(__file__))
print('dirname:     ', os.path.dirname(__file__))
print('abspath:     ', os.path.abspath(__file__))
print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))

now = datetime.now()

# Linien Stärke
lws = 3
lwb = 7
# Bezugsschriftgröße
size = 25

# output größe der bilder
h = 16 * 1.2
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

name_1 = "GGS plot 1 alle voc Anteil.png"
name_2 = "GGS plot 2 voc ohne alpha Anteil.png"
name_3 = "GGS plot 3 voc ohne alpha abs Zahlen.png"
name_4 = "GGS plot 1 alle voc abs Zahlen.png"

# Webabruf - CSV einlesen
data = pd.read_csv("https://covid19.who.int/WHO-COVID-19-global-data.csv")

data['Date_reported'] = pd.to_datetime(data.Date_reported, utc=True)

########################################################################################################################

# Datenimport VOC
df_VOC = pd.read_csv(Laufwerk + pfad_input + name_input_VOC_GGS, sep=";", decimal=".")

# Prozente der Varianten ausrechnen
df_VOC["Testanzahl_VOC"] = df_VOC["Alle_Anderen"] + df_VOC["B_1_1_7"] + df_VOC["B_1_351"] + df_VOC["P_1"] + df_VOC[
    "B_1_617"]
df_VOC["n_B_1_1_7"] = 100 * (df_VOC["B_1_1_7"] / df_VOC["Testanzahl_VOC"])
df_VOC["n_B_1_617"] = 100 * (df_VOC["B_1_617"] / df_VOC["Testanzahl_VOC"])
df_VOC["n_B_1_351"] = 100 * (df_VOC["B_1_351"] / df_VOC["Testanzahl_VOC"])
df_VOC["n_P_1"] = 100 * (df_VOC["P_1"] / df_VOC["Testanzahl_VOC"])
df_VOC["n_alle_anderen"] = 100 - df_VOC["n_B_1_1_7"] - df_VOC["n_B_1_351"] - df_VOC["n_P_1"] - df_VOC["n_B_1_617"]
df_VOC = df_VOC.dropna()

AnzahlWochen = len(df_VOC["KW"])
print(AnzahlWochen)

#######################################################################################################################
# plot 1 alle voc - Anteil
#######################################################################################################################
plt.figure(figsize=(h, v * 1.22))
plt.style.use('seaborn')

w = 0.40

x = df_VOC["KW"].tolist()
bar1 = np.arange(len(x))
bar2 = [i + w for i in bar1]

p11 = plt.bar(x=bar1, height=df_VOC["n_B_1_1_7"], width=0.4,
              align='center', color="blue", label="Alpha - B.1.1.7 (Großbritannien)")

p12 = plt.bar(x=bar1, height=df_VOC["n_B_1_617"], width=0.4,  ###
              align='center', color="red",
              bottom=df_VOC["n_B_1_1_7"],
              label="Delta - B.1.617 (Indien)")

p13 = plt.bar(x=bar1, height=df_VOC["n_B_1_351"], width=0.4,
              align='center', color="black",
              bottom=np.array(df_VOC["n_B_1_1_7"]) + np.array(df_VOC["n_B_1_617"]),
              label="Beta - B.1.351 (Südafrika)")

p14 = plt.bar(x=bar1, height=df_VOC["n_P_1"], width=0.4,  ###
              align='center', color="yellow",
              bottom=np.array(df_VOC["n_B_1_1_7"]) + np.array(df_VOC["n_B_1_617"]) + np.array(df_VOC["n_B_1_351"]),
              label="Gamma - P.1 (Amazonas)")

p15 = plt.bar(x=bar1, height=df_VOC["n_alle_anderen"], width=0.4,  ###
              align='center', color="grey",
              bottom=np.array(df_VOC["n_B_1_1_7"]) + np.array(df_VOC["n_B_1_617"]) + np.array(
                  df_VOC["n_B_1_351"]) + np.array(df_VOC["n_P_1"]),
              label="Anteil alle anderen")

# # Schriftgrößen x und y achsenwerte
plt.xticks(bar1, x, fontsize=size - 5, rotation=45)
plt.yticks(fontsize=size - 4)

plt.yticks(np.arange(0, 100 + 1, 10))

plt.ylabel('Anteil Virusvarianten [in %]', fontsize=size)
plt.xlabel('Zeit', fontsize=size, rotation=0)

plt.title('Deutschland: Anteil "Variants of Concern" RKI-Gesamtgenomsequenzierung [in %]\n', fontsize=size)
plt.suptitle(today + ' PW', fontsize=size - 5, y=0.91)

plt.legend(loc='upper center',
           bbox_to_anchor=(0.5, -0.15),
           fancybox=True,
           shadow=True,
           ncol=2,
           fontsize=size)

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + name_1, dpi=dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + name_1, dpi=dpi, bbox_inches='tight')

# plt.show()
# plt.show()

#######################################################################################################################

# y-achse finde die MAX höhe
df_VOC["n_alleVOC"] = df_VOC["n_B_1_617"] + df_VOC["n_B_1_351"] + df_VOC["n_P_1"]
max_height = round(df_VOC["n_alleVOC"].max(), 0)
print(f'max_height = {max_height}')

#######################################################################################################################
# plot 2 voc ohne alpha - Anteil
#######################################################################################################################

plt.figure(figsize=(h, v * 1.22))
plt.style.use('seaborn')

w = 0.40

x = df_VOC["KW"].tolist()
bar1 = np.arange(len(x))

# p21 = plt.bar(x=bar1, height=df_VOC["n_B_1_1_7"], width = 0.4,
#              align = 'center', color = "blue", label = "Alpha - B.1.1.7 (Großbritannien)")

p22 = plt.bar(x=bar1, height=df_VOC["n_B_1_617"], width=0.4,  ###
              align='center', color="red",
              label="Delta - B.1.617 (Indien)")

p23 = plt.bar(x=bar1, height=df_VOC["n_B_1_351"], width=0.4,
              align='center', color="black",
              bottom=np.array(np.array(df_VOC["n_B_1_617"])),
              label="Beta - B.1.351 (Südafrika)")

p24 = plt.bar(x=bar1, height=df_VOC["n_P_1"], width=0.4,  ###
              align='center', color="yellow",
              bottom=np.array(np.array(df_VOC["n_B_1_617"]) + np.array(df_VOC["n_B_1_351"])),
              label="Gamma - P.1 (Amazonas)")

# # Schriftgrößen x und y achsenwerte
plt.xticks(bar1, x, fontsize=size - 5, rotation=45)
plt.yticks(fontsize=size - 4)

# y-achse soll 10% höher sein als der max Wert und immer in 10 Teile teilen
plt.yticks(np.arange(0, max_height + max_height / 10, max_height / 10))

plt.ylabel('Anteil Virusvarianten [in %]', fontsize=size)
plt.xlabel('Zeit', fontsize=size, rotation=0)

plt.title('Deutschland: Anteil "Variants of Concern" RKI-Gesamtgenomsequenzierung [in %]\n', fontsize=size)
plt.suptitle(today + ' PW', fontsize=size - 5, y=0.91)

plt.legend(loc='upper center',
           bbox_to_anchor=(0.5, -0.15),
           fancybox=True,
           shadow=True,
           ncol=2,
           fontsize=size)

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + name_2, dpi=dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + name_2, dpi=dpi, bbox_inches='tight')

# plt.show

#######################################################################################################################

# y-achse finde die MAX höhe
df_VOC["alleVOC"] = df_VOC["B_1_617"] + df_VOC["B_1_351"] + df_VOC["P_1"]
max_height_abs = round(df_VOC["alleVOC"].max(), 0)
print(f'max_height_abs = {max_height_abs}')

#######################################################################################################################
# plot 2 voc ohne alpha - abs Zahlen
#######################################################################################################################

plt.figure(figsize=(h, v * 1.22))
plt.style.use('seaborn')

x = df_VOC["KW"].tolist()
bar1 = np.arange(len(x))

# p31 = plt.bar(x=bar1, height=df_VOC["n_B_1_1_7"], width = 0.4,
#              align = 'center', color = "blue", label = "Alpha - B.1.1.7 (Großbritannien)")

p32 = plt.bar(x=bar1, height=df_VOC["B_1_617"], width=0.4,
              align='center', color="red",
              label="Delta - B.1.617 (Indien)")

p33 = plt.bar(x=bar1, height=df_VOC["B_1_351"], width=0.4,
              align='center', color="black",
              bottom=np.array(np.array(df_VOC["B_1_617"])),
              label="Beta - B.1.351 (Südafrika)")

p34 = plt.bar(x=bar1, height=df_VOC["P_1"], width=0.4,
              align='center', color="yellow",
              bottom=np.array(np.array(df_VOC["B_1_617"]) + np.array(df_VOC["B_1_351"])),
              label="Gamma - P.1 (Amazonas)")

# # Schriftgrößen x und y achsenwerte
plt.xticks(bar1, x, fontsize=size - 5, rotation=45)
plt.yticks(fontsize=size - 4)

plt.yticks(np.arange(0, max_height_abs + max_height_abs / 10, round(max_height_abs / 10, 0)))

plt.ylabel('Virusvarianten - Absolute Zahlen', fontsize=size)
plt.xlabel('Zeit', fontsize=size, rotation=0)

plt.title('Deutschland: "Variants of Concern" RKI-Gesamtgenomsequenzierung\n', fontsize=size)
plt.suptitle(today + ' PW', fontsize=size - 5, y=0.91)

plt.legend(loc='upper center',
           bbox_to_anchor=(0.5, -0.15),
           fancybox=True,
           shadow=True,
           ncol=2,
           fontsize=size)

# hintergrund einfärben und Hinweistext
plt.axvspan(AnzahlWochen - AnzahlWochen * 0.07, AnzahlWochen, facecolor='grey', alpha=0.7)
plt.text(x=AnzahlWochen - AnzahlWochen * 0.08, y=0.97 * max_height_abs, s=" Daten nicht\n vollständig",
         fontsize=size * 0.8,
         horizontalalignment='left', rotation=0, color="white",
         bbox={'facecolor': "grey", 'alpha': 0.7, 'pad': 5})

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + name_3, dpi=dpi, bbox_inches='tight')
plt.savefig(Laufwerk + pfad_onedrive + name_3, dpi=dpi, bbox_inches='tight')

# plt.show()


#######################################################################################################################
# plot 2 voc ohne alpha - abs Zahlen
#######################################################################################################################

# y-achse finde die MAX höhe
df_VOC["alleVOC"] = df_VOC["B_1_1_7"] + df_VOC["B_1_617"] + df_VOC["B_1_351"] + df_VOC["P_1"]
max_height_abs = round(df_VOC["alleVOC"].max(), 0)

#######################################################################################################################


plt.figure(figsize=(h, v * 1.22))
plt.style.use('seaborn')

x = df_VOC["KW"].tolist()
bar1 = np.arange(len(x))

p32 = plt.bar(x=bar1, height=df_VOC["B_1_617"], width=0.4,
              align='center', color="red",
              label="Delta - B.1.617 (Indien)")

p31 = plt.bar(x=bar1, height=df_VOC["B_1_1_7"], width=0.4,
              align='center', color="blue",
              bottom=np.array(df_VOC["B_1_617"]),
              label="Alpha - B.1.1.7 (Großbritannien)")

p33 = plt.bar(x=bar1, height=df_VOC["B_1_351"], width=0.4,
              align='center', color="black",
              bottom=np.array(np.array(df_VOC["B_1_1_7"]) + np.array(df_VOC["B_1_617"])),
              label="Beta - B.1.351 (Südafrika)")

p34 = plt.bar(x=bar1, height=df_VOC["P_1"], width=0.4,
              align='center', color="yellow",
              bottom=np.array(np.array(df_VOC["B_1_1_7"]) + np.array(df_VOC["B_1_617"]) + np.array(df_VOC["B_1_351"])),
              label="Gamma - P.1 (Amazonas)")

# # Schriftgrößen x und y achsenwerte
plt.xticks(bar1, x, fontsize=size - 5, rotation=45)
plt.yticks(fontsize=size - 4)

# plt.yticks(np.arange(0, max_height_abs + max_height_abs / 10, round(max_height_abs / 10, 0)))

plt.ylabel('Virusvarianten - Absolute Zahlen', fontsize=size)
plt.xlabel('Zeit', fontsize=size, rotation=0)

plt.title('Deutschland: "Variants of Concern" RKI-Gesamtgenomsequenzierung\n', fontsize=size)
plt.suptitle(today + ' PW', fontsize=size - 5, y=0.91)

plt.legend(loc='upper center',
           bbox_to_anchor=(0.5, -0.15),
           fancybox=True,
           shadow=True,
           ncol=2,
           fontsize=size)

# hintergrund einfärben und Hinweistext
plt.axvspan(AnzahlWochen - AnzahlWochen * 0.07, AnzahlWochen, facecolor='grey', alpha=0.7)
plt.text(x=AnzahlWochen - AnzahlWochen * 0.08, y=0.97 * max_height_abs, s=" Daten nicht\n vollständig",
         fontsize=size * 0.8,
         horizontalalignment='left', rotation=0, color="white",
         bbox={'facecolor': "grey", 'alpha': 0.7, 'pad': 5})

# Diagramm als Bild exporieren und Auflösung definieren
plt.savefig(Laufwerk + pfad_output + name_4, dpi=dpi, bbox_inches='tight')  # ToDo: Pfad
plt.savefig(Laufwerk + pfad_onedrive + name_4, dpi=dpi, bbox_inches='tight')

# plt.show()


#######################################################################################################################
# performance
#######################################################################################################################
now2 = datetime.now()
performance = now2 - now
print(f'runtime = {round(performance.total_seconds(), 1)} seconds')
