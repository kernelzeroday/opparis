# tscope

## Warning
DO NOT use your personal information/Twitter account with this program.

## Requirements
* `Node.js`

## Setup
* clone and `cd` into repo
* `npm install`
* `cd ./config`
* You will need to create a new Twitter app at [dev.twitter.com](https://dev.twitter.com/) to obtain the keys to input to `auth.json` in the next step
* Edit `auth.json` by filling in the keys from your new Twitter app
* Edit `config/hashtags.json` to include the hashtag(s) you want to search for
* Edit `config/stasuses.json` to include the status(es) you want to reply with

## Usage
`node tscope`