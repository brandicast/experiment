
'use strict';
const querystring = require('querystring');
const https = require('https');
const express = require('express');
const PORT = 8888;
const HOST = '0.0.0.0';
const app = express();

var token_list = [] ;

app.get('/', (req, res) => {
   res.sendfile('index.html', function(err) {
        if (err) res.sendFile(404);
    });
});

app.get("/code_receiver", (req, res) => {
    console.log ("CODE = " + req.query.code) ;
    res.sendfile('success.html', function(err) {
        if (err) res.sendFile(404);
    });
    getToken (req.query.code) ;
}) ;

app.listen(PORT, HOST);


function getToken(code) {
    doHTTPSPost (code) ;  
}

function doHTTPSPost (code)     {

    var postData = querystring.stringify({
        'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri': 'http://192.168.0.18:8888/code_receiver',
        'client_id' : 'id',
        'client_secret' : 'secret'
    });

    console.log ("[Send to  notify-bot.line.me] "+postData) ;

    var options = {
        hostname: 'notify-bot.line.me', 
        path: '/oauth/token',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
           // 'Content-Length': Buffer.byteLength(data)
          }
        }
        
    var req = https.request(options, (res) => {
      console.log('statusCode:', res.statusCode);
      //console.log('headers:', res.headers);
    
      res.on('data', (d) => {
        console.log ("[Reply from notify-bot.line.me] " + d) ;
        if (res.statusCode ==200)
            token_list.push (d) ;
      });
    });

    req.on('error', (e) => {
        console.log ("[Reply from notify-bot.line.me] " + d) ;
    });

    req.write(postData);
    req.end();
}

exports.getTokenList = function () {
    return token_list ;
}