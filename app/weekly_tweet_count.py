import mysql.connector
import requests
import os
import json
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# Load env variables
load_dotenv()

# Connect to database
try:
    my_conn = mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        db=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
    )
except mysql.connector.Error as err:
    logging.error(f"Failed to connect to the database: {err}")
    exit(1)


# Bearer token for access to Twitter API
bearer_token = os.getenv("BEARER_TOKEN")

# Url to search tweets for the past 7 days

search_url = "https://api.twitter.com/2/tweets/counts/recent"

def weekly_update():
    my_cursor = my_conn.cursor()
    my_cursor.execute("SELECT Symbol FROM nasdaq_tickers")
    ticker_list = my_cursor.fetchall()


    def updatecount(start, end):
        for x in range(start, end):
            ticker = ticker_list[x][0]
            query_params = {'query': f'{ticker} lang:en', 'granularity': 'day'}

            def bearer_oauth(r):
                """
                Method required by bearer token authentication.
                """

                r.headers["Authorization"] = f"Bearer {bearer_token}"
                r.headers["User-Agent"] = "v2RecentTweetCountsPython"
                return r

            def connect_to_endpoint(url, params):
                response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
                print(response.status_code)
                if response.status_code != 200:
                    raise Exception(response.status_code, response.text)
                return response.json()

            def main():
                json_response = connect_to_endpoint(search_url, query_params)
                #print(json.dumps(json_response, indent=4, sort_keys=True))
                total_count = int(json.dumps(json_response['meta'].get('total_tweet_count')))
                rs = my_cursor.execute("UPDATE nasdaq_tickers SET count = %s WHERE Symbol = '%s'" % (total_count, ticker))
                print(f"{ticker} count is {total_count}.")
                my_conn.commit()

            if __name__ == "__main__":
                main()

    start = 0
    end = 300

    #Update symbols 300 at a time

    for i in range(round(len(ticker_list) / 300)):
        updatecount(start, end)
        start += 300
        end += 300

        #Get current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        print("15 minute break starting: " + current_time)
        time.sleep(900) #15 minute break based on Twitter API limit of 300 requests per 15 minutes


weekly_update()
