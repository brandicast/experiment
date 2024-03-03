var http = require("http");
var stbclient = require("./stbclient");
var secure = require("./lib/endecode.js");
var mysql = require('mysql');



var stbs = null;
var encode = 0; //  0 : clear ,  1 :  encode
var hostname = "172.18.129.66" ;

var server = http.createServer((req, res) => {

    switch (req.method) {
        case "GET":
        default: {
            let result = "";
            if (req.url = "/list") {
                for (let key in stbs) {
                    result += "<li>" + key + ":" + stbs[key].toJsonString() + ", and isConnected? " + stbs[key].isConnected();
                }
                res.setHeader('Content-Type', 'text/html');
            } else if (req.path = "/send") {
                stbs[req.query.smc].sendMessage(req.query.msg);
                result = "[Discovery] Forward the message to  " + req.query.smc + " with message : " + req.query.msg;
            } else
                result = "[Discovery] This is Discovery Service ! ";
            res.end(result);
            break;
        }
        case "POST": {
            let body = "";
            let payload = null;
            req.on("data", (chunk) => {
                body += chunk;
            });
            req.on("end", () => {
                if (req.url == "/rcs") { // Meaning this is from Remote Control Service
                    msg = '{"code":1, "msg":"Not OK"}';
                    status = 500;
                    try {
                        payload = JSON.parse(body);
                    } catch (e) {
                        console.log("[Discovery] RCS  POST data is not a JSON object  : " + body);
                        payload = null;
                        msg = '{"code":1, "msg":"Not a valid JSON object"}';
                        status = 500;
                    }

                    if (payload.smc != null) {
                        if (payload.cmd != null) {
                            stb_is_alive = forward_request(payload.smc, payload.cmd);
                            if (!stb_is_alive) {
                                status = 500;
                                msg = '{"code":1, "msg":"STB is not connected"}';
                            } else {
                                status = 200;
                                msg = '{"code":0, "msg":"Forwarding Request!"}';
                            }
                        } else if (payload.action != null) {
                            if (payload.action == "pair") {
                                if (isValidSMC(payload.smc)) {
                                    if (payload.num != null) {
                                        param = payload.num;
                                        if (param == "CONFIRMED") { // Meaning this is the pairing result from Remote Control 
                                            isA1 = true;
                                            try {
                                                isA1 = (payload.stb == "a1");
                                            } catch (e) {
                                                isA1 = true;
                                            }
                                            client = registerClient(payload.smc, isA1);
                                            msg = `{"code":0, "msg":"OK","endpoint":"${client.getEndPoint()}","SMS":"${payload.smc}"}`;
                                            status = 200;
                                        }
                                    }
                                }
                            }
                        }
                    } else {
                        status = 500;
                        msg = '{"code":1, "msg":"JSON format error"}';
                    }
                    res.statusCode = status;
                    res.setHeader('Content-Type', 'application/json');
                    res.end(msg);
                } else { //  Meaning this is from STB
                    if (encode == 1) {
                        try {
                            body = secure.strdecode(body.trim());
                        } catch (e) {
                            console.log("[Discovery] Incoming  POST data decode error  : " + body);
                            body = "";
                        }
                    }
                    try {
                        payload = JSON.parse(body);
                    } catch (e) {
                        console.log("[Discovery] Incoming  POST data is not a JSON object  : " + body);
                        payload = null;
                    }

                    status = 200;
                    msg = '{"code":"0","msg":"OK !"}';
                    if ((payload != null) && (payload.smc != null)) {
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
                                            status = forwardPairingCode(payload.smc, payload.num, (req.url == "/a1")); //   TODO: here needs to check params == null ;
                                            //status = 200;
                                            if (status == 200) {
                                                //'''{"code":0, "msg":"OK", "endpoint":"Not Ready", "SMS":"%s-%s,%s", "parameters":"%s"}''' % (varify_so, varify_subsid, varify_smartcard, escape_datas)
                                                msg = `{"code":0, "msg":"OK","endpoint":"Not Ready","SMS":"${payload.smc}"}`;
                                            } else {
                                                //buf =  '''{"code":0, "msg":"%s", "smc":"%s"}''' % (retsult_json['status'], jsonObj['smc'])
                                                msg = '{"code":1, "msg":"OAuth Server Error"}';
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
                        } else {
                            status = 400;
                            msg = '{"code":1, "msg":"Invalid  Action"}';
                        }
                    } else {
                        status = 400;
                        msg = '{"code":1, "msg":"Invalid  Payload"}';
                    }
                    res.statusCode = status;
                    res.setHeader('Content-Type', 'application/json');

                    if (encode == 1) {
                        try {
                            msg = secure.strencode(msg.trim());
                        } catch (e) {
                            console.log("[Discovery] Incoming  POST data decode error  : " + body);
                            msg = '{"code":1, "msg":"Response encode error "}';
                        }
                    }
                    console.log("[Discovery] " + msg);
                    res.end(msg);
                }
            });
            break;
        }
    }
});



