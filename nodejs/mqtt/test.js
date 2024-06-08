var mqtt  = require ('mqtt');
var opt =  {
    port:1883,
    clientId: 'bman'
};

var client = mqtt.connect ('mqtt://192.168.68.57', opt);

client.on ('connect', function ()  {
    console.log ('Connected to MQTT broker') ;
    client.subscribe ('brandon/iot/pico/gate') ;
}
);

client.on ('message', function (topic, msg){
    console.log ('Receiving from [' + topic + '] with message : ' + msg)
});


