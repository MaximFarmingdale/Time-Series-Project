import numpy as np
import polars as pl 
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
from darts import TimeSeries
from darts.models import AutoARIMA, ExponentialSmoothing, LightGBMModel
from darts.metrics import  mae





rawPassword = "password"
encodedPassword = urllib.parse.quote_plus(rawPassword)
connection = f"postgresql+psycopg://postgres:{encodedPassword}@localhost:5432/Time_Series"
engine = create_engine(connection)
query = "SELECT * FROM insurance_claims"
df = pl.read_database(query, engine)
# turning data monthly
df =df.group_by_dynamic("Claim_Date", every="1mo").agg(pl.col("Claim_Amount").sum())
timeSeries = TimeSeries.from_dataframe(df, time_col="Claim_Date", value_cols="Claim_Amount", freq="MS",)
expModel = ExponentialSmoothing()
arimaModel = AutoARIMA()
lightgbmModel = LightGBMModel(lags = 12)
#model uses the window of 12 months

expTest = expModel.historical_forecasts(
    series = timeSeries,
    start = pd.Timestamp("2024"),
    forecast_horizon= 12, 
    stride=1,
    retrain=True,
    verbose=True
    )

arimaTest = arimaModel.historical_forecasts(
    series = timeSeries,
    start = pd.Timestamp("2024"),
    forecast_horizon= 12, 
    stride=1,
    retrain=True,
    verbose=True
    )
lightgbmTest = lightgbmModel.historical_forecasts(
    series = timeSeries,
    start = pd.Timestamp("2024"),
    forecast_horizon= 12, 
    stride=1,
    retrain=True,
    verbose=True
    )

expmae = mae(timeSeries, expTest)
arimamae = mae(timeSeries, arimaTest)
lightgbmmae = mae(timeSeries, lightgbmTest)

resultsPD = pl.DataFrame({
    "Models": ["Exponential", "ARIMA", "lightGBM", "RRN"],
    "MAE": [expmae,arimamae,lightgbmmae]}).sort(pl.col("MAE"))
print(f"\n The mae for the exponential smoothing model is {expmae} \n")
print(f"The mae for the ARIMA model is {arimamae} \n")
print(f"The mae for the lightGBM model is {lightgbmmae}\n")

expModel.fit(timeSeries)
arimaModel.fit(timeSeries)
lightgbmModel.fit(timeSeries)

expData = expModel.predict(24).to_dataframe(backend = "polars")
arimaData = arimaModel.predict(24).to_dataframe(backend = "polars")
lightgbmData = lightgbmModel.predict(24).to_dataframe(backend = "polars")

expData.write_csv("exponential_smoothing_data.csv")
arimaData.write_csv("arima_smoothing_data.csv")
lightgbmData.write_csv("lightgbm_smoothing_data.csv")