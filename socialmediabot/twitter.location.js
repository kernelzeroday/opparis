var Twitter = require('twitter');
//https://apps.twitter.com/app/new for your api keys 
var client = new Twitter({
  consumer_key: '',
  consumer_secret: '',
  access_token_key: '',
  access_token_secret: ''
});

client.get('statuses/user_timeline', {screen_name: process.argv[2]}, function(error, tweets, response){
  stream.on('data', function(tweet) {
//      if you want full json
//      console.log(tweet.text);
        console.log('tweet id:',tweet.id, 'user id:', tweet.user.id, 'tweet: ', tweet.text, tweet.geo, tweet.user.location, tweet.coordinates  );
        console.log();
//      client.say('tweet id:',tweet.id, 'user id:', tweet.user.id, 'tweet: ', tweet.text);
  });

  stream.on('error', function(error) {
    console.log(error);
  });
});


