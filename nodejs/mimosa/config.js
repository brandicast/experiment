module.exports = {
    line_notify : {
        client_id  :  '' ,
        client_secret : '', 
        redirect_uri : 'http://192.168.0.120:8888/code_receiver',
        success_page : '/home/brandon/Dropbox/workbench/nodejs/Personal/mimosa/LineNotify/success.html'  , 
        token_file : "./token_list.json" , 
        port : 8888
    }, 
    gateway : {
        port : 9613 
    }, 
    line_bot: {
        port : 9999,
        channelId: 123456,
        channelSecret: '',
        channelAccessToken: ''  ,
        user_id_file : './user_id.json' , 
        notify_uri : 'http://192.168.0.120:8888/'
    },
    log4js_set: {
        appenders: {
                out: {
                        type: 'console'
                },
                app: {
                        type: 'file',
                        filename: 'logs/mimosa',
                        maxLogSize: 4096000,
                        backups: 9
                }
        },
        categories: {
                default: {
                        appenders: ['out', 'app'],
                        level: 'debug'
                }
        }
}

}