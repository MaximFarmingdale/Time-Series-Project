# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 13:01:23 2026

@author: Maxim
"""
import numpy as np
import polars as pl 
from datetime import datetime, timedelta
import uuid 
import urllib.parse
from sqlalchemy import create_engine
startDate = datetime(2016, 1, 1).date()
endDate = datetime(2026, 1, 1).date()
claims = []
rangeDate = pl.date_range(
    start = startDate,
    end = endDate,
    interval = "1d", 
    eager = True
    )
np.random.seed(2222)
for date in rangeDate:
    
    baseRate = 10
    month = date.month
    seasonalChange = 0
    if month in [12, 1, 2] : 
        seasonalChange = 2
    elif month in [6, 7,8]:
        seasonalChange = 1.5 
    growthTrend = np.random.normal(((date - startDate).days * .006), .04)
    lambdaValue = baseRate + seasonalChange + growthTrend
    numClaims = np.random.poisson(lam = lambdaValue)
    for i in range(numClaims):
        inflation = 1.0226 ** ((date - startDate).days / 365)
        if np.random.rand() < .005:
            finalValue = np.random.normal(30000, 7000) * inflation
        else:
            baseValue = np.random.lognormal(10, 1)
            finalValue = baseValue * inflation
        claims.append({
            "Claim_ID": uuid.uuid4(),
            "Claim_Date": date,
            "Claim_Amount": finalValue,
        })
df = pl.DataFrame(claims)

rawPassword = "password"
encodedPassword = urllib.parse.quote_plus(rawPassword)
connection = f"postgresql+psycopg://postgres:{encodedPassword}@localhost:5432/Time_Series"
engine = create_engine(connection)
try:
    with engine.begin() as conn:
        df.write_database(
            table_name= "insurance_claims",
            connection = conn,
            if_table_exists= "replace", 
            engine ="sqlalchemy")
        print("Success")
except Exception as e:
    print(e)