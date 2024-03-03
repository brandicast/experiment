var PORT = 41848;
var MCAST_ADDR = "225.0.0.1"; //not your IP and should be a Class D address, see http://www.iana.org/assignments/multicast-addresses/multicast-addresses.xhtml
var dgram = require('dgram'); 
var server = dgram.createSocket("udp4"); 

exports .start = function start () {
    server.bind(PORT, function(){
        server.setBroadcast(true);
        server.setMulticastTTL(0);
        server.addMembership(MCAST_ADDR);
    });
}

//setInterval(broadcastNew, 3000);

exports.broadcast = function broadcastNew(msg) {
    //var message = new Buffer(news[Math.floor(Math.random()*news.length)]);
    server.send(msg, 0, msg.length, PORT,MCAST_ADDR);
    console.log("Sent " + msg + " to the wire...");
}