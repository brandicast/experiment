
// https://nodejs.org/docs/latest/api/net.html#net_server_address
let net = require('net');
var stbclient = require ("./stbclient") ;

let stbs = {} ;

let server = net.createServer(function(socket){
  console.log('Client Connected ' + socket.remoteAddress  + " :"   + socket.address().port) ;
    socket.on ('data', function (data ){
         console.log ("Server Receiving : " + data) ;
                
         let invalid_client = false ;
         try{
            data = JSON.parse (data) ;
            invalid_client =  (data.smc == null)  ;
            console.log (invalid_client) ;
         }
         catch (e) {
             console.log ( "\"" +  data + "\"" +  " may not a valid JSON String !  :  "  + e   ) ;
             invalid_client = true ;
         }
         

         if (invalid_client) {
            socket.end () ;
         } else {             
             if (stbs[data.smc] == null)  {
                stbs[data.smc] = new stbclient (data.smc, "");  
                stbs[data.smc].setSocket (socket) ;
                stbs[data.smc].sendMessage ("Hi ! " + data.smc) ;
                socket.write ("Hi ! " + data.smc) ; 
                console.log ("[ENDPOINT]" + " adding stb for " + data.smc + ":" + Object.keys (stbs).length)  ;
             }
             else{
                stbs[data.smc].sendMessage ("[ECHO] "  + JSON.stringify(data)) ;
                if (data.action == "close") {
                    delete stbs[data.smc] ;
                    console.log ("deleting "  +data.smc + " : size : " + Object.keys (stbs).length) ; 
                }
             }
            
            
         }       
    });



});


exports.start  =  function (port) {
    server.listen(port,'192.168.0.17',function(){
    console.log("End Point Service  running on " + port  +" !");
});
}

exports.get_connected_stbs =  stbs ;

server.listen(9999,'192.168.0.17',function(){
    console.log("End Point Service  running on " + 9999  +" !");
})