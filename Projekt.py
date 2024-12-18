import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import arma_order_select_ic
import pyreadr
from Lista2 import ts_plot
from dm_test import dm_test


plt.rc(
    "figure",
    autolayout=True,
    figsize=(11.69,8.27),
    titlesize=10,
    titleweight='bold',
)
plt.rc(
    "axes",
    labelweight="bold",
    labelsize="large",
    titleweight="bold",
    titlesize=20,
    titlepad=10,
)
sns.set_theme(style='whitegrid',
              context='paper',
              palette='dark')

pd.set_option('display.max_columns', None)


data = sm.datasets.get_rdataset("ausbeer", package="fpp2").data

#print(data.columns)
# Mamy dwie kolumny: time i value

#print(data.value.describe())
'''
Średnia wartość: 415
STD value: 85
MIN: 213
MAX: 599
Dane w milionach hektolitrów? Potwierdzić
'''

#print(data.time)
'''
STD value: 85
Od: 1956
Do: 2010
Dane kwartalne
'''


# Funkcja do mapowania kwartałów na miesiące
def convert_to_datetime(row):
    year, quarter = str(row).split('.')
    quarter_to_month = {'0': '01', '25': '04', '5': '07', '75': '10'}
    month = quarter_to_month[quarter]
    return f"{year}-{month}-01"

data['time'] = pd.to_datetime(data['time'].apply(convert_to_datetime))

# Zwraca interaktywny wykres w JS, fajnie byłoby wykorzystać
#ts_plot(data)

# Znalazłem parę anomalii
'''
Widać na wykresie dla październik 2004 że jest znaczący spadek, chat odpowiedział:
Tak, w 2004 roku Australia doświadczyła przedłużającej się suszy, która miała znaczący wpływ na produkcję rolną, 
w tym na uprawy jęczmienia — kluczowego składnika w produkcji piwa. Mimo że areał zasiewów jęczmienia wzrósł o 4%, 
wszystkie główne stany uprawne odnotowały znaczące spadki w poziomach produkcji. 
'''

'''
Na przełomie lat 1980 i 1981 zachodzi ciekawa anomalia.
Zazwyczaj peak produkcji przypadał na październik. Dla tego okresu jest widoczny wzrost, 
jednakże peak następuje w styczniu. Z informacji które udało mi się znaleźć:

1. Były to okresy ekstremalnych susz, co mogło mieć oczywiście przełożenie na produkcję.
2. Na przełom tych lat przypada również sezon cyklonów tropikalnych który był powyżej średniej.
'''

# Dekompozycja, przyjęty model addytywny z okresem 4

docomposition = seasonal_decompose(data['value'], model='additive', period=4, extrapolate_trend='freq', filt=4*[1/4])

data['trend'] = docomposition.trend
data['season'] = docomposition.seasonal
data['noise'] = docomposition.resid

'''
fig, ax = plt.subplots(4,1, sharex=True)
fig.suptitle('Dekompozycja Beer Production')
sns.lineplot(data['value'],ax=ax[0], color='black')
ax[0].set_title('Pierwotny szereg')
sns.lineplot(data['trend'],ax=ax[1], color='darkred')
ax[1].set_title('Składowa trendu')
sns.lineplot(data['season'],ax=ax[2], color='darkgreen')
ax[2].set_title('Składowa sezonowa')
sns.lineplot(data['noise'], ax=ax[3], color='darkblue')
ax[3].set_title('Szum')
plt.tight_layout()
plt.show()
'''


fig, ax = plt.subplots(2, 1, sharex=True)
fig.suptitle('Szum BeerProduction')
plot_acf(data['noise'], ax=ax[0], color='darkgreen')
ax[0].set_title('ACF')
plot_pacf(data['noise'], ax=ax[1], color='darkgreen')
ax[1].set_title('PACF')
plt.tight_layout()
plt.show()
