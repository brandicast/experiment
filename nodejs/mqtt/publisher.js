var mqtt  = require ('mqtt');
var opt =  {
    port:1883,
    clientId: 'publisher'
};

var client = mqtt.connect ('mqtt://192.168.68.57', opt);
var topic = "brandon/iot/pico/gate"

client.on('connect', () => {
    client.publish(topic, 'OPEN', (error) => {
      if (error) {
        console.error(error)
      }
    })

    client.end()
  })


