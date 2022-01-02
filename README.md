# check-new-post.py
Automatically check for new Facebook group post, without the need of opening browser.

## Why?
Because Facebook is so distracting, a countermeasure is needed. This script can also be used in cronjob to periodically check for new posts.

## Demo

![demo](https://user-images.githubusercontent.com/87116762/147879353-a018d87f-fa5f-48d9-b004-d20780e6823f.gif)

## Installation
```bash
https://raw.githubusercontent.com/git-akihakune/facebook-check-group-post.py/main/check-new-post.py
```

Get you Facebook access token at [Graph API Explorer page](https://developers.facebook.com/tools/explorer). The group ID can be found in the group URL.

## Usage
```python
python3 check-new-post.py
```

You may also want to edit the config file at `~/.fbgr/config.ini` to avoid being prompted repeatedly.


## Development
This is one of on-the-whim scripts that I think would be useful. If you want to develop on it, please create a fork.
