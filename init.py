import configparser
import base64
import requests

# Read Twitter API credentials from a config file and return a bearer token
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
