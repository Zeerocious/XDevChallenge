
import configparser
import requests
import base64
from flask import Flask, jsonify, request
from flask_cors import CORS

# Read Twitter API credentials from a config file and Initialize Tweepy
def init():
    config = configparser.ConfigParser()
    config.read("config.ini")

    api_key = config.get("TwitterCredentials", "API_KEY")
    api_secret_key = config.get("TwitterCredentials", "API_SECRET_KEY")
    access_token = config.get("TwitterCredentials", "ACCESS_TOKEN")
    access_token_secret = config.get("TwitterCredentials", "ACCESS_TOKEN_SECRET")
    
    auth_url = "https://api.twitter.com/oauth2/token"
    key_secret = f"{api_key}:{api_secret_key}".encode("ascii")
    b64_encoded_key = base64.b64encode(key_secret)
    
    headers = {
        "Authorization": f"Basic {b64_encoded_key.decode('ascii')}",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    
    data = {
        "grant_type": "client_credentials"
    }
    
    response = requests.post(auth_url, headers=headers, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        raise Exception("Failed to get bearer token")

# Search tweets based on parameters
def trend_tweets(woeid, bearer_token):
    trend_url = f"https://api.twitter.com/2/trends/by/woeid/{woeid}"
    headers = {
        "Authorization" : f"Bearer {bearer_token}"
    }
    response =  requests.get(trend_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to search tweets")
    
# Search tweets based on parameters
def search_tweets(bearer_token, query, max_results=10, start_time=None):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization" : f"Bearer {bearer_token}"
    }
    params = {
        "query": params,
        "max_results": 10
    }
    response =  requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        return jsonify(response)
    else:
        raise Exception("Failed to search tweets")

# def main():
#     # Load Twitter API credentials. Return the Bearer_token
#     bearer_token= init()
    
#     # Fetch trending tweets
#     trends = trend_tweets(26062, bearer_token)

#     # Display fetched tweets
#     for trend in trends["data"]:
#         trend_name = trend["trend_name"]
#         tweet_count = trend["tweet_count"] if "tweet_count" in trend else 0
#         print(f"Trend: {trend_name} | Tweet Count: {tweet_count}\n")


bearer_token= init()

app = Flask(__name__)
CORS(app)

@app.route('/', method = ['GET'])
def welcome():
    return 'Welcome to Twitter API!'

@app.route('/api/trends', methods=['GET'])
def trends():
    query = request.args.get('query')
    if query:
        
        trends = trend_tweets(query, bearer_token)
        return trends
    else:
        return jsonify({
            'status': 'error',
            'message': 'Query parameter "q" is required.'
        }), 400  # HTTP status code 400 (Bad Request)

    
# Run the main function when this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
