'use strict';

// https://developer.shodan.io/api/stream

var util = require('util'),

    ShodanClient = require('shodan-client'),

    options = {
        key: process.argv[2],
        timeout: 15000
    },
    shodanClient = new ShodanClient(options);


shodanClient.streamBanners(function (err, data) {
    console.log('\n------------------- streamBanners -------------------');
    if (err) {
        console.log('ERROR: shodanClient.streamBanners: ' + err);
    } else {
        console.log(util.inspect(data, { depth : 6 }));
    }
});

shodanClient.streamGeo(function (err, data) {
    console.log('\n------------------- streamGeo -------------------');
    if (err) {
        console.log('ERROR: shodanClient.streamGeo: ' + err);
    } else {
        console.log(util.inspect(data, { depth : 6 }));
    }
});

shodanClient.streamPorts('23', function (err, data) {
    console.log('\n------------------- streamPorts -------------------');
    if (err) {
        console.log('ERROR: shodanClient.streamPorts: ' + err);
    } else {
        console.log(util.inspect(data, { depth : 6 }));
    }
});