function forward_request(smc, cmd) {
    stb_is_alive = false;
    if (stbs != null) {
        if (stbs[smc] != null) {
            console.log("[Discovery]  Forwarding  message : " + cmd + " for " + smc);
            if (encode == 1) {
                try {
                    cmd = secure.strencode(cmd.trim());
                } catch (e) {
                    console.log("[Discovery] Forwarding data decode error  : " + cmd);
                    cmd = '{"code":1, "msg":"Forwarding CMD encode error "}';
                }
            }
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

function registerClient(smc, isA1) {
    stbs[smc] = new stbclient(smc, getAllocatedEndPoint(smc, isA1));
    return stbs[smc];
}

// TODO : 要跟 Remote Control Service 說 Unpair
function unRegisterClient(smc) {
    delete stbs[smc];
    forwardUnPairingCode(smc);
}

// TODO : Production需要分單號卡跟雙號卡，分配 EndPoint Service的loading
// A1有先跟凱擘協調，可能得用port來分，比方說 211.76.126.125:8002
// PSTB可以用IP 
function getAllocatedEndPoint(smc, isA1) {
    isA1 = true; 
    let ep = "211.76.126.125:8001"
    if (isA1) {
        ep = "211.76.126.125:8001"
    } else {
        ep = "172.18.129.65:8001";
    }
    return ep;

}

function forwardPairingCode(smc, pin_code, so_id, isA1) {
    status = 200;
    var post_data = `smart_card=${smc}&code=${pin_code}&so_id=${so_id}&stb=` + (isA1 ? "a1" : "p");
    var options = {
        hostname: `172.18.129.66`,
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
    console.log(post_data);
    req.write(post_data);
    req.end();
    return status;
}

// 跟 Remote Control Service說要unpair
function forwardUnPairingCode(smc) {
    status = 200;
    var post_data = `smart_card=${smc}`;
    var options = {
        hostname: '172.18.129.66',
        port: 80,
        path: '/api/v1/unpairing',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    };

    var req = http.request(options, function (res) {
        status = res.statusCode;
        if (status == 200)
            console.log("[Discovery] UNPair " + smc + " successful !");
        else
            console.log("[Discovery] UNPair " + smc + " UNsuccessful !");
        req.on('error', function (e) {
            console.log('[Discovery] UNPair process error : ' + e.message);
            status = 400;
        });

    });
    // write data to request body
    console.log(post_data);
    req.write(post_data);
    req.end();
    return status;
}

exports.start = function (port) {
    server.listen(port);
    console.log("[Discovery] Discovery Service Running on  " + port);
}

exports.set_stbs_reference = function (endpoint_stbs) {
    stbs = endpoint_stbs;
}


exports.init = function (enc) {
    encode = enc;
    registerClient("1234567890");

    try {
        var con = mysql.createConnection({
            host: "172.18.129.66",
            user: "bridge",
            password: "aogrules!",
            database: "authdb"
        });

        con.connect(function (err) {
            try {
                con.query("SELECT smart_card FROM sv_smartbox_identities", function (err, result, fields) {
                    try {
                        if (result.length > 0) {
                            for (var i = 0; i < result.length; i++) {
                                registerClient(result[i].smart_card, true);
                                console.log("[Discovery] Registering : " + result[i].smart_card);
                            }
                        }
                    } catch (err) {
                        console.log("[Discovery] Initialization DB Error");
                    }

                });
            } catch (err) {
                console.log("[Discovery] Initialization DB Error");
            }

        });
    } catch (e) {
        console.log("[Discovery] Initialization DB Error");
    }

}
