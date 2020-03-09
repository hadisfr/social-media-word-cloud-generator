# [Social Media Word Cloud Generator](https://github.com/hadisfr/social-media-word-cloud-generator)

a series of scripts to generate word cloud from social media posts 

---

## Usage

* you may need to use `git submodule update --init --recursive` to download submodules

### Telegram

* (optional) create a python3 virtual environment
* install requirements mentioned in [_requirements.txt_](requirements.txt)
* export a chat to a place such as _extracted-chats-folder_
* run script as: `python3 -m tlgr extracted-chats-folder res.png` to generate _res.png_

### Twitter

* (optional) create a python3 virtual environment
* install requirements mentioned in [_requirements.txt_](requirements.txt) and [twint](https://github.com/twintproject/twint)
* export a chat to a place such as _tweets.json_ with ```twint -u <username> -o tweets.json --json --filter-retweets```
* run script as: `python3 -m twtr tweets.json res.png` to generate _res.png_
