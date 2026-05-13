var mqtt  = require ('mqtt');
var opt =  {
    port:1883,
    clientId: 'bman'
};

var client = mqtt.connect ('mqtt://172.28.248.138', opt);

client.on ('connect', function ()  {
    console.log ('Connected to MQTT broker') ;
    client.subscribe ('brandon/epaper/text') ;
}
);

client.on ('message', function (topic, msg){
    console.log ('Receiving from [' + topic + '] with message : ' + msg)
});


