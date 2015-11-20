//install: npm install  twitter/fb-search/node-irc/tumblr

//usage: nodejs script.js keyword

var FacebookSearch = require('facebook-search');

var fb = new FacebookSearch('FB API APP KEY HERE', 'FB API SECRET HERE'); 

var searchFor = {
	type: 	'page',		//need to also add event/group
	q:	process.argv[2],
};

fb.search(searchFor, function(err, res) { console.log(err ? err : res);
	

fb.next(function(err, res) {
    console.log(err ? err : res);
});
});



var tumblr = require('tumblr');

var oauth = {
  consumer_key: '',
  consumer_secret: '',
  token: '',
  token_secret: ''
};


tag = new tumblr.Tagged('tag', oauth);

//tag.search(tag['isis', options], callback) {
//  if (error) {
//    throw new Error(error);

//}
//console.log(response.posts);
//});


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
//	client.say('tweet id:',tweet.id, 'user id:', tweet.user.id, 'tweet: ', tweet.text);
  });

  stream.on('error', function(error) {
    console.log(error);
  });
});



var ircClient = require('node-irc');

var server = 'irc.freenode.net',
    port = 6667,
    myNick = 'opparisbot',
    fullname = 'opparisbot',
    chan = '#oppdev';

// Create client object, pass in constructor arguments
var client = new ircClient(server, port, myNick, fullname);

client.verbosity = 2;

client.on('ready', function () {
  client.join(chan);
});

client.on('PRIVMSG', function (data) {
  if (data.sender === 'kod_') {
    if (data.message.match('^SAY')) {
      var splitMessage = data.message.split(" ");
      var receiver = splitMessage[1] 
      var message = splitMessage.splice(2);
      message = message.join(" ");
      client.say(receiver, message);
    }
    else if (data.message.match('^JOIN')) {
      var channel = data.message.split(" ")[1];
      client.join(channel);
    }
    else if (data.message.match('^PART')) {
      var channel = data.message.split(" ")[1];
      client.part(channel);
    }
    else if (data.message.match('^QUIT')) {
      var message = data.message.split(" ")[1];
      client.quit(message);
    }
    else if (data.message.match('^KICK')) {
      var message = data.message.split(" ");
      var channel = message[1];
      var nick = message[2];
      var reason = message.splice(3).join(" ");
      client.kick(channel, nick, reason);
    }  
    else if (data.message.match('^NICK')) {
      var newNick = data.message.split(" ")[1];
      client.nick(newNick);
    }
    else if (data.message.match('^OP')) {
      var channel = data.message.split(" ")[1];
      var opnick = data.message.split(" ")[2];
      client.mode(channel, '+o', opnick);
    }
    else if (data.message.match('^PRIVATE')) {
      var channel = data.message.split(" ")[1];
      client.mode(channel, '+p');
    }
  }
});

//enable for irc

//client.connect();
