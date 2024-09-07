**add-date-time-period-to ESO-demand-files**

*OVERVIEW*

A script which takes yearly historic demand electricity data CSV files as published on the National Grid ESO Data Portal and adds time and date data. The script converts the files into dataframes and adds a column with datetime data indicating the start of the settlement period and including time zones, and a column with PeriodIndex data corresponding to the relevant settlement dates and settlement periods. It then saves the altered dataframe as a CSV file.

*Programs Used:*

Python in Visual Studio Code

*Data Sources:*

•	Historic electricity demand data came from the National Grid [ESO Data Portal](https://www.nationalgrideso.com/data-portal/historic-demand-data). The data covers historic electricity national demand and transmission system demand per settlement period. It also includes figures for interconnector imports and exports, estimated embedded solar and wind generation, and hydro storage pumping demand and Non-BM Short Term Operating Reserve. I used data from 2018 to 2023. The data is available under the National Grid ESO Open Data Licence v1.0. This allows users to copy, publish, distribute, adapt and exploit the data commercially and non-commercially provided the source is acknowledged. So, this project is supported by National Grid ESO Open Data.

*Attribution:* 

Several of the functions calculating the last Sundays in March and October were very slightly adapted from a [Stack Overflow answer](https://stackoverflow.com/questions/54531558/how-do-i-know-if-today-is-a-day-due-to-change-civil-local-time-e-g-daylight-sav) by [Arount](https://stackoverflow.com/users/7200715/arount). These are available under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license and can be shared and reused providing attribution is given and the resulting contributions are shared under the same license. 

*Next steps:*

•	Look to automate process within GitHub when new data files are added along the lines of this article [Automating Data Pipelines with Python & GitHub Actions](https://towardsdatascience.com/automating-data-pipelines-with-python-github-actions-c19e2ef9ca90).

•	Investigate outputting the DataFrame as a parquet file rather than as a CSV file in order for the datatypes particularly datetime objects to be preserved. 

