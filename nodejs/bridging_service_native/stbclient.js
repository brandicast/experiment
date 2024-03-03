let secure = require("./lib/endecode.js");
const util = require('util');



function stbclient(smc, endpoint_address) {
    this.smc = smc;
    this.endpoint = endpoint_address;
}

stbclient.prototype.setSocket = function (socket) {
    this.socket = socket;
}

stbclient.prototype.isMe = function (smc) {
    return (this.smc == smc);
}

stbclient.prototype.isConnected = function () {
    isConnected = false;
    if (this.socket != null) {
        isConnected = (this.socket.remoteAddress != null)
    }
    return isConnected;
}

stbclient.prototype.sendMessage = function (msg) {
    sent = false;
    try {

        console.log(util.inspect(this.socket, {
            showHidden: true
        }));
        // msg = secure.strencode(msg);
        if (this.isConnected()) {
            console.log("[STBCLIENT] Forwarding message to " + this.smc + ":" + msg);
            this.socket.write(msg + "\n");
            sent = true;
        } else {
            console.log("[STBCLIENT] Can not Forwarding message to " + this.smc + ":" + msg + ".  Because Socket doesn not seem Connected !");
        }
    } catch (e) {
        console.log("[STBCLIENT] Forwarding message Error ! Socket could be closed !" + e);
    }
    return sent;
}

stbclient.prototype.toJsonString = function () {
    return `{"smc":"${this.smc}","endpoint":"${this.endpoint}"}`;
}

stbclient.prototype.getEndPoint = function () {
    return this.endpoint;
}

stbclient.prototype.getSMC = function () {
    return this.smc;
}

stbclient.prototype.closeSocket = function () {
    try {
        if (this.socket != null) {
            this.socket.end();
        }
    } catch (e) {
        console.log("trying to close socket for " + this.smc + " , but socket is already closed !");
    }
}

module.exports = stbclient;