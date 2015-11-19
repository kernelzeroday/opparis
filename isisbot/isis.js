//install: npm install -g twitter

//usage: nodejs script.js keyword

var tumblr = require('tumblr');

var oauth = {
  consumer_key: '',
  consumer_secret: '',
  token: '',
  token_secret: ''
};


tag = new tumblr.Tagged('tag', oauth);

tag.search(tag[, options], callback) {
  if (error) {
    throw new Error(error);

}
console.log(response.posts);
});


var Twitter = require('twitter');
//https://apps.twitter.com/app/new for your api keys 
var client = new Twitter({
  consumer_key: '',
  consumer_secret: '',
  access_token_key: '',
  access_token_secret: ''
});

client.stream('statuses/filter', {track: process.argv[2]}, function(stream){
  stream.on('data', function(tweet) {
//	if you want full json
//   	console.log(tweet.text);
        console.log('tweet id:',tweet.id, 'user id:', tweet.user.id, 'tweet: ', tweet.text);
	console.log();
  });

  stream.on('error', function(error) {
    console.log(error);
  });
});
