var gw = require ('./gateway.js');

gw.em ('connect', function (data){	
	console.log (data);
});

