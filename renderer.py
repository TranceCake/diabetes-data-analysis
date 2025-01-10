import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


# Define color mapping based on BG value
def get_color(bg_value):
    if bg_value < 72:
        return 'orangered'
    elif 72 <= bg_value <= 180:
        return 'green'
    else:
        return 'orange'

def render_day_graph(data, date, use_mmol=False):
    # Filter the DataFrame for the selected day
    day_data = data[data['Datetime'].dt.date == pd.to_datetime(date).date()]

    if not day_data.empty:
        # Apply the color mapping to each BG value in the day_data
        colors = day_data['BG'].apply(get_color)
        if use_mmol:
            day_data['BG'] = day_data['BG'] / 18

        # Plot the data with custom colors
        plt.figure(figsize=(18, 5))
        plt.scatter(day_data['Datetime'], day_data['BG'], c=colors, label='BG Level', marker='o', s=20)

        # Set x-axis grid with finer granularity
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=120))  # Set grid every 10 minutes
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format time as HH:MM

        # Remove margins on the left and right of the plot
        start_of_day = pd.Timestamp(date)
        end_of_day = start_of_day + pd.Timedelta(days=1)
        plt.xlim(start_of_day, end_of_day)

        # Set y-axis grid height based on the use_mmol flag
        if use_mmol:
            plt.gca().yaxis.set_major_locator(plt.MultipleLocator(2))  # 2 mmol/L grid
            plt.ylabel('Blood Glucose (BG) [mmol/L]')
        else:
            plt.gca().yaxis.set_major_locator(plt.MultipleLocator(36))  # 36 mg/dL grid
            plt.ylabel('Blood Glucose (BG) [mg/dL]')

        # Add insulin bolus as blue bars at the bottom
        for i, row in day_data.iterrows():
            if pd.notna(row['Units']):  # Only plot if Units are not NaN
                # Calculate a consistent bar width (e.g., 5 minutes in datetime units)
                bar_width = pd.Timedelta(minutes=5)

                # Add a blue bar at the bottom for the insulin bolus
                plt.bar(row['Datetime'], bottom=-1, width=bar_width.total_seconds() / (24 * 3600),
                        # Convert to days for matplotlib
                        height=row['Units']*6, color='blue', alpha=0.6)

                # Display the insulin amount above the bar
                plt.text(row['Datetime'], -1 + row['Units']*6 + 0.2, f'{row["Units"]}U',
                         ha='center', va='bottom', fontsize=9, color='blue')

            if pd.notna(row['Carbs']):  # Only plot if Carbs are not NaN
                # Calculate a consistent bar width (e.g., 5 minutes in datetime units)
                bar_width = pd.Timedelta(minutes=5)

                # Add a blue bar at the bottom for the insulin bolus
                plt.bar(row['Datetime'], bottom=-1, width=bar_width.total_seconds() / (24 * 3600),
                        # Convert to days for matplotlib
                        height=row['Carbs']*2, color='chocolate', alpha=0.6)

                # Display the insulin amount above the bar
                plt.text(row['Datetime'], -1 + row['Carbs']*2 + 0.2, f'{row["Carbs"]}g',
                         ha='center', va='bottom', fontsize=9, color='chocolate')

        # Add labels, title, and grid
        plt.xlabel('Time')
        plt.ylabel('Blood Glucose (BG)')
        plt.title(f'Blood Glucose Chart of {date}')
        plt.grid(True)
        plt.legend()

        # Display the plot
        plt.show()
    else:
        print(f"No data available for {date}")