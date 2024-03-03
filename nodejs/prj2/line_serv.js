var http= require ('http') ;
var https=require ('https'); 
const port = 9999 ;

var server = http.createServer (function (req, res) {
 console.log ('URL : '+ req.url);

 console.log ("Method :" + req.method);

 console.log("Headers: " + req.rawHeaders) ;

 var post_data = '' ;
 req.on ('data', function (chunk){
	post_data += chunk ;
 }); 
	
 req.on ('end', function (){
	 console.log ("post_data :" + post_data) ; 
	 var parsed_data = JSON.parse(post_data); 
	 //console.log(parsed_data);
	 if (parsed_data.events)
	 {
	 console.log(parsed_data.events[0].replyToken);
	
	 var options = {
		hostname: 'api.line.me',
		path: '/v2/bot/message/reply',
		method: 'POST',
		headers: {'Content-Type': 'application/json',
					'Authorization': 'Bearer {yct/yeyDMvkabAaR8r7RIEZXwgHTm7oBFGmo7GWvDxMrap/poPdt3kyMM6p5Ku2sRg8i3uUXqSWGr7TseHKiMcQP7DxluYtE2L1CR7cjvDgRz9iU82aV5Qezt+YGv5jmaz2tpGQh4nKmsi780MyDqgdB04t89/1O/w1cDnyilFU=}'}
	  };

	  var req = https.request(options, function(res) {
		
		console.log('Status: ' + res.statusCode);
		res.setEncoding('utf8');
		res.on('data', function (body) {
		  console.log('Body: ' + body);
		});
	  });
	  req.on('error', function(e) {
		console.log('problem with request: ' + e.message);
	  });
	  // write data to request body


	  var response = '{"replyToken":"' + parsed_data.events[0].replyToken + '","messages":[{"type":"text","text":"Hello, user"}]	}' ;
	  console.log(response);
	  req.write(response);
	  req.end();	




	 }
 })
 

 res.writeHead(200,{'Content-Type':'text/html'});
 res.write ("OK"+ req.url);
 res.end ();


});

server.listen(port);

console.log ('NodeJS HTTP Server is running on ' + port ) ;



