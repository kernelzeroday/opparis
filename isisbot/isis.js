//install: npm install -g twitter

//usage: nodejs script.js keyword

var FB = require('fb');


FB.api('oauth/access_token', {
    client_id: 'app_id',
    client_secret: 'app_secret',
    grant_type: 'client_credentials'
}, function (res) {
    if(!res || res.error) {
        console.log(!res ? 'error occurred' : res.error);
        return;
    }

    var accessToken = res.access_token;
});

var FB = require('fb');

FB.api('4', { fields: ['id', 'name'] }, function (res) {
  if(!res || res.error) {
    console.log(!res ? 'error occurred' : res.error);
    return;
  }
  console.log(res.id);
  console.log(res.name);
});



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
