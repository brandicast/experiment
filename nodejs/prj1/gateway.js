const io = require ('socket.io-client') ('https://io.luffanet.com.tw?token=token');
var linebot = require('linebot');
 var bot = linebot({
  channelId: 1617614710,
  channelSecret: 'secret',
  channelAccessToken: 'token'
});

var user_id_array = ['U17f3c29570cb4be181aa7e82b86b3ba7'];
var mute = false ;
var period = 60000 * 60 * 3;

io.on ('connect', function(){
	 console.log ('connected', io.id); 
});

io.on('data', function (data) {
    console.log ('0) event', io.id, data);
    var msg = filter_philio_data(data) ;
    console.log ("4) msg.length = " + msg.length) ;
    if ((msg.length > 0) && !mute)
        bot.push(user_id_array, msg);
})


var last_record =  {"temp":0, "lumin":0, "door":0, "temp_timestamp":0, "lumin_timestamp":0, "door_timestamp":0} ;
var funcType = {11:"Temperature Sensor", 12:"Illumination Sensor", 13:"Door / Window Sensor",  14:"PIR Sensor", 23:"Switch"} ;
var eventCode = {0: "沒資料 !", 4001:"Tamper trigger", 4002:"Low battery", 4101:"PIR Trigger",  4102:"Door/Window Open", 4103:"Door/Window Close", 4801:"Temperature Report", 4802:"Illumination report", 4804:"Meter report", 5002:"Status update"};

function filter_philio_data (x){
    var message = "" ;

    if (x.eventlog)
    {
        var now = Date.now() ;

        switch (x.eventlog.funcType){
            case 11 : {
                last_record.temp = ((x.eventlog.dataUnit ==1) ? x.eventlog.sensorValue * 0.1 : (x.eventlog.sensorValue * 0.1-30 ) /2) ;
                last_record.temp_timestamp = now ;
                break ;
            }
            case 12 :  {            
                last_record.lumin = x.eventlog.sensorValue; 
                last_record.lumin_timestamp = now ;
                break ;
            }   
            case 0 : {
                if (x.eventlog.eventCode == 4003){
                    message = "" ;
                    break
                }
            }
            case 13 : {
                message = x.eventlog.uid + ":" +  "(" + x.eventlog.eventCode + ")" + eventCode[x.eventlog.eventCode] ;  
                last_record.door = x.eventlog.eventCode ;
                last_record.door_timestamp = now ;
                break ;
            }
            case 14 : {
                message = x.eventlog.uid + ":" +  "(" + x.eventlog.eventCode + ")" + eventCode[x.eventlog.eventCode] ;  
                break ; 
            
            }
         }
    }
    return message ;
}



/*
bot.on('message', function (event) {
  event.reply(event.message.text).then(function (data) {
     console.log (event.message.text) ;
     switch (event.message.text) {
         case "(current_temp)": {
             bot.push (event.source.userId, "現在溫度 : "  + last_record.temp) ;
             break ;
         }
         case "(current_lumin)": {
            bot.push (event.source.userId, "現在亮度 : "  + last_record.lumin) ;
            break ;
         }
         default : {
            bot.push (event.source.userId, "echo : " + event.message.text) ;
            break ;
        }
    }
  }).catch(function (error) {
    console.log ('Error' + error) ;
  });
});
 */


bot.on('message', function (event) {
       switch (event.message.text) {
            case "(STATUS)": {
            event.reply ("現在溫度 : " + last_record.temp + ", 現在亮度 :" + last_record.lumin + ", 門窗 :" + eventCode[last_record.door] + ", 靜音模式 :" +(mute?"啟動":"關閉"));
               break ;
           }
           case "(current_temp)": {
               event.reply ("現在溫度 : "  + last_record.temp) ;
               break ;
           }
           case "(current_lumin)": {
              event.reply ("現在亮度 : "  + last_record.lumin) ;
              break ;
           }
           case "(MUTE)" :{
               mute = !mute ;
               var mode = mute?"啟動":"關閉" ;
               event.reply ("靜音模式 : " + mode) ;
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
    console.log(event) ;http://book.mixu.net/node/ch6.htmlhttp://book.mixu.net/node/ch6.html
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
    var sendMsg = '您好，我準備為您即時回報 !' ;
    bot.push(user_id_array,sendMsg);
    console.log('send: '+user_id_array + ':' + sendMsg);
},3000);

setInterval(function(){
    if (!mute)
        bot.push (user_id_array, "現在溫度 : " + last_record.temp + ", 現在亮度 :" + last_record.lumin + ", 門窗 :" + eventCode[last_record.door]) ;
},period)