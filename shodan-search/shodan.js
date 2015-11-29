//npm install -g shodan-client
//node shodan.js query facets apikey

var ShodanClient = require('shodan-client'),
    options = {
        key: process.argv[4],
    },
    shodanClient = new ShodanClient(options),
    searchOptions = {
        query: process.argv[2],
        limit: 5,
        facets: process.argv[3],
        minify: false
    };

shodanClient.search(searchOptions,  function (data, err) {
    console.log('\n------------------- search -------------------');
    if (err) {
        console.log('ERROR: shodanClient.search: ' + err);
    } else {
        console.log(data);
    }
});

shodanClient.streamBanners(function (data, err) {
    console.log('\n------------------- streamBanners -------------------');
    if (err) {
        console.log('ERROR: shodanClient.streamBanners: ' + err);
    } else {
        console.log(data);
    }
});

var searchOptionsExploits = {
    query: process.argv[2],
    facets: process.argv[3],
    page: 1
};

shodanClient.exploitSearch(searchOptionsExploits,  function (data, err) {
    console.log('\n------------------- exploitSearch -------------------');
    if (err) {
        console.log('ERROR: shodanClient.exploitSearch: ' + err);
    } else {
        console.log(data);
    }
});

shodanClient.profile(function (err,data) {
    if (err) {
        console.log ("ERROR: shodanClient.profile: " + err);
    } else {
        console.log ("Profile query success. You have " + data.credits + " query credits remaining.");
    }
});

