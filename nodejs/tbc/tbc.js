
var linebot = require('linebot');
 var bot = linebot({
  channelId: 1619180638,
  channelSecret: 'secret',
  channelAccessToken: 'token'
});

var http = require ('http') ;
var mute = false ;

var user_id_array = ['U17f3c29570cb4be181aa7e82b86b3ba7', 'Ua4fb37520ce928e81b4f03cb72848b9a',];

bot.on('message', function (event) {
       switch (event.message.text) {
            case "(CHANNEL Up)": {
                http.get ('http://61.219.181.31:8088/channelUp') ;
                event.reply ('上一台');
                console.log ('上一台') ;
               break ;
           }
           case "(CHANNEL Down)": {
               event.reply ('下一台') ;
               http.get ('http://61.219.181.31:8088/channelDown') ;
               console.log ('下一台') ;
               break ;
           }
           case "(VOLUME Up)": {
              event.reply ('音量變大') ;
              http.get ('http://61.219.181.31:8088/volumeUp') ;
              console.log ('音量變大') ;
              break ;
           }
           case "(VOLUME Down)": {
            event.reply ('音量變小') ;
            http.get ('http://61.219.181.31:8088/volumeDown') ;
            console.log ('音量變小') ;
            break ;
         }
           case "(MUTE)" :{
               mute = !mute ;
               var mode = mute?"啟動":"關閉" ;
               event.reply ("靜音模式 : " + mode) ;
               http.get ('http://61.219.181.31:8088/mute') ;
               console.log ('靜音') ;
               break ;
           }
           case "(EXIT)": {
                event.reply ("服務停止....1分鐘後，自動啟動!") ;
                setTimeout(function(){
                    process.exit(0)}, 5000) ;
                break ;
           }
           default : {
            event.reply("echo :" + event.message.text) ;
              break ;
          }
      }});
  

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
console.log ('系統啟動 !') ;
