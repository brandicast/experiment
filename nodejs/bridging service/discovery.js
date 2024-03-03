var http = require("http");
//var querystring = require('querystring');
var express = require("express");
var stbclient = require("./stbclient");

var app = express();
app.use(express.json());

let stbs = null;

app.get("/", function (req, res) {
    res.send("This is Discovery Service !");
});

app.get("/list", function (req, res) {
    console.log("STBs is null? " + (stbs == null));
    result = "";
    for (let key in stbs) {
        result += "<li>" + key + ":" + stbs[key].toJsonString() + ", and isConnected? " + stbs[key].isConnected();
    }
    res.send(result);
});

app.get("/send", function (req, res) {
    stbs[req.query.smc].sendMessage(req.query.msg);
    res.send("Send !");
});

app.post("/", function (req, res) {
    console.log("[Discovery]" + " Receiving request from " + req.ip + " with data  : " + JSON.stringify(req.body));
    payload = req.body;

    status = 200;
    msg = "OK !";
    if (payload.smc != null) {

        if (payload.action != null) {
            switch (payload.action) {
                case "status":
                default: { // STB asking for status 
                    ep = getEndPoint(payload.smc);
                    if (ep != null) {
                        status = 200;
                        msg = `{"code":0, "url":"${ep.getEndPoint()}"}`;
                    } else {
                        status = 400;
                        msg = '{"code":1, "msg":"Pair First !"}';
                    }
                    break;
                }
                case "pair": { // STB asking for pairing
                    if (isValidSMC(payload.smc)) {
                        if (payload.num != null) {
                            param = payload.num;
                            if (param == "CONFIRMED") { // Meaning this is the pairing result from Remote Control 
                                client = registerClient(payload.smc);
                                msg = `{"code":0, "msg":"OK","endpoint":"${client.getEndPoint()}","SMS":${payload.smc}}`;
                            } else { // Meaning this is the pairing request from STB
                                status = forwardPairingCode(payload.smc, payload.param); //   TODO: here needs to check params == null ;
                                if (status == 200) {
                                    //'''{"code":0, "msg":"OK", "endpoint":"Not Ready", "SMS":"%s-%s,%s", "parameters":"%s"}''' % (varify_so, varify_subsid, varify_smartcard, escape_datas)
                                    msg = `{"code":0, "msg":"OK","endpoint":"Not Ready","SMS":${payload.smc}}`;
                                } else {
                                    //buf =  '''{"code":0, "msg":"%s", "smc":"%s"}''' % (retsult_json['status'], jsonObj['smc'])
                                    msg = '{"code":1, "msg":"OAuth Server Error"}';
                                }
                            }
                        }
                    } else {
                        status = 400;
                        msg = '{"code":1, "msg":"Invalid  Smart Card  (Verified by SMS)"}';
                    }
                    break;
                }
                case "unpair": { // STB asking for unpair
                    unRegisterClient(payload.smc);
                    break;
                }
            }
        } else if (payload.cmd != null) {
            stb_is_alive = forward_request(payload.smc, payload.cmd);
            if (!stb_is_alive) {
                status = 400;
                msg = "STB is not connected";
            }
        } else {
            status = 400;
            msg = "Invalid Action !";
        }
    } else {
        status = 400;
        msg = "Invalid Smart Card ! ";
    }
    res.status(status).send(msg);
});

function forward_request(smc, cmd) {
    stb_is_alive = false;
    if (stbs != null) {
        if (stbs[smc] != null) {
            console.log("[Discovery]  Forwarding  message : " + cmd + " for " + smc);
            stb_is_alive = stbs[smc].sendMessage(cmd);
        }
    }
    return stb_is_alive;
}

function getEndPoint(smc) {
    return stbs[smc];
}

function isValidSMC(smc) { // TODO : here to check with SMC for valid smart card
    return true;
}

function registerClient(smc) {
    stbs[smc] = new stbclient(smc, getAllocatedEndPoint(smc));
    return stbs[smc];
}

function unRegisterClient(smc) {
    delete stbs[smc];
}

function getAllocatedEndPoint(smc) { //  TODO :    Here need to  dynamically check resources and allocate resource
    return "172.18.129.66:9999";
}

function forwardPairingCode(smc, pin_code) {
    status = 200;
    var post_data = `smart_card=${smc}&code=${pin_code}`;
    var options = {
        hostname: '172.18.129.66',
        port: 80,
        path: '/api/v1/pairing',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    };

    var req = http.request(options, function (res) {
        status = res.statusCode;
        console.log('STATUS: ' + res.statusCode);
        req.on('error', function (e) {
            console.log('problem with request: ' + e.message);
            status = 400;
        });

    });
    // write data to request body
    req.write(post_data);
    req.end();
    return status;
}

exports.start = function (port) {
    app.listen(port);
    console.log("Discovery Service Running on " + port + " !");
}

exports.set_stbs_reference = function (endpoint_stbs) {
    stbs = endpoint_stbs;
}

exports.init = function () {
    registerClient("009804199718");
    registerClient("123");
}