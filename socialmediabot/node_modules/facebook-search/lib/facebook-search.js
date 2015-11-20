var https = require('https'),
    url = require('url'),
    qs = require('querystring'),
    _ = require('underscore'),
    fbutil = require('./facebook-utils');

function FacebookSearch(apiKey, apiSecret, opts) {
    this.auth = {
        key: apiKey,
        secret: apiSecret,
        token: undefined,
        code: undefined
    };
    
    this.config = _.defaults((opts || {}), {
        'redirect_uri': 'http://127.0.0.1:3000/',
        'protocol': 'https',
        'host': 'graph.facebook.com',
        'oauth_path': '/oauth/access_token',
        'search_path': '/search',
        'scope': 'client_credentials'
    });
    
    this.paging = {};
};

FacebookSearch.prototype.getAuthorizationUrl = function(opts) {
    opts = _.defaults((opts || {}), {
        'redirect_uri': this.config.redirect_uri,
        'protocol': this.config.protocol,
        'scope': this.config.scope,
        'host': 'www.facebook.com',
        'path': '/dialog/oauth'
    });

    query = {
        'client_id': this.auth.key,
        'redirect_uri': opts.redirect_uri,
        'scope': _.isArray(opts.scope) ? opts.scope.join(',') : opts.scope
    };
    
    return url.format({
        protocol: opts.protocol,
        host: opts.host,
        pathname: opts.path,
        query: query
    });
};

FacebookSearch.prototype.handleAuthorizationResponse = function(res, cb) {
    var data = qs.parse(res);
    
    if(data.error) {
        cb({error: {type: data.error_reason, message: data.error_description}});
    } else {
        this.auth.code = data.code;
        
        this.requestAccessToken(cb);   
    }
};

FacebookSearch.prototype.handleSignedRequest = function(req) {
    var data = fbutil.parseSignedRequest(req, this.auth.secret);
    
    if(data) {
        this.auth.token = data.oauth_token;
    }
    
    return this.auth.token;
};

FacebookSearch.prototype.setAccessToken = function(token) {
    this.auth.token = token;
};

FacebookSearch.prototype.requestAccessToken = function(uri, cb) {
    if(typeof uri === 'function') {
        cb = uri;
        uri = this.config.redirect_uri;
    }
 
    var self = this;
    query = {
        'client_id': self.auth.key,
        'client_secret': self.auth.secret,
        'redirect_uri': uri
    };
    
    if(self.auth.code) {
        _.extend(query, {
            'code': self.auth.code   
        });
    } else {
        _.extend(query, {
            'grant_type': 'client_credentials'
        });
    }

    _doRequest(url.format({
        protocol: self.config.protocol,   
        host: self.config.host,
        pathname: self.config.oauth_path,
        query: query
    }), function(err, tok) {        
        if(tok !== undefined) {
            self.auth.token = qs.parse(tok).access_token;
        }
        
        cb(err, self.auth.token);
    });  
};

FacebookSearch.prototype.search = function(req, cb) {
    if(arguments.length == 2) {
        if(typeof req === 'string') {
            req = {q: req};
        }
        
        var self = this;
        
        req = _.defaults(req, {
            'type': 'post'
        });
        
        this.request(self.config.search_path, req, function(err, res) {
            if(res.error) {
                cb(res.error);
            } else {
                self.paging = res.paging;
                
                cb(null, res.data);
            }          
        });
    } else {
        cb({error: {message: 'Not enough arguments'}});
    }
};

FacebookSearch.prototype.request = function(path, opts, cb) {
    if(typeof opts === 'function') {
        cb = opts;
        opts = {};
    }
    
    var self = this;
    
    if(this.auth.token) {           
        opts = _.defaults(opts, {
            'access_token': this.auth.token
        });
      
        _doRequest(url.format({protocol: self.config.protocol, host: self.config.host, pathname: path, query: opts}), function(err, res) {
            cb(err, JSON.parse(res));
        });
    } else {
        self.requestAccessToken(function(err, res) {
           if(res) self.request(path, opts, cb);
           else cb(err);
        });
    }
};

FacebookSearch.prototype.previous = function(cb) {
    this.page('previous', cb);
};

FacebookSearch.prototype.next = function(cb) {
    this.page('next', cb);
};

FacebookSearch.prototype.page = function(dir, cb) {
    var self = this;

    if(self.paging[dir]) {
        _doRequest(self.paging[dir], function(err, res) {
            res = JSON.parse(res);
            
            if(res.error) {
                cb(res.error);
            } else {
                self.paging = res.paging;
                
                cb(null, res.data);
            }          
        });
    } else {
        cb({error: {message: 'Invalid page'}});
    }
}

function _doRequest(req, cb) {
    if(typeof req === 'string') req = url.parse(req);
    
    https.get(req, function(res) {
        var buffer = '';
        
        res.on('data', function(d) {
            buffer += d;
        }).on('end', function() {
            cb(null, buffer);
        });
    }).on('error', function(e) {
        cb(e);
    });
};

module.exports = FacebookSearch;
