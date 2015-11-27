
// Search for a user's tweets and display geolocation data

// Usage: node script.js screen_name

// DEPS: npm install twitter

var Twitter = require('twitter');
//https://apps.twitter.com/app/new for your api keys
var client = new Twitter({
  consumer_key: 'oygfO2el6S3pKD8sLZClLWc6H',
  consumer_secret: 'IL2dp5pZdAmG6CGuBCNqTCx1jBUZBYLX4xTsSzbO8G9ukQWjKY',
  access_token_key: '48372745-msod0g54kqxhjgAjU00dAlyFkq9fYD8skgqU7C0Vo',
  access_token_secret: 'xTs5FMhvwB6JC9udHDzteYElknMn0DBbN3aNjV8RSCFSB'
});

client.get('statuses/user_timeline', {screen_name: process.argv[2]}, function(error, tweets, response){
        for (var i = 0; i < tweets.length; i++) {
                var tweet = tweets[i];
                console.log('tweet id:',tweet.id, 'user id:', tweet.user.id, 'tweet: ', tweet.text, 'geo: ', tweet.geo, 'user.location: ', tweet.user.location, 'coordinates: ', tweet.coordinates  );
        }
});