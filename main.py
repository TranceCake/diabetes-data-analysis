from parser import mgdl_to_mmol
import pandas as pd

from renderer import render_day_graph

# Path to data
file_path = 'data/data.csv'

data = pd.read_csv(file_path, delimiter=';', usecols=['Date', 'Time', 'BG', 'Units', 'Carbs'])
data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format='%d.%m.%Y %H:%M')
data.drop(columns=['Date', 'Time'], inplace=True)


if __name__ == '__main__':
    render_day_graph(data, '2024-12-31')