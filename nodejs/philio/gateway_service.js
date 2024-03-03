// https://nodejs.org/docs/latest/api/net.html#net_server_address
let net = require('net');
let ph = require ("./protocol_handler_philio.js") ;
let line = require ("./LineNotify/LineNotify.js") ;
let server = net.createServer(function (socket) {
  console.log('Client Connected ' + socket.address().address + " :" + socket.address().port);
  socket.setTimeout(0);

  socket.on('data', function (data) {
    
    var newData = new String (data)  ; 
    if (data[data.length-1] == 0 )
        newData = newData.substr (0, newData.length-1) ;
    newData = newData.trim () 

    try {
     dataJson = JSON.parse(newData );
    }
    catch (e)  {
      console.log (e.code + ":" + e.message ) ;
      console.log (e.stack) ;
      console.log ("[EXCEPTION] " + "#" + newData + "#") ;
      dataJson = null ;
    }
  
    if (dataJson != null) {
      //console.log('---------------------------------------------------Start------------------------------------------------------------------------------');
        //iterateData (dataJson) ;

        event_msg = ph.protocolHandler (dataJson) ;
        if (event_msg.length > 0)
            line.sendMessageToAll (event_msg) ;

      //console.log('---------------------------------------------------Event------------------------------------------------------------------------------\n');     
     // console.log('\n');     
    }
    
  });
});

/*
function iterateData (dataJson)  {
  Object.keys(dataJson).forEach(type => {
    let handler = ph[type];
    if (handler)  {
        console.log ("processing " + type ) ;
        handler(dataJson[type]);
    } 
    else  {
        console.log ("[" + type  + "]" + " is not handled ! ") ;
    }
      
  });
}
*/

exports.start = function (port) {
  server.listen(port, function () {
    console.log('Gateway Service listen on ' + port);
  });
};