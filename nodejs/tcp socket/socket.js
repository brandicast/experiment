// https://nodejs.org/docs/latest/api/net.html#net_server_address
let net = require('net');
let server = net.createServer(function (socket) {
  console.log('Client Connected ' + socket.address().address + " :" + socket.address().port);
  socket.setTimeout(0);
  socket.on('data', function (data) {
    console.log("Server Receiving : " + data);
    // socket.write("[Server ECHO]" + data);
  });

});
server.listen(9613, function () {
  console.log('Server running on 9613 !');
});