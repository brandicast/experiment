var mqtt  = require ('mqtt');
var opt =  {
    port:1883,
    clientId: 'nodejs-8F'
};

var client = mqtt.connect ('mqtt://192.168.0.17', opt);

client.on ('connect', function ()  {
    console.log ('Connected to MQTT broker') ;
    //client.subscribe ('brandon/iot_command') ;
}
);

client.on ('message', function (topic, msg){
    console.log ('Receiving from [' + topic + '] with message : ' + msg)
});


client.publish("brandon/iot/command", "(STATUS)")