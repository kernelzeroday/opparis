var FacebookSearch = require('facebook-search');

var fb = new FacebookSearch('YOUR_APP_ID', 'YOUR_APP_SECRET');
var searchFor = {
    type: 'place',
    q: 'beer',
    center: '48.13708, 11.5756',
    distance: 1000
};

fb.search(searchFor, function(err, res) {
    console.log(err ? err : res);
    
    fb.next(function(err, res) {
        console.log(err ? err : res);
    });
});
