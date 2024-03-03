var mdns = require('multicast-dns')()

const util = require('util');
 
mdns.on('response', function(response) {
  //console.log('got a response packet:', response)
})
 
mdns.on('query', function(query) {
  console.log('got a query packet:', util.inspect(query))
})
 
// lets query for an A record for 'brunhilde.local'
mdns.query({
  questions:[{
    name: 'DESKTOP-8F.local',
    type: 'A'
  }]
})