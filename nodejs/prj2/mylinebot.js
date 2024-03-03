var linebot = require('linebot');
 
var bot = linebot({
  channelId: 1617614710,
  channelSecret: 'secret',
  channelAccessToken: 'token'
});
 
var text_msg = '有人發訊喔 !'; 

var brandon_user_id = 'U17f3c29570cb4be181aa7e82b86b3ba7' ;

var user_id_array = ['U17f3c29570cb4be181aa7e82b86b3ba7'];

bot.on('message', function (event) {
  event.reply(event.message.text).then(function (data) {
  bot.push(user_id_array, text_msg) ;
  }).catch(function (error) {
    console.log ('Error' + error) ;
  });
});
 
bot.on ('leave', function(event){
    console.log(event) ;
    var index = user_id_array.indexOf(event.source.userId) ;
    if (index > 0)
        user_id_array.splice(index,1) ;
})

bot.on ('join', function(event){
    console.log(event) ;
    user_id_array.push(event.source.userId) ;
})

bot.on ('follow', function(event){
    console.log(event) ;
    user_id_array.push(event.source.userId) ;
})

bot.on ('unfollow', function(event){
    console.log(event) ;
    var index = user_id_array.indexOf(event.source.userId) ;
    if (index > 0)
        user_id_array.splice(index,1) ;
})

bot.listen('/', 9999);

setTimeout(function(){
    //var sendMsg = text_msg ;
    var sendMsg = '您好，我準備為您定時回報 !' ;
    bot.push(user_id_array,sendMsg);
    console.log('send: '+user_id_array + ':' + sendMsg);
},3000);
