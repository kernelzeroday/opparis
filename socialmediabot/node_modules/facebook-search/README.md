# node-facebook-search

A simple Facebook Graph Searching API for [node.js] (http://nodejs.org). This module requires that you have a FaceBook APP ID, check out [Facebook - Authenticating as an App] (https://developers.facebook.com/docs/authentication/applications/). For more information about the Search API check out the [Facebook Developer API] (https://developers.facebook.com/docs/reference/api/).

## Install
```
npm install facebook-search
```

## Usage
```
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
```

## Licence
The MIT License (MIT)
Copyright (c) 2012 Code-IO.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.