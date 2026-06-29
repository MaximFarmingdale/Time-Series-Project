## Introduction

This is an implementation of Time Series models used on synthetic data of claim amounts per day for 10 years using Python, PostgreSQL and Excel. This is meant to parallel real workflows that are done in the insurance industry.

## Data Creation

Python is used to create the data in a way that mimics economic and growth factors that would be present in real insurance data. A Poisson distribution is used to simulate the number of claims per day, the mean parameter is influenced by the season, with summer and winter having a higher lambda, and a growth factor is added to simulate the growth of the insurance company. Most claims then follow a lognormal distribution to simulate a small claim, while there is also a 0.5% chance of getting a large normally distributed claim. This data is then saved to a PostgreSQL database. The Polars library is used for storage, while numpy is used for the statistical distributions used to generate the data, and SQLAlchemy is used to write to the PostgreSQL database.

## Models

Python is then used again to build models from the data, namely an exponential smoothing model, an AutoRegressive Integrated Moving Average (Auto ARIMA) model, and a Light Gradient Boosting Machine (LightGBM) model. These models are created with the darts library; Polars and Pandas are used for data storage and SQLAlchemy is used to read from the  PostgreSQL database. Before the data is evaluated, the daily claim amounts are aggregated into monthly amounts. Each model is tested using its Mean Absolute Error using rolling origin backtests starting in the 8th year. The model that got the lowest score was exponential, then Auto ARIMA and finally LightGBM. These models are then used to simulate the claim amount each month of the next two years and the data is saved to a CSV file.

## Excel Data Analysis

In Excel, the data is pulled from PostgreSQL into a table and two pivot tables are created, one is a table with data grouped by year and quarter, and the second table of data is grouped by month. The first table is used to create a line chart showing long term cycles of the data, while the second table shows the seasonal trend of the data, with more claims in the summer and winter. Each CSV file of the predictions by each model is then loaded into Excel and a sheet. The user is able to look up the simulated claim amounts per month for the next two years.
