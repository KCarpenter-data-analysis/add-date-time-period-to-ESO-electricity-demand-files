import pandas as pd
import numpy as np
import datetime
from dateutil.rrule import rrule, WEEKLY
from dateutil.rrule import SU as Sunday
import calendar
import pyarrow as pa
import pyarrow.parquet as pq



def leap_year(df, date):
    """Given df and date creates col with start time of settlment period and time zone info
    and col with periodindex of settlement periods. number of rows differ if a leap year."""
    yearly_half_hours = 17520
    if calendar.isleap(date.year):
        yearly_half_hours = 17568
    df['period_start'] = pd.date_range(start=date, periods=yearly_half_hours, freq='30min', tz='Europe/London')
    df['period'] = pd.period_range(date, periods=yearly_half_hours, freq='30min')
    return df


def get_last_sunday(year, month): # function slightly adapted from stack overflow answer 
    """Obtain last Sunday of any month in any particular year."""
    date = datetime.date(year=year, month=month, day=1)
    days = rrule(freq=WEEKLY, dtstart=date, byweekday=Sunday, count=5)
    if days[-1].month == month:
        return days[-1]
    else:
        return days[-2]
    


def get_march_switch(year):  # function slightly adapted from stack overflow answer 
    """Find last day in March for a particular year to find out which
    day clocks go forward in UK for BST."""
    day = get_last_sunday(year, 3)
    return day



def get_october_switch(year):  # function slightly adapted from stack overflow answer 
    """Find last day in October for a particular year to find out which
    day clocks go back in UK."""
    day = get_last_sunday(year, 10)
    return day




def long_short_day(df, short_day, long_day):
    """"Given a df, string of the day clocks go forwards and string of day clock goes back
     amends 'period' column in df to reflect time with clocks changing."""
    short_day_idx = df.index[(df['SETTLEMENT_DATE'] == short_day) & (df['SETTLEMENT_PERIOD'] == 3)].tolist()
    long_day_idx = df.index[(df['SETTLEMENT_DATE'] == long_day) & (df['SETTLEMENT_PERIOD'] == 5)].tolist()
    
    df.loc[short_day_idx[0]:(long_day_idx[0] +1), 'period'] = df.loc[short_day_idx[0]:(long_day_idx[0] +1), 'period'].shift(periods=-2,axis=0)
    df.loc[long_day_idx[0], 'period'] = df.loc[(long_day_idx[0]-2), 'period']
    df.loc[long_day_idx[0] + 1, 'period'] = df.loc[(long_day_idx[0]-1), 'period']
    return df



def add_datetime_periodindex(file_path):
   """Reads a csv file using the file_path into a df called demand_df. Adds a column with a periodindex object
   corresponding to the date and settlement period and a column called period_start with the start date and time
   of each settlement period as a datetime object with UK timezone info. Returns altered df.pip install pyarrow"""
   demand_df = pd.read_csv(file_path)
   demand_df['SETTLEMENT_DATE'] = pd.to_datetime(demand_df['SETTLEMENT_DATE'], format = 'mixed')
   day = demand_df.iloc[1,0] #Get first day of the year from df
   demand_df = leap_year(demand_df, day)
   clock_forward_day = get_march_switch(day.year)
   clock_back_day = get_october_switch(day.year)
   demand_df= long_short_day(demand_df, clock_forward_day, clock_back_day)
   return demand_df


data_file = 'demand_data_2023.csv'

elec_df = add_datetime_periodindex(data_file)

save_filepath = 'elec_demand_2023.parquet'

elec_df.to_parquet(save_filepath, engine="pyarrow")

