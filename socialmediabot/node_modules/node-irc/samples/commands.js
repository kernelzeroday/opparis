var ircClient = require('node-irc');

var server = 'irc.freenode.net',
    port = 6667,
    myNick = 'lolznick',
    fullname = 'lolzname',
    chan = '#Nuug';

// Create client object, pass in constructor arguments
var client = new ircClient(server, port, myNick, fullname);

client.verbosity = 2;

client.on('ready', function () {
  client.join(chan);
});

client.on('PRIVMSG', function (data) {
  if (data.sender === 'bleakgadfly') {
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

client.connect();
