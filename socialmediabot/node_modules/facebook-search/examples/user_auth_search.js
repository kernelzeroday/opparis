var url = require('url'),
    express = require('express'),
    FacebookSearch = require('facebook-search');

var app = express.createServer(express.logger());
var port = (process.env.PORT || 3000);
var fb = new FacebookSearch('YOUR_APP_ID', 'YOUR_APP_SECRET',
                            {
                                'redirect_uri': 'http://127.0.0.1:'+port+'/auth/facebook',
                                'scope': 'user_status'
                            });

app.use(express.bodyParser());
app.use(express.cookieParser());
app.use(express.session({secret: 'secret'}));

app.post('/', function(req, res) {
    // Deal with Facebook Canvas POST
    var tok = fb.handleSignedRequest(req.body.signed_request);
    
    if(tok !== undefined) {
        req.session.token = tok;
        
        res.redirect('/home');
    } else {
        res.redirect(fb.getAuthorizationUrl({'redirect_uri': req.header('referrer')}));
    }
});

app.get('/', function(req, res) {
    if(req.session.token) {
        res.redirect('/home');
    } else {
        res.redirect(fb.getAuthorizationUrl());
    }
});

app.get('/home', function(req, res) {
    if(req.session.token) {
        fb.setAccessToken(req.session.token);
        
        var searchFor = {
            type: 'place',
            q: 'beer',
            center: '48.13708, 11.5756',
            distance: 1000
        };
        
        fb.search(searchFor, function(err, data) {
            res.send(err ? err : data);
        });
    } else {
        res.redirect(fb.getAuthorizationUrl());
    }
});

app.get('/auth/facebook', function(req, res) {
    fb.handleAuthorizationResponse(url.parse(req.url).query, function(err, tok) {        
        if(tok !== undefined) {
            req.session.token = tok;
            
            res.redirect('/home');
        } else {
            res.send(err);
        }
    });
});

app.listen(port, function() {
  console.log("Listening on " + port);
});