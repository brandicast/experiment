// https://nodejs.org/docs/latest/api/net.html#net_server_address
let net = require('net');

let stbs = {};

let server = net.createServer(function (socket) {
   console.log('Client Connected ' + socket.remoteAddress + " :" + socket.address().port);
   zombie = true;
   socket.setTimeout(0);
   socket.on('data', function (data) {
      console.log("Server Receiving : " + data);
      zombie = false;

      if (isValidClient(data)) {
         try {
            data = JSON.parse(data);
            if (data.action != null) {
               switch (data.action) {
                  case "connect":
                  default: {
                     if (isRegistered(data)) {
                        stbs[data.smc].setSocket(socket);
                        msg = `{"code":"0","url":"${stbs[data.smc].getEndPoint()}"}`;
                     } else {
                        msg = '{"code":"1","msg":"Pair First"}';
                     }
                     socket.write(msg);
                     console.log("[ENDPOINT]" + " Reply CONNECT command for  " + data.smc + " with returning msg = " + msg);
                     break;
                  }
                  case "disconnect": {
                     delete stbs[data.smc];
                     break;
                  }
               }
            } else {
               msg = '{"code":"1","msg":"Not a valid action!"}';
               socket.write(msg);
               console.log("[ENDPOINT]" + msg);
            }
         } catch (e) {
            console.log("\"" + data + "\"" + " may not a valid EndPoint Protocol !  :  " + e);
         }
      } else {
         msg = '{"code":"0","msg":"Not a valid client command!"}';
         socket.write(msg);
         console.log("[ENDPOINT]" + msg);
      }

   });

   setTimeout(function () {
      if (zombie) {
         socket.end();
         console.log("[EndPoint] No action in 10 secs.  Consider as Zombie ! End the Socket !")
      }
   }, 10000); // if socket connection without any data packet

});

function isValidClient(data) {
   let validclient = false;
   try {
      data = JSON.parse(data);
      validclient = (data.smc != null);
   } catch (e) {
      //console.log("\"" + data + "\"" + " may not a valid EndPoint Command !  :  " + e);
   }
   return validclient;
}

function isRegistered(data) {
   return (stbs[data.smc] != null);
}


exports.start = function (port) {
   server.listen(port, function () {
      console.log("End Point Service  running on " + port + " !");
   });
}

exports.get_connected_stbs = stbs;