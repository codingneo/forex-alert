import streamlit as st
import requests
import schedule
from datetime import datetime, timedelta
import time
import json
from threading import Thread

from utils import is_hammer, is_shooting_star



# The webhook URL that you copied from your Discord server
webhook_url = 'https://discord.com/api/webhooks/1173258822341640193/jgT1nrH3d9xo6-7Sc3H38-oEU25MblHMtjxd1-f-FvL6s6HMiR8gS3QVUy-Ohjk_axyK'


# OANDA API information
api_key = "c89d4d36bf19bd1c810ca3a59797d78b-c33df693c4f8ba9d0beb3d8a4e431192"  # Replace with your actual OANDA API key
account_id = "101-003-27403441-001"  # Replace with your OANDA account ID
url = f"https://api-fxpractice.oanda.com/v3/accounts/{account_id}/instruments/USD_MXN/candles?price=M&granularity=H4&count=2"

forex_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

alert_support = None  # Global variable to hold the alert value
alert_resistance = None

def check_price():
    # global alert_support, alert_resistance
    response = requests.get(url, headers=forex_headers)
    
    if response.status_code == 200:
        data = response.json()
        latest_open = data['candles'][-2]['mid']['o']  # The open price of the last complete candle
        latest_high = data['candles'][-2]['mid']['h']  # The highest price of the last complete candle
        latest_low = data['candles'][-2]['mid']['l']  # The lowest price of the last complete candle
        latest_close = data['candles'][-2]['mid']['c']  # The close price of the last complete candle

        is_hammer_flag = is_hammer(float(latest_open), float(latest_high), float(latest_low), float(latest_close))
        is_shooting_star_flag = is_shooting_star(float(latest_open), float(latest_high), float(latest_low), float(latest_close))

        if (float(latest_low)<=alert_support*1.05) and (is_hammer_flag):
            st.warning(f"Alert: USD/MXN has reached the specified value of {alert_support}")
            # Here you can add code to send an actual alert, like an email or a notification

            # The message that you want to send
            message = 'Hello, USD/MXN reach support area and has a hammer pattern'

            # The username and avatar URL are optional, but they can customize the appearance of the webhook message
            # username = 'My Python Bot'
            # avatar_url = 'URL_TO_AVATAR_IMAGE'

            # Create the payload to send to the webhook
            data = {
                'content': message,
                # 'username': username,
                # 'avatar_url': avatar_url
            }

            # Set the headers, including the content type
            headers = {
                'Content-Type': 'application/json'
            }

            # Post the message using the requests library
            response = requests.post(webhook_url, json=data, headers=headers)

            # Check the response
            if response.status_code == 204:
                print('Message sent successfully.')
            else:
                print('Failed to send message. Response:', response.content)
                            
    if (float(latest_high)>=alert_resistance*0.95) and (is_shooting_star_flag):
            st.warning(f"Alert: USD/MXN has reached the resistance area: {alert_resistance}")
            # Here you can add code to send an actual alert, like an email or a notification

            # The message that you want to send
            message = 'Hello, USD/MXN reach resistance area and has a shooting star pattern'

            # The username and avatar URL are optional, but they can customize the appearance of the webhook message
            # username = 'My Python Bot'
            # avatar_url = 'URL_TO_AVATAR_IMAGE'

            # Create the payload to send to the webhook
            data = {
                'content': message,
                # 'username': username,
                # 'avatar_url': avatar_url
            }

            # Set the headers, including the content type
            headers = {
                'Content-Type': 'application/json'
            }

            # Post the message using the requests library
            response = requests.post(webhook_url, json=data, headers=headers)

            # Check the response
            if response.status_code == 204:
                print('Message sent successfully.')
            else:
                print('Failed to send message. Response:', response.content)
                        
    else:
        print("Failed to retrieve data")

# Calculate the delay until the next 4-hour mark starting from a specific time
def run_at_specific_time(hour_to_start):
    now = datetime.now()
    next_run = now.replace(hour=hour_to_start, minute=0, second=0, microsecond=0)
    
    # If the next run time is in the past, add 4 hours to it until it's in the future
    while next_run < now:
        next_run += timedelta(hours=4)
    
    delay = (next_run - now).total_seconds()
    return delay

def run_scheduler():

    # Initialize the first run delay
    first_run_delay = run_at_specific_time(2)  # Starts running at 08:00 AM

    # Run the job for the first time after the delay
    schedule.enter(first_run_delay, 1, job)

    # Run the check_price function every 4 hours
    schedule.every(4).hours.do(check_price)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Streamlit app to set the alert value
st.title('USD/MXN Price Alert System')

input_support = st.number_input('Set support value for USD/MXN:', format="%.4f")  # You can change the default value
input_resistance = st.number_input('Set resistance value for USD/MXN:', format="%.4f")  # You can change the default value

if st.button('Set Alert'):
    alert_support = float(input_support)
    alert_resistance = float(input_resistance)
    st.success(f"Alert set for USD/MXN at {alert_support}, {alert_resistance}")

# Start the scheduler thread
Thread(target=run_scheduler).start()
