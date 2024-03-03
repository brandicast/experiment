var http = require("http");
var io = require('socket.io');

let clients = {};

var server = http.createServer(function (request, response) {
  console.log('Connection');
  var path = request.url;

  switch (path) {
    case '/':
      response.writeHead(200, {
        'Content-Type': 'text/html'
      });
      response.write('Hello, World.');
      response.end();
      break;
    default:
      response.writeHead(404);
      response.write("opps this doesn't exist - 404");
      response.end();
      break;
  }
});

io.sockets.on("connection", function (socket) {
    socket

});


exports.start = function (port) {
  server.listen(port);
  io.listen(server);
  console.log('Socket IO listen on ' + port);
}