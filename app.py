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

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        one_day_ago = datetime.now(timezone.utc) - timedelta(hours=8)
        start_time = one_day_ago.isoformat(timespec='milliseconds').replace('+00:00', '') + "Z"
        
        search_results = search_tweets(bearer_token, query, max_results=50, start_time=start_time)
        return search_results
    else:
        return jsonify({
            'status': 'error',
            'message': 'Query parameter "q" is required.'
        }), 400
    
@app.route('/api/summarize', methods=['POST'])
def summarize():
    query = request.json.get('query')
    if query:
        qualities = tweets_qualities(bearer_token, query, sampler)
        while len(qualities) != 3:
            qualities = tweets_qualities(bearer_token, query, sampler)
            return jsonify({
                'status': 'error',
                'message': 'Grok AI is dumb and failed the prompt 3 times. Please try again.'
            }), 400
            
        
        quality_obj = {}
        for quality in summary:
            quality_obj[quality] = quality
        return jsonify(quality_obj)
    else:
        return jsonify({
            'status': 'error',
            'message': 'Query parameter "q" is required.'
        }), 400

# Run the main function when this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
