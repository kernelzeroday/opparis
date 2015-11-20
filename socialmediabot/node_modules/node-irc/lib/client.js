(function () {
    var events = require('events');

    function ircClient(server, port, nickname, fullname) {
        this.host = server;
        this.port = port;
        this.nickname = nickname;
        this.fullname = fullname;
        this.verbosity = 1; // 0 => Silent, 1 => Normal, 2 => Info, 3 => Debug
        this.debug = false;
        events.EventEmitter.call(this);
        return this;
    }

    ircClient.super_ = events.EventEmitter;
    ircClient.prototype = Object.create(events.EventEmitter.prototype);

    ircClient.prototype.connect = function () {
        var that = this,
            net = require('net'),
            client = net.createConnection(that.port, that.host);

        client.addListener('connect', function () {
            client.write('NICK ' + that.nickname + '\r\n');
            client.write('USER ' + that.nickname + ' 0 * :' + that.fullname + '\r\n');
            that.logger('Client connected', 1);
        });

        client.addListener('data', function (data) {
            if (this.debug) console.log(data.toString());
            that.dispatcher(data.toString());
        });

        client.addListener('close', function (data) {
            that.logger('Disconnected from server', 1);
        });
 
        this.client = client;
    };

    // FORMALITY HANDLERS

    ircClient.prototype.dispatcher = function (data) {
        var response = data.split('\n'),
            formatResponse,
            preparedResponse,
            sortedResponse,
            i;

        if (data.match('^PING')) {
            this.pingHandler(data);
        } else {
            for (i = response.length; i--;) {
                rawResponse = response[i].split(" ");
                if(rawResponse[1] === '376') { // If MOTD has been written
                    this.emit('ready');
                } else { 
                    this.eventHandler(assembleResponse(rawResponse));
                }
            }
        }
    };

    ircClient.prototype.eventHandler = function (data) {
        if (data.method === 'PRIVMSG') {
            data.message = data.message.join(" ");
            data.message = data.message.substring(1, (data.message.length-1));
                if (data.receiver.match(/^#/)) {
                    data.method = 'CHANMSG';
    	              this.emit('CHANMSG', data);
                } else {
    	              this.emit('PRIVMSG', data); 
                }
        }
        else if (data.method === 'JOIN') {
            // Remove preceding semi-colon
            data.receiver = data.receiver.substring(0, (data.receiver.length-1));
            this.emit('JOIN', data);
        }
        else if (data.method === 'INVITE') {
            data.message = data.message[0].substring(1, (data.message[0].length-1));
            this.emit('INVITE', data);
        }
        else if (data.method === 'TOPIC') {
            data.message = data.message.join(" ");
            data.message = data.message.substring(1, (data.message.length-1));
            this.emit('TOPIC', data);
        }
        else if (data.method === 'PART') {
            data.receiver = data.receiver.substring(0, (data.receiver.length-1));
            this.emit('PART', data);
        }
        else if (data.method === 'KICK') {
            data.message[1] = data.message.splice(1);
            data.message[1] = data.message[1].join(" ");
            data.message[1] = data.message[1].substring(1, (data.message[1].length-1));
            this.emit('KICK', data);
        }
        else if (data.method === 'QUIT') {
            data.receiver = '';
            this.emit('QUIT', data);
        }
        else if (data.method === 'NICK') {
            data.receiver = data.receiver.substring(1, (data.receiver.length-1));
            this.emit('NICK', data);
        }
    };
 
    ircClient.prototype.pingHandler = function (response) {
        var splitResponse = [];
        splitResponse = response.split(" ");
        this.logger('PING ' + splitResponse[1], 2);  
        this.logger('PONG ' + splitResponse[1], 2);
        this.client.write('PONG ' + splitResponse[1] + '\r\n');
    };

    ircClient.prototype.logger = function (message, level) {
        if ((this.verbosity !== 0) && (this.verbosity >= level)) {
            console.log('Level ' + level + ': ' + message);
        }
    };

    // USER COMMANDS

    ircClient.prototype.join = function (channel) {
        this.logger('JOIN ' + channel, 1);
        this.client.write('JOIN ' + channel + '\r\n');   
    };

    ircClient.prototype.quit = function (message) {
        this.logger('QUIT :' + message, 2);
        this.client.write('QUIT :Quit: ' + message + '\r\n');
    };

    ircClient.prototype.part = function (channel) {
        this.logger('PART ' + channel, 2);
        this.client.write('PART ' + channel + '\r\n');
    };

    ircClient.prototype.say = function (receiver, message) {
        this.logger('PRIVMSG ' + receiver + ' ' + message, 2);
        this.client.write('PRIVMSG ' + receiver + ' :' + message + '\r\n');
    };
    ircClient.prototype.nick = function (newNick) {
        this.logger('NICK ' + newNick, 2);
        this.client.write('NICK ' + newNick + '\r\n');
    };
    ircClient.prototype.mode = function (channel, mode, nick) {
        this.logger('MODE ' + channel + ' ' + mode + ' ' + nick, 2);
        this.client.write('MODE ' + channel + ' ' + mode + ' ' + nick + '\r\n');
    };
    ircClient.prototype.kick = function (channel, nick, reason) {
        this.logger('KICK ' + channel + ' ' + nick + ' :' + reason, 2);
        this.client.write('KICK ' + channel + ' ' + nick + ' :' + reason + '\r\n');
    };

    // TOOLBOX
    function trim (string) {
      string = string.replace(/(^\s*)|(\s*$)/gi,"");
      string = string.replace(/[ ]{2,}/gi," ");
      string = string.replace(/\n /,"\n");
      return string;
    }
    
    function assembleResponse (response) {
        var sender,
            formatUserhost,
            formatNick,
            formattedReturn,
            nick;
            
        // In case sender is a nick!user@host, parse the nick.
        try {
            formatUserhost = new RegExp(/\b[^]*(.*?)!/);                // :nick!user@host => 
            nick = formatUserhost.exec(response[0]);                    // [n,i,c,k,!] =>
            formatNick = nick.join("");                                 // nick! => 
            sender = (formatNick.substring(0,(formatNick.length-1)));   // nick => Done.
        } catch(e) {
            sender = undefined;
        }
        
        var returnObject = {
            method: response[1],
            receiver: response[2],
            sender: sender,
            message: response.slice(3)
        };

        return returnObject;
    }

    module.exports = ircClient;
})();
