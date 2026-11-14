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
import plotly.graph_objects as go
import matplotlib.dates as mdates
from scipy import stats
from scipy.special import  inv_boxcox
from ProjektDekompozycja import data, polyreg
from scipy.stats import percentileofscore
from scipy.stats import t
import torch
from chronos import ChronosPipeline
from sklearn.metrics import mean_squared_error

# Ustawienia stylu podobne do ggplot2


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
    titlesize=16,
    titlepad=10,
)
sns.set_theme(style='whitegrid',
              context='paper',
              palette='dark')


future_data = np.array([17.08, 17.2, 17.42, 17.38, 17.35,
               17.36, 16.18, 16.18, 15.94, 15.95,
               16.1, 16.1, 16.58, 16.83, 13.67, 14.37]) * 100 # z milionów hektolitrów (10^8) na megalitry (10^6)

sarima_predict = pd.read_csv('forecast_output_sarima.csv')
ar_predict = pd.read_csv('prediction_ar4.csv')

#Skumulowanie wartości dla SARIMY
sarima_predict['year'] = sarima_predict['time'].astype(int)
result1 = sarima_predict.groupby('year')['forecast'].sum().reset_index()
result1.rename(columns={'forecast': 'total_forecast_sarima'}, inplace=True)

# Zaczynamy od Q1
# Kończymy na Q2 2010
# predykcje wielomianową zaczniemy od t=72


#Skumulowanie wartości dla AR(4)
trend_predict = np.polyval(polyreg[2]['for_predict'], np.arange(72, 72+64))
season_predict = np.tile(polyreg[2]['season'][:4], 16)[:64]
ar_predict['Prediction'] = ar_predict['Prediction'] + trend_predict + season_predict
ar_predict['year'] = ar_predict['Time'].astype(int)
result2 = ar_predict.groupby('year')['Prediction'].sum().reset_index()
result2.rename(columns={'Prediction': 'total_forecast_ar'}, inplace=True)


#### SKumulowane wartości dla Chronosa

pipeline = ChronosPipeline.from_pretrained(
  "amazon/chronos-t5-small",
  device_map="cpu",
  torch_dtype=torch.bfloat16,
)

# context must be either a 1D tensor, a list of 1D tensors,
# or a left-padded 2D tensor with batch as the first dimension
context = torch.tensor(np.array(data['value']))
prediction_length = 64 #63
forecast = pipeline.predict(context, 1, prediction_length)  # shape [num_series, num_samples, prediction_length]
forecast = forecast.numpy()[0].flatten()

forecast_sum_chronos = np.array([np.sum(forecast[i:i+4]) for i in range(0, len(forecast), 4)])


result = pd.DataFrame({'year': result1['year'], 'true value': future_data,
                       'total_forecast_sarima': result1['total_forecast_sarima'],
                       'total_forecast_ar': result2['total_forecast_ar'],
                       'total_forecast_chronos': forecast_sum_chronos})

mse_sarima = mean_squared_error(result['true value'], result['total_forecast_sarima'])
mse_ar = mean_squared_error(result['true value'], result['total_forecast_ar'])
mse_chronos = mean_squared_error(result['true value'], result['total_forecast_chronos'])

print(f"MSE dla prognozy SARIMA: {mse_sarima}")
print(f"MSE dla prognozy AR: {mse_ar}")
print(f"MSE dla prognozy Chronos: {mse_chronos}")

plt.figure(figsize=(8, 5))
sns.lineplot(data=result, x='year', y='true value', color='black', marker='o', label='wartości')
sns.lineplot(data=result, x='year', y='total_forecast_sarima', color='red', marker='1', label='SARIMA')
sns.lineplot(data=result, x='year', y='total_forecast_ar', color='green', marker='2', label='AR(4)')
sns.lineplot(data=result, x='year', y='total_forecast_chronos', color='blue', marker='3', label='Chronos-small')
plt.title('Produkcja piwa w Australii - predykcja', loc='center')
plt.xlabel('Lata')
plt.ylabel('Megalitry')
plt.tight_layout()
plt.savefig('wykres8.png', format='png', bbox_inches='tight')
plt.show()

