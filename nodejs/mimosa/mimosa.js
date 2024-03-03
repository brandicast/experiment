let gw = require('./gateway_manager.js');
let config = require ('./config.js') ;

gw.start(config.gateway.port);
