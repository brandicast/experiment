// https://nodejs.org/docs/latest/api/net.html#net_server_address
let net = require('net');
let ph = require ("./protocol_handler_philio.js") ;
let notifier = require ("./notifier.js") ;
let bot = require ('./linebot_handler.js') ;
const config  = require ('./config.js') ;
let mqtt = requiret('./mqtt_client.js');

const log4js = require("log4js");
log4js.configure (config.log4js_set) ;
const logger =  log4js.getLogger("Gateway_Manager") ;

let server = net.createServer(function (socket) {
  logger.info('Client Connected ' + socket.address().address + " :" + socket.address().port);
  socket.setTimeout(0);

  bot.setInfoDatabase (ph.getDatabase() ) ;
  bot.setNotifier(notifier) ;

 notifier.setInfoDatabase (ph.getDatabase()) ;

  socket.on('data', function (data) {
    
    var newData = new String (data) .replace('\0','').split ("\n") ; 
    
    for (var i=0; i<newData.length; i++) {
      var processData =  newData[i].trim() ; 
      if (processData.length > 0) {
        
      try {
          dataJson = JSON.parse(processData );
        }
      catch (e)  {
        logger.debug (e.code + ":" + e.message ) ;
        logger.debug (e.stack) ;
        logger.error ("[EXCEPTION] " + "#" + processData + "#") ;
        dataJson = null ;
      }
  
    if (dataJson != null) {
        event_msg = ph.protocolHandler (dataJson) ;
        if (event_msg.length > 0)
          notifier.sendMessageToAll (event_msg) ;
          
    }
  }
  }
});

socket.on('error', function (data) {
    logger.error (data) ;
})

});

exports.start = function (port) {
  server.listen(port, function () {
    logger.info('Gateway Service listen on ' + port);
  });
};