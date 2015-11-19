var ircClient = require('./client.js');

var server = 'irc.freenode.net',
    port = 6667,
    nick = 'lolznick',
    fullname = 'lolzname',
    chan = '#Nuug';

// Create client object, pass in constructor arguments
var client = new ircClient(server, port, nick, fullname);

// This decides the verbosity of the output, set to 1 as default
client.verbosity = 2; // 0 == Silent, 1 == Normal, 2 == Info

// This is set to false by defaults, prints out all raw server messages
client.debug = false;

// Key piece.
client.on('ready', function () {
  client.join(chan);
});

/**                                      \** 
  *                                        *
  * THESE ARE THE AVAILABLE EVENT TRIGGERS *
  *                                        *
  **\                                    **/

client.on('CHANMSG', function (data) {
  /** 
      The data object contains
      data.receiver : The channel the message was written in prefixed with hash (#) 
      data.sender   : The nick of the person who sent the message
      data.message  : The message the person sent
  **/
  var message = data.sender + ' said: ' + data.message;
  if(data.sender !== nick) client.say(data.receiver, message); 
});

client.on('PRIVMSG', function (data) {
  /**
      The data object contains:
      data.receiver : The nick person who received the message (this should always be you)
      data.sender   : The nick of the person who sent you the message 
      data.message  : The message the person sent 
  **/
  var message = 'Hi, ' + data.sender +
                ', nice of you to speak to a bot. I can only repeat what you said: ' + data.message;
  if(data.sender !== nick) client.say(data.sender, message);
});

client.on('JOIN', function (data) {
  /** 
      The data object contains:
      data.receiver : The channel the person joined, prefixed by a hash (#)
      data.sender   : The nick of the person who joined 
  **/
  var message = 'Welcome to ' + data.receiver + ', ' + data.sender;
  if(data.sender !== nick) client.say(data.receiver, message);
});

client.on('INVITE', function (data) {
  /** 
      The data object contains:
      data.receiver : The nick of the person who was invited (this should always be you)
      data.sender   : The nick of the person who invited you
      data.message  : The channel you were invited to, prefixed by a hash (#)
  **/
  var message = 'Thank you for your invite to ' + data.message + ', ' + data.sender;
  client.join(data.message);
  client.say(data.message, message);
});

client.on('TOPIC', function (data) {
  /** 
      The data object contains:
      data.receiver : The channel the topic was changed on, prefixed by a hash (#)
      data.sender   : The nick of the person who changed the topic
      data.message  : The new topic message
  **/
  var message = 'Hmm, seems like ' + data.sender + 
                ' changed the topic of ' + data.receiver + ' to: ' + data.message;
  client.say(data.receiver, message);
});

client.on('PART', function (data) {
  /**
      The data object contains:
      data.receiver : The channel the person parted from, prefixed by a hash (#)
      data.sender   : The nick of the person who parted
  **/
  var privMessage = 'Sorry to see you leave from ' + data.receiver + 
                    ', ' + data.sender + '. Hope to see you again soon!';
  var chanMessage = 'Hmm, seems like ' + data.sender + ' left us';
  client.say(data.receiver, chanMessage);
  client.say(data.sender, privMessage);
});

client.on('KICK', function (data) {
  /** 
      The data object contains:
      data.receiver   : The channel the person got kicked out of, prefixed by a hash (#)
      data.sender     : The nick of the person who kicked out the other person
      data.message[0] : The nick of the person who got kicked out
      data.message[1] : The optional kick message, will default to the nick of the kicked user
  **/
  var privMessage = 'Im sory but you seem to be some kind of an douche, ' + data.message[0] + 
                ', or else you wouldnt have been kicked by ' + data.sender + 
                ' on ' + data.receiver + ' because of ' + data.message[1];
  var chanMessage = 'Sorry guys, but ' + data.message[0] + ' had to go!';
  client.say(data.message[0], privMessage);
  client.say(data.receiver, chanMessage);
});

client.on('QUIT', function (data) {
  /**
      The data object contains:
      data.sender  : The nick of the person who quitted 
      data.message : The quit message (usually deactivated on servers because of spam) 
  **/
  var message = data.sender + ' has left the building!';
  client.say(chan, message);
});

client.on('NICK', function (data) {
  /** 
      The data object contains:
      data.receiver : The new nick of the person
      data.sender   : The old nick of the person
  **/
  var message = data.sender + ' changed his nick to ' + data.receiver + '! We got a badass in here ;-)';
  client.say(chan, message);
});

client.connect();
