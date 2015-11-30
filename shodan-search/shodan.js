//npm install -g shodan-client
//node shodan.js query apikey

'use strict';

// https://developer.shodan.io/api

var util = require('util'),

    ShodanClient = require('shodan-client'),

    options = {
        key: process.argv[3],
        timeout: 15000
    },
    shodanClient = new ShodanClient(options),
    searchOptions,
    // countOptions,
    hostOptions;


// Minimal required parameters
hostOptions = { ip: '1.1.1.1' };

// Full supported params
// hostOptions = {
//     ip: '1.1.1.1',
//     history: true,    // default is false
// };

shodanClient.host(hostOptions, function (err, data) {
    console.log('\n------------------- host -------------------');
    if (err) {
        console.log('ERROR: shodanClient.host: ' + err);
    } else {
        console.log(util.inspect(data, { depth : 6 }));
    }
});


// Full supported params
// TODO: API still fails with some of them
searchOptions = {
    query: process.argv[2],
    // query: 'asterisk port:5060',
    // query: encodeURIComponent('openssh port:22'),
    // query: 'openssh+port%3A22',
    // query: 'penssh%20port%3A22',
    limit: 5,
    // facets: 'port:100',
    minify: false
};

// A premium account is needed in some cases, in the doc:
// " Uses 1 query credit if:
// - Page number > 1
// - Search query contains any of the following filters: city,
// country, net, geo, before, after, org, isp, title, html "
shodanClient.search(searchOptions,  function (err, data) {
    console.log('\n------------------- search -------------------');
    if (err) {
        console.log('ERROR: shodanClient.search: ' + err);
    } else {
        console.log(util.inspect(data, { depth : 6 }));
    }
});

// Minimal required parameters
// countOptions = {
//     query: 'freepbx'
// };

// Full supported params
// countOptions = {
//     query: 'freepbx',
//     facets: 'port:100'
// };

// shodanClient.count(countOptions,  function (err, data) {
//     console.log('\n------------------- count -------------------');
//     if (err) {
//         console.log('ERROR: shodanClient.count: ' + err);
//     } else {
//         console.log(util.inspect(data, { depth : 6 }));
//     }
// });

shodanClient.resolve('google.com,bing.com', function (err, data) {
    console.log('\n------------------- resolve -------------------');
    if (err) {
        console.log('ERROR: shodanClient.resolve: ' + err);
    } else {
        console.log(util.inspect(data, { depth : 6 }));
    }
});

shodanClient.reverse('74.125.227.230,204.79.197.200', function (err, data) {
    console.log('\n------------------- reverse -------------------');
    if (err) {
        console.log('ERROR: shodanClient.reverse: ' + err);
    } else {
        console.log(util.inspect(data, { depth : 6 }));
    }
});

shodanClient.myip(function (err, data) {
    console.log('\n------------------- myip -------------------');
    if (err) {
        console.log('ERROR: shodanClient.myip: ' + err);
    } else {
        console.log(util.inspect(data, { depth : 6 }));
    }
});
