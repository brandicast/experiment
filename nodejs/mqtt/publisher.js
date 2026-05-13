var mqtt  = require ('mqtt');
var opt =  {
    port:1883,
    clientId: 'publisher'
};

var client = mqtt.connect ('mqtt://172.28.248.138', opt);
var topic = "brandon/epaper/text"

client.on('connect', () => {
    client.publish(topic, 'OPEN', (error) => {
      if (error) {
        console.error(error)
      }
    })

    client.end()
  })


