var PORT = 41848;
var MCAST_ADDR = "225.0.0.1"; //same mcast address as Server
var HOST = '192.168.0.15'; //this is your own IP
var dgram = require('dgram');
var client = dgram.createSocket({
    type: 'udp4',
    reuseAddr: true
});

client.on('listening', function () {
    var address = client.address();
    console.log('UDP Client listening on ' + address.address + ":" + address.port);
    client.setBroadcast(true)
    client.setMulticastTTL(1);
    client.addMembership(MCAST_ADDR);
});

client.on('message', function (message, remote) {
    console.log('MCast Msg: From: ' + remote.address + ':' + remote.port + ' - ' + message);
});

client.bind(PORT);