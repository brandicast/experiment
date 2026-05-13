// publisher_binary.js
const mqtt = require('mqtt');
const fs = require('fs');

const client = mqtt.connect('mqtt://172.28.248.138', { port: 1883 });

client.on('connect', () => {
  // 读取图片文件
  const imageBuffer = fs.readFileSync('1.bmp');
  
  client.publish('test/binary', imageBuffer, (err) => {
    if (err) {
      console.error('Publish error:', err);
    } else {
      console.log(`Published ${imageBuffer.length} bytes of binary data`);
    }
    client.end();
  });
});

