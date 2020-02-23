from flask import Flask
import requests
import json

app = Flask(__name__)


@app.route('/home')
def tags():

    discovery_repositories = get_discovery_repositories(
        "https://api.github.com/users/dominasasa/repos")

    response = requests.get(
        'https://api.github.com/repos/dominasasa/DiscoveryArduino/git/refs/tags')

    if response.status_code == requests.codes.ok:
        tag_response = json.loads(response.content)

        release = get_release(tag_response)
    else:
        tag_response = "dupa"

    return release


def get_release(tag_response):
    ref = tag_response[0]['ref']
    release = ref.split('release/')[-1]
    return release


if __name__ == '__main__':
    app.run(debug=True)


def get_discovery_repositories(url):
    repositories = []

    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        repo_response = json.loads(response.content)
        for repo in repo_response:
            if repo['name'].startswith('Discovery'):
                name = repo['name']
                author = repo['owner']['login']
                version_list = get_version_list(repo['tags_url'])
                current_version = version_list[-1]

                is_finished = is_project_finished()


def get_version_list(tags_url):
    version_list =[]

    tag_list_response = requests.get(tags_url)

    if tag_list_response.status_code == requests.codes.ok:
        tag_list = json.loads(tag_list_response)
        for version in tag_list:
            version_list.append(get_version(version))
    
    return version_list


class Repository:

    def __init__(self, name, author, version_list, current_version, is_finished, url):
        self.name = name
        self.author = author
        self.version_list = version_list
        self.current_version = current_version
        self.is_finished = is_finished
        self.url = url
