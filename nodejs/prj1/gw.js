const io = require ('socket.io-client') ('https://io.luffanet.com.tw?token=token');

io.on ('connect', function(){
	 console.log ('connected', io.id); 
});

io.on('data', function (data) {
	console.log ('event', io.id, data);
})




