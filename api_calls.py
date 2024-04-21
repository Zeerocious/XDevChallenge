from flask import jsonify
import xai_sdk
import requests
import json

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
def search_tweets(bearer_token, query, max_results=50, start_time=None):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization" : f"Bearer {bearer_token}"
    }
    params = {
        "query": query,
        "max_results": max_results,
        "start_time": start_time
    }
    response =  requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to search tweets")
    
async def tweets_qualities(query):
    client = xai_sdk.Client()
    sampler = client.sampler
    
    FIRST_PREAMBLE = """\
This is a conversation between a human user and a highly intelligent AI. The AI's name is Grok and it makes every effort to truthfully answer a user's questions. It always responds politely but is not shy to use its vast knowledge in order to solve even the most difficult problems. The conversation begins.

Human: I want you to find the three main qualities or focus of these set of tweets.

Please format your answer to ONLY include those qualities separated by commas. For eg. if your qualities are "price, comfort, peaceful" your output should ONLY be. NO YAPPING AT ALL. NOT EVEN NUMBERS OR ANYTHING ELSE. JUST THE QUALITIES SEPARATED BY COMMAS. NO SPACES. NO QUOTES

price,comfort,peaceful
<|separator|>

Assistant: Understood! Please provide the list of tweets as a list of strings."""
    prompt = FIRST_PREAMBLE + f"<|separator|>\n\nHuman: {query}<|separator|>\n\nAssistant: " + "\n"
    print(prompt)
    response = ""
    async for token in sampler.sample(
        prompt=prompt,
        max_len=64,
        stop_tokens=["<|separator|>"],
        temperature=0.5,
        nucleus_p=0.95):
        response = response + token.token_str
    prompt = prompt + response + "\n"
    qualities = response.split(",")
    return qualities, prompt


async def summarize_tweets(prompt):
    client = xai_sdk.Client()
    sampler = client.sampler

    prompt = prompt + """\
Human: Based on the qualities you've given, create three summaries of the same set of tweets on people's sentiments about those qualities.

Please format your answer as a valid JSON. For eg. if your qualities are (price, comfort, peaceful) your output should be.

{
    "info": [
        {
            "quality": "price",
            "summary": "An opinionated summary of the tweets that express the price"
        },
        {
            "quality": "comfort",
            "summary": "A opinionated summary of the tweets that express the comfort"
        },
        {
            "quality": "peaceful",
            "summary": "A opinionated summary of the tweets that express the peaceful"
        }
    ]
}
<|separator|>

Assistant: Understood! Here's the valid JSON and nothing else: \n {\n"""
    print(prompt)
    response = "{\n"
    async for token in sampler.sample(
        prompt=prompt,
        max_len=1024,
        stop_tokens=["<|separator|>"],
        temperature=0.5,
        nucleus_p=0.95):
        response = response + token.token_str
    print(response)
    response_dict = json.loads(response)
    return response_dict
    
    