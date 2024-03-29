<h1>Trending Plays: Weekly Tweet Count</h1>

This script uses the Twitter API and MySQL to collect tweets for a given list of tickers and updates their counts in a MySQL database.

Currently utilizing script to display the top ten trending tickers each week on the <a href="www.trendingplays.com">Trending Plays</a> website. Repository can be found <a href="https://github.com/karenastevens/trendingplays_">here</a>.

<h2>Requirements:</h2>
<ul>
    <li>python3</li>
    <li>mysql.connector</li>
    <li>requests</li>
    <li>os</li>
    <li>json</li>
    <li>time</li>
    <li>logging</li>
    <li>datetime</li>
    <li>dotenv</li>
</ul>

<h2>Usage:</h2>

Clone this repository

Create a .env file in the root directory and add the following environment variables:

    DB_USER: your MySQL username
    DB_PASS: your MySQL password
    DB_NAME: the name of the database you want to connect to
    DB_HOST: the hostname or IP address of your MySQL server
    BEARER_TOKEN: your Twitter API bearer token

Run python3 weekly_tweet_count.py

<h2>Functionality:</h2>

The script connects to a MySQL database and queries a table called `nasdaq_tickers` for a list of symbols. It then uses the Twitter API to search for tweets containing each ticker symbol and the language set to English. The number of tweets for each ticker is then updated in the `nasdaq_tickers` table. The script updates 300 tickers at a time, with a 15-minute break in between each batch to comply with Twitter API rate limits.

<h2>Note:</h2>

Please check the <a href="https://developer.twitter.com/en/docs/twitter-api">Twitter API's TOS</a> and make sure that the usage of the API does not violate any of the terms of service.
