from flask import Flask
import requests
import json
from flask.json import jsonify
from json import JSONEncoder
from flask.templating import render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/home')
def directories():
    discovery_repositories =[]

    discovery_repositories = get_discovery_repositories('https://api.github.com/users/dominasasa/repos')

    return json.dumps(discovery_repositories)


def get_version_list(tags_url):
    version_list = []

    tag_list_response = requests.get(tags_url)

    if tag_list_response.status_code == requests.codes.ok:
        tag_list = json.loads(tag_list_response.content)
        for version in tag_list:
            version_list.append(get_version(version))
    return version_list

def get_version(version):
    release = version['name'].split('release/')[-1]
    return release


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
                current_version = version_list[-1] if version_list else ""
                is_finished = True if version_list else False
                url = repo['html_url']
                repository = Repository(
                    name, author, version_list, current_version, is_finished, url)
                repositories.append(repository)

    return repositories


class Repository(dict):

    def __init__(self, name, author, version_list, current_version, is_finished, url):
        self.name = name
        self.author = author
        self.version_list = version_list
        self.current_version = current_version
        self.is_finished = is_finished
        self.url = url
        dict.__init__(self, name=name, author=author, version_list=version_list, current_version=current_version, is_finished=is_finished,url=url)


if __name__ == '__main__':
    app.run(debug=True)
