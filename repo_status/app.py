from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route('/home')
def tags():
    response = requests.get('https://api.github.com/repos/dominasasa/DiscoveryArduino/git/refs/tags')

    if response.status_code == requests.codes.ok:
        tag_response = json.loads(response.content)
        release = get_release(tag_response)
    else:
        tag_response = "dupa"

    return release

def get_release(tag_response):
    ref = tag_response[0]['ref']
    release = ref.split('refs/tags/release/')[-1]
    return release


if __name__ == '__main__':
   app.run(debug=True)