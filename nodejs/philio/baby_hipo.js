let gw = require("./gateway_service.js");
//let sio = require("./socket_io_service.js");

const GATEWAY_PORT = 9613;
//const SOCKET_IO_PORT = 8001;

gw.start(GATEWAY_PORT);
//sio.start(SOCKET_IO_PORT);