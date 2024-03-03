let line = require ("./line_notify.js") ;

exports.sendMessageToAll  = function (message) {
    line.sendMessageToAll (message) ;
}

exports.setInfoDatabase  = function (db) {
    line.setInfoDatabase (db) ;
}