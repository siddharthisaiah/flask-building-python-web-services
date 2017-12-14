import requests
import json

TOKEN = "700423df0f32bc9633d5f5fc9dce0b3c86a96bda"
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"


class BitlyHelper:

    def shorten_url(self, long_url):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN, long_url)
            response = requests.get(url).text
            jr = json.loads(response)
            return jr['data']['url']
        except Exception as e:
            print(e)
