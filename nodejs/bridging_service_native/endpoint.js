// https://nodejs.org/docs/latest/api/net.html#net_server_address
let net = require('net');
let secure = require("./lib/endecode.js")

let stbs = {};
let encode = 0;

let server = net.createServer(function (socket) {
   console.log('[EndPoint]  Client Connected ' + socket.remoteAddress + " :" + socket.address().port);
   zombie = true;
   socket.setTimeout(33 * 1000);
   socket.on('data', function (data) {
      if (encode == 1) {
         try {
            data = secure.strdecode(("" + data).trim()); // Decode Data first
         } catch (e) {
            console.log("[EndPoint] Incoming  data decode error  : " + data);
         }
      }
      console.log("[EndPoint]  Receiving : " + data);

      zombie = false;
      illegal = false;
      msg = "";

      if (isValidClient(data)) {
         try {
            data = JSON.parse(data);
            if (data.action != null) {
               switch (data.action) {
                  case "connect":
                  default: {
                     if (isRegistered(data)) {
                        stbs[data.smc].setSocket(socket);
                        msg = `{"code":0,"url":"${stbs[data.smc].getEndPoint()}"}`;
                     } else {
                        msg = '{"code":1,"msg":"Pair First"}';
                     }
                     console.log("[ENDPOINT]" + " Reply CONNECT command for  " + data.smc + " with returning msg = " + msg);
                     break;
                  }
                  case "disconnect": {
                     stbs[data.smc].closeSocket();
                     delete stbs[data.smc];
                     break;
                  }
               }
            } else {
               msg = '{"code":1,"msg":"Not a valid action!"}';
               console.log("[ENDPOINT]" + msg);
            }
         } catch (e) {
            console.log("\"" + data + "\"" + " may not a valid EndPoint Protocol !  :  " + e);
            msg = '{"code":1,"msg":"Not a legal endpoint protocol ! "}';
            illegal = true;
         }
         if (encode == 1) {
            try {
               msg = secure.strencode(msg); ///    Encrypt Message Here....
            } catch (e) {
               console.log("EndPoint] Encoding Error : " + msg);
            }
         }
      } else {
         msg = '{"code":1,"msg":"Not a valid client command!"}';
         console.log("[ENDPOINT]" + msg);
      }

      if (msg != "") {
         msg = msg + "\n";
         socket.write(msg);
      }
      if (illegal) {
         socket.end();
      }

   });

   socket.on("error", () => {
      console.log("[EndPoint] Error ! Socket was interrupted : " + socket.remoteAddress);
   })

   socket.on("end", () => {
      console.log("[EndPoint] End ! Socket was ended !");
   })

   socket.on("close", () => {
      console.log("[EndPoint] Close ! Socket was closed !");
   })

   socket.on("timeout", () => {
      try {
         console.log("[EndPoint] Timeout ! Socket was timeouted !");
         socket.end();
      } catch (e) {
         console.log(e);
      }

   })

   setTimeout(function () {
      if (zombie) {
         socket.end();
         console.log("[EndPoint] No action in 10 secs.  Consider as Zombie ! End the Socket !")
      }
   }, 10000); // if socket connection without any data packet

});

function isValidClient(d) {
   let validclient = false;
   try {
      d = JSON.parse(d);
      validclient = (d.smc != null);
   } catch (e) {
      console.log("[EndPoint] Client Validation Error  : " + d);
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

exports.init = function (enc) {
   encode = enc;
}

exports.get_connected_stbs = stbs;