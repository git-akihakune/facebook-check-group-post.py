import os
import json
import requests
from typing import Dict, List

homeDir = os.path.expanduser('~')
ROOT_DATA_DIR = os.path.join(homeDir, '.fbgr')


def _takeArguments() -> Dict[str, str]:
    from os.path import join, isfile
    import configparser
    config = configparser.ConfigParser()
    configFile = join(ROOT_DATA_DIR, 'config.ini')

    if isfile(configFile):
        config.read(configFile)
        if config['CONFIG']['groupId'] != 'default':
            return config['CONFIG']
        else:
            print(f"Maybe you'll want to modify the values at '{configFile}'?")

    # if there's no config file, or the config was left to
    # default, prompt user for input
    limit = input("Number of retrieving posts: ") or ""
    groupId = input("Group ID: ")
    accessToken = input("Access token: ") or ""
    configVal = {
        "groupId": groupId,
        "limit": limit,
        "access_token": accessToken
    }
    return configVal


def _createConfig() -> None:
    # Check if the data directory has already existed,
    # create one if it wasn't
    if os.path.isdir(ROOT_DATA_DIR):
        return None
    os.mkdir(ROOT_DATA_DIR)

    import configparser
    config = configparser.ConfigParser()
    config['CONFIG'] = {
        "groupId": 'default',
        "limit": '',
        "access_token": 'default'
    }
    configFile = os.path.join(ROOT_DATA_DIR, 'config.ini')
    with open(configFile, 'w') as cfg:
        config.write(cfg)


def writeLogs(data: List[Dict]):
    with open(os.path.join(ROOT_DATA_DIR, 'log.json'), 'w') as f:
        json.dump(data, f)
    print("Previous log file overwritten")


def checkNewPost(data: List[Dict]) -> List[Dict]:
    # make sure previous logs exist
    if not os.path.isfile(os.path.join(ROOT_DATA_DIR, 'log.json')) or \
            os.stat(os.path.join(ROOT_DATA_DIR, 'log.json')).st_size == 0:
        writeLogs(data)
        return data
    with open(os.path.join(ROOT_DATA_DIR, 'log.json'), 'r') as logFile:
        previousData = json.load(logFile)

    from datetime import datetime as dt

    latestRecord = previousData[0]['updated_time']
    latestRecord = dt.strptime(latestRecord, "%Y-%m-%dT%H:%M:%S+%f")

    newPosts = []
    for post in range(len(previousData)):
        uploadDate = data[post]['updated_time']

        # convert to comparable datetime type
        uploadDate = dt.strptime(uploadDate, "%Y-%m-%dT%H:%M:%S+%f")

        # if the post is not newer than the latest recorded post
        if uploadDate <= latestRecord:
            break
        newPosts.append(data[post])

    # update the log file to newest posts
    if len(newPosts) > 0:
        writeLogs(newPosts)

    return newPosts


def main():
    config = _takeArguments()
    groupId = config['groupId']
    limit = config['limit']
    accessToken = config['access_token']

    params = {
        "limit": limit,
        "access_token": accessToken
    }
    response = requests.get(
        f"https://graph.facebook.com/{groupId}/feed", params=params)

    # Stop the program if there's error
    if "error" in response.json():
        print(json.dumps(response.json(), indent=4))
        return 1

    returnedData = response.json()['data']
    newPosts = checkNewPost(returnedData)
    if len(newPosts) == 0:
        print("There's no new post. Have a nice day!")
    else:
        print(json.dumps(newPosts, indent=4))


if __name__ == '__main__':
    _createConfig()
    main()
