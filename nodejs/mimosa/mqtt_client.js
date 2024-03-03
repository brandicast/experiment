var mqtt  = require ('mqtt');
var opt =  {
    port:1883,
    clientId: 'nodejs'
};

var client = mqtt.connect ('mqtt://192.168.0.120', opt);




exports.publish  = function (topic, msg) {
        client.publish("brandon/test", msg); 
}
