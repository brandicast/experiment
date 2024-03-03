const PORT = process.env.PORT || 9999;
var linebot = require('linebot');
var bot = linebot({
    channelId: 12345678,
    channelSecret: '',
    channelAccessToken: ''
});

var user_id_array = ['U17f3c29570cb4be181aa7e82b86b3ba7']; 


bot.on('message', function (event) {
    event.reply("echo :" + event.message.text);

});


bot.on('leave', function (event) {
    console.log(event);
    var index = user_id_array.indexOf(event.source.userId);
    if (index > 0)
        user_id_array.splice(index, 1);
})

bot.on('join', function (event) {
    console.log(event);
    user_id_array.push(event.source.userId);
})

bot.on('follow', function (event) {
    console.log(event);
    user_id_array.push(event.source.userId);
})

bot.on('unfollow', function (event) {
    console.log(event);
    var index = user_id_array.indexOf(event.source.userId);
    if (index > 0)
        user_id_array.splice(index, 1);
})
bot.listen('/', PORT);

setTimeout(function () {
    //var sendMsg = text_msg ;
    var sendMsg = '您好，我準備為您即時回報 !';
    bot.push(user_id_array, sendMsg);
    console.log('send: ' + user_id_array + ':' + sendMsg);
}, 3000);