from flask import Flask, jsonify, request
from flask_cors import CORS
from init import init
from api_calls import trend_tweets, search_tweets, summarize_tweets, tweets_qualities
from datetime import datetime, timedelta, timezone
import xai_sdk
import asyncio

bearer_token= init()

app = Flask(__name__)
CORS(app)
client = xai_sdk.Client()
sampler = client.sampler

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

@app.route('/api/sentiments', methods=['GET'])
def sentiments():
    query = request.args.get('query')
    if query:
        # Get tweets from the past 24 hours
        one_day_ago = datetime.now(timezone.utc) - timedelta(hours=8)
        start_time = one_day_ago.isoformat(timespec='milliseconds').replace('+00:00', '') + "Z"
        
        # Call the search_tweets function to get tweets and put them in a list
        search_results = search_tweets(bearer_token, query, max_results=10, start_time=start_time)
        tweets = []
        for tweet in search_results["data"]:
            tweets.append(tweet["text"])
        
        qualities, prompt = asyncio.run(tweets_qualities(tweets))
        print(qualities)
        tries = 0
        while len(qualities) != 3:
            if tries == 3:
                return jsonify({
                    'status': 'error',
                    'message': 'Grok AI is dumb and failed the quality prompt 3 times. Please try again.'
                }), 400
            qualities, prompt = asyncio.run(tweets_qualities(tweets))
            tries += 1
        tries = 0
        while True and tries < 3:
            try:
                summary_obj = asyncio.run(summarize_tweets(prompt))
                break
            except:
                tries +=1
        if tries == 3:
            return jsonify({
                'status': 'error',
                'message': 'Grok AI is dumb and failed the summary prompt 3 times. Please try again.'
            }), 400
        return summary_obj
        
    else:
        return jsonify({
            'status': 'error',
            'message': 'Query parameter "q" is required.'
        }), 400
    
# Run the main function when this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
