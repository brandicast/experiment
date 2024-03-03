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
        this.socket.write(msg);
        sent = true;
    } catch (e) {
        console.log("[STBCLIENT] Forwarding message Error ! Socket could be closed !");
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

module.exports = stbclient;