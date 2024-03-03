
'use strict';
const config = require ("../mimosa/config.js") ;
const querystring = require('querystring');
const https = require('https');
const express = require('express');
var fs = require("fs");
const PORT = config.line_notify.port;
const HOST = '0.0.0.0';
const app = express();

const log4js = require("log4js");
const logger =  log4js.getLogger("LineNotify") ;

var token_list =  {};
var database = null ;

app.get('/', (req, res) => {
    res.set('Content-Type', 'text/html');
    var redirect_script_html = '<script>'  + 
                                                           ' window.location.href = "'   + 
                                                            'https://notify-bot.line.me/oauth/authorize?' + 
                                                            'response_type=code' +
                                                            '&client_id='  + config.line_notify.client_id + 
                                                            '&redirect_uri=' + config.line_notify.redirect_uri + "?mac=123" +
                                                            '&scope=notify' + 
                                                            '&state=NO_STATE' + '";'  
                                                            +"</script>" ;
    res.send (redirect_script_html) ;
});

app.get("/code_receiver", (req, res) => {
    res.sendFile(config.line_notify.success_page, function(err) {
        if (err) res.sendFile(404);
    });
    getToken (req.query.code) ;
}) ;

app.get('/tokenlist', (req, res) => {
    res.set('Content-Type', 'text/html');
    let result = "Empty" ;
    if (token_list != null ) {
        result = "" ;
        token_list.MAC.forEach (token => {
            result += "<li>" + token  ;
        })
    }
    res.send (result) ;
});

app.get ('/database', (req, res) => {
        res.set ('content-type', 'application/json') ;
        if (database != null) {
            res.send (JSON.stringify(database)) ;
        }
        else {
            res.send ("Empty") ;
        }

});


function getToken(code) {

    var options = {
        hostname: 'notify-bot.line.me', 
        path:  '/oauth/token',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }     

        /*
        var urlParams  = new URLSearchParams();
        urlParams.append('grant_type','authorization_code');
        urlParams.append('code','haha');
        urlParams.append('redirect_uri',config.line_notify.redirect_uri + "?mac=123");
        urlParams.append('client_id',config.line_notify.client_id);
        urlParams.append('client_secret',config.line_notify.client_secret);

        */


    var postData = querystring.stringify({
        'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri':  config.line_notify.redirect_uri + "?mac=123",
        'client_id' : config.line_notify.client_id,
        'client_secret' : config.line_notify.client_secret
    });

    logger.debug (postData) ;

    doHTTPSPost (options, postData, registerToken) ;  
}
function registerToken (callbackdata) {
    try {
            var json_d = JSON.parse (callbackdata) ;
            if  (json_d.access_token)  {
                if (token_list.MAC == null)
                    token_list.MAC = [] ;
                 token_list.MAC.push (json_d.access_token) ;
                 fs.writeFileSync (config.line_notify.token_file, JSON.stringify(token_list)) ;
                 sendMessage (json_d.access_token, "Welcome Join !") ;
            }
    }
    catch (err) {
        logger.error (err) ;
        }
}

function doHTTPSPost (options, postData, callback)  {
    
    var req = https.request(options, (res) => {

      res.on('data', (d) => {
        logger.debug ("[Reply from " + options.hostname + options.path + "]" + d) ;
        if (callback)
            callback (d) ;
      });
    });

    req.on('error', (e) => {
        logger.error ("[Reply from notify-bot.line.me] " + e) ;
    });

    req.write(postData);
    req.end();
}

function sendMessage (token, msg) {

    var options = {
        hostname: 'notify-api.line.me', 
        path:  '/api/notify',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' ,
            'Authorization': 'Bearer ' + token 
          }
        }     

    var postData = querystring.stringify({
        'message' : msg
    });
    
    doHTTPSPost (options, postData) ;

}

function init () {
    try{
        let tmp = fs.readFileSync (config.line_notify.token_file) ;
        if (tmp)
            token_list = JSON.parse(tmp) ;
    }
    catch (err) {
        logger.error ("[LineNotify] No Init" ) ;
    }
}


app.listen(PORT, HOST);
logger.info ("[LineNotify] Server running on " +  HOST + ":" + PORT) ;
init() ;



exports.getTokenList = function () {
    return token_list ;
}

exports.sendMessageToAll = function (msg) {
    token_list.MAC.forEach (token => {
        sendMessage (token, msg) ;
    })   
    
}

exports.setInfoDatabase = function (db) {
    database = db ;
}