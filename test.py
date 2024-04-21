from init import init
import asyncio
from api_calls import summarize_tweets, trend_tweets, search_tweets, tweets_qualities
from datetime import datetime, timedelta, timezone

bearer_token= init()

# trends = trend_tweets(2487956, bearer_token)
# print(trends)

# {
#     'data': [
#         {'trend_name': 'Victorville'}, 
#         {'trend_name': '#LAFC'}, 
#         {'trend_name': '#LakeShow', 'tweet_count': 5375}, 
#         {'trend_name': 'Gabe Vincent', 'tweet_count': 1528}, 
#         {'trend_name': 'Taurean Prince', 'tweet_count': 1497}, 
#         {'trend_name': 'Hayes', 'tweet_count': 23338}, 
#         {'trend_name': '#TakesEverybody', 'tweet_count': 1214}, 
#         {'trend_name': '#AEWCollision', 'tweet_count': 16584}, 
#     ]
# }

one_day_ago = datetime.now(timezone.utc) - timedelta(hours=8)
start_time = one_day_ago.isoformat(timespec='milliseconds').replace('+00:00', '') + "Z"

search_results = search_tweets(bearer_token, "#TakesEverybody", max_results=10, start_time=start_time)
tweets = []
for tweet in search_results["data"]:
    tweets.append(tweet["text"])
    
qualities, prompt = asyncio.run(tweets_qualities(tweets))

asyncio.run(summarize_tweets(prompt))
