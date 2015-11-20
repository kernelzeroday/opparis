var qs = require('querystring'),
    crypto = require('crypto');

module.exports.parseSignedRequest = function(req, secret) {
    var parts = req.split('.', 2);
    
    var sig = _base64UrlToBase64(parts[0]);
    var data = JSON.parse(_base64UrlToString(parts[1]));
    
    if (!data.algorithm || data.algorithm.toUpperCase() != 'HMAC-SHA256') {
        console.error('Unknown algorithm. Expected HMAC-SHA256');
        return null;
    }

    var expectedSig = crypto.createHmac('sha256', secret).update(parts[1]).digest('base64');
    
    if (sig !== expectedSig) {
        console.error('Bad signed JSON Signature!');
        return null;
    }
    
    return data;
};

function _base64ToString(str) {
    return (new Buffer(str || "", "base64")).toString("ascii");
};

function _base64UrlToString(str) {
    return _base64ToString(_base64UrlToBase64(str));
};

function _base64UrlToBase64(str) {
    var pad = (4 - (str.length % 4));
    
    for (var i = 0;i < pad;i++) {
        str += '=';
    }
    
    return str.replace(/\-/g, '+').replace(/_/g, '/');
};
