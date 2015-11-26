# tscope
**tscope is a command-line tool for Twitter-data extraction.**

It takes an input of a search query thay can contain phrases, Twitter hashtags and / or Twitter usernames.
It then returns a list of related tweets, hashtags and users.

There is also an option to automatically Tweet a reply to all Tweets that were found.

## Requirements
* **[Node.js](https://nodejs.org/)**
* Due to Twitter's API rate limits, You will need to **[register your own Twitter app](https://apps.twitter.com/)** and obtain keys for `config/auth.json` in step 4 of Setup. On the [Twitter apps page](https://apps.twitter.com), Fill in the **Name**, **Description** and **Website** fields with anything you want (Website does not have to be real). Then, click 'Agree' and Create App.

## Setup
* `git clone https://github.com/adv3nt/tscope.git`
* `cd tscope`
* `npm install`
* Enter the keys from your new Twitter app into `config/auth.json`

### Optional
* Edit `config/queries.json` to include the query(s) you want to search for
* Edit `config/statuses.json` to include Tweet status(es) for use with the `-r` flag

*These steps are optional because they can be instead defined in the command line.*

## Usage

### Output usage information:

	node tscope -h

### Basic usage
Return a list of Tweets based on a search query built from `config/queries.json`

	node tscope

Return a list of Tweets, Hashtags, Usernames, and URL's based on a search query built from `config/queries.json`

	node tscope -H@U

### Custom language query

Only return Tweets in a specific language. It takes an argument in the form of a **2-letter [ISO 639-1 code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)**.

	node tscope -l ar

### Custom sample size

Specify the number of Tweets to analayze data from. *(max 100)*

	node tscope -c 100

### Reply to Tweets

Reply to found Tweets with a random status from `config/statuses.json`

	node tscope -r

Reply to found tweets with a custom status:

	node tscope -r -s "Hello, friend."

### Save output to file

	node tscope > output.log