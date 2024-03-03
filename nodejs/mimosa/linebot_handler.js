
const log4js = require("log4js");
const logger =  log4js.getLogger("LineBot_Handler") ;

let linebot = require('linebot');
let bot =  linebot({
    channelId: 123,
    channelSecret: 'secret',
    channelAccessToken: 'token'
  });
  let config = require ("./config.js") ;

  var  notifier =  null ;
  var  database = null ;
  
  var user_id_array = ['U17f3c29570cb4be181aa7e82b86b3ba7'] ;

  bot.on('message', function (event) {
    switch (event.message.text) {
         case "(STATUS)": {
            let msg = "" ;
            if (database)
                   msg = JSON.stringify (database) ;
             if (notifier)  
                 notifier.sendMessageToAll (msg) ;
             else 
                event.reply (msg);          
            break ;
        }
        default : {
            if (notifier) 
                notifier.sendMessageToAll (msg) ;
            else 
                event.reply("echo :" + event.message.text) ;
           break ;
       }
   }});


   bot.on ('leave', function(event){
    logger.debug(event) ;
    var index = user_id_array.indexOf(event.source.userId) ;
    if (index > 0)
        user_id_array.splice(index,1) ;
})

bot.on ('join', function(event){
    logger.debug(event) ;
    user_id_array.push(event.source.userId) ;
    event.reply ("http://192.168.0.18:8888/") ;
})

bot.on ('follow', function(event){
    logger.debug(event) ;
    user_id_array.push(event.source.userId) ;
    event.reply ("http://192.168.0.18:8888/") ;
})

bot.on ('unfollow', function(event){
    logger.debug(event) ;
    var index = user_id_array.indexOf(event.source.userId) ;
    if (index > 0)
        user_id_array.splice(index,1) ;
})


setTimeout(function(){
    var sendMsg = '您好，我準備為您即時回報 !' ;
    bot.push(user_id_array,sendMsg);
    logger.info('send: '+user_id_array + ':' + sendMsg);
},3000);

bot.listen('/', config.line_bot.port);



exports.setNotifier = function (nf) {
    notifier = nf ;
}

exports.setInfoDatabase = function (db) {
    database = db ;
}

