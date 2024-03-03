let https = require('https');
let querystring = require ('querystring');


function doHTTPSPost (options, postData, callback)  {
    
    var req = https.request(options, (res) => {

      res.on('data', (d) => {
        console.log ("[Reply from " + options.hostname + options.path + "]" + d) ;
        if (callback)
            callback (d) ;
      });
    });

    req.on('error', (e) => {
        console.log ("[Reply from notify-bot.line.me] " + e) ;
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

sendMessage ('6iZh1YdbArCmuakc0QTAbXIvysY6YSbGxLf2Qjjkpb8', 'I can\'t tell you why');