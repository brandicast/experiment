// subscriber_binary.js
const mqtt = require('mqtt');
const fs = require('fs');

const client = mqtt.connect('mqtt://172.28.248.138', { port: 1883 });

client.on('connect', () => {
  console.log ('Connected to MQTT broker') ;
  client.subscribe('test/binary', (err) => {
    if (err) console.error('Subscribe error:', err);
  });
});

client.on('message', (topic, message) => {
  // message 是 Buffer（Node.js 的二进制数据类型）
  console.log(`Received ${message.length} bytes`);
  
  // 保存为文件
  fs.writeFileSync('received.bmp', message);
  console.log('Saved to received.png');
  
  client.end();
});

