node-irc
=============

node-irc is a socket wrapper for the IRC protocol that extends EventEmitter. node-irc aims to be an efficient, extremely easy to use IRC library used to build bots and clients.

Get started
-------------

### Install node-irc with npm.

```
npm install node-irc
```

### Import node-irc.


```
var ircClient = require('node-irc');
```

### Pass in the server, port, nickname and fullname as parameters to the constructor.

```
var client = new ircClient('irc.freenode.net', 6667,
```

### Add an event handler for what to do When the server is ready, like joining a channel and say something weird.

```
client.on('ready', function () {
  client.join('#Node.js');
  client.say('#Node.js', 'I see node people fart.');
});
```

### Connect to the server

```
client.connect()
```
