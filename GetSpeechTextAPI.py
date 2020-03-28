# Request module must be installed.
# Run pip install requests if necessary.
import requests

subscription_key = '021699b562d646a785d897581437e39b'

def get_token(subscription_key):
    fetch_token_url = 'https://southeastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    print(access_token)
