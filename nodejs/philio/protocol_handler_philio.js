/*const eventHandlers = {
    mac: data => {
        console.log('MAC:' + data);
      },
      eventLog: data => {
        console.log('===', 'Get a event \n', JSON.stringify(data));
        //
        // refer to Philio SDK to get more detail about event log.
        //
      },
      result: data => {
        console.log('===', 'Get a result \n', JSON.stringify(data));
      }
};

module.exports = Object.freeze (eventHandlers) ;
*/

var timestamp = Date.now () ;

exports.protocolHandler = function (json) {
  var msg = "" ;
  if ((json.mac) && (passEventFilter(json.eventLog[0]))){
    msg = "[" + timeStamp2String(parseInt(json.eventLog[0].timeStamp  + get3DigitsMilisString(json.eventLog[0].timeStamp_ms))) + "]  " 
    +  getDeviceMappingName(json.eventLog[0] )+ " : " 
    + getEventTranslation(json.eventLog[0]) ;
       console.log ( msg) ; 
       console.log (json.mac  + " : " + JSON.stringify (json.eventLog[0])) ; 
       console.log ("\n") ;
  }
  else if (json.result)   {  /*  Gateway request for AuthCode */
    // console.log ("[RESULT]") ;
    //  console.log (json.result.data) ;
    
    } 
    else {
      console.log ("[NOT HANDLED]") ;
      console.log (JSON.stringify(json)) ;
    }
    return msg  ;
};

function passEventFilter (event_obj) {
  let passed = false ;
  switch (event_obj.eventCode) {
    case 4002 : case 4101 :    case 4102 :  case 4103 :  case 5002 :{
      passed = true ;
        break ;
    }
    case 4801 : case 4802 :  {
    if ((Date.now() - timestamp) > (3 * 60 * 60 *1000))   {      // every 3 hour
              timestamp = Date.now() ; 
              passed  = true ;
    }
      break ;
    }
    case 4804 : {
      if ((Date.now() - timestamp) > (24 * 60 * 60 *1000))   {      // every day
        timestamp = Date.now() ; 
        passed  = true ;
      }
      break ;
    }
  }
  return passed ;
}

function getDeviceMappingName (event_obj)  {
   var name = "NoName" ;
   switch (event_obj.uid) {
     case 260 : {
        name = "外接插座" ;  
        break ;
     }
     case  264 : {
       name = "客廳牆壁內插座" ;
       break ;
     }
     case  267 : {  
       name =  "6F Sensor" ;
       break ;
     }
     case 268 : { 
       name = "5F Sensor" ;
       break ;
     }
     default : {
       name = event_obj.funcName ;
       break; 
     }
   }
   return name ;
  }

function getEventTranslation (event_obj) {
  
  var msg = "N/A" ;
  switch (event_obj.eventCode) {
    case 4002 : {
        msg = "Low Battery !" ;
        break ;
    }
    case 4003 : {
      msg = "Battery Change" ;
      msg += ": Battery Capacity = " + event_obj.battery ;
      break ;
  }
    case 4101 : {
      msg = "PIR Trigger" ;
      break; 
    }
    case 4102 : {
      msg = "Door Open" ;
      break ;
    }
    case 4103 : {
      msg = "Door Close" ;
      break ;
    }
    case 4801 : {
      msg = "Temperature";
      if  (event_obj.dataUnit == 2) 
        msg += ": " + (((event_obj.sensorValue * 0.1) - 32 ) * 5 / 9).toPrecision (3)  + "°C";
      break ;
    }
    case 4802 : {
      msg = "Illumination";
      msg  += ": " + event_obj.sensorValue  + "" + ((event_obj.dataUnit == 3) ?"%":" lux");
      break ;
    }
    case 4804 : {
      msg = "Meter";
      msg += ": " + JSON.stringify(event_obj.meter) ;
      break ;
    }
    case 5002 :  case 9999:  {
      msg = "Status Update" ;
      if (event_obj.funcType == 22) 
        msg += ": " + event_obj.funcName + " is " +  ( event_obj.basicValue  == 0?"Off":"On") ;
      break;
    }
    
  }
  return msg ;
}

function get3DigitsMilisString (ms) {
   var ms_string = ms + "" ;
   for (var i =0; i<3-ms_string.length;i++)
      ms_string = "0" + ms_string ;
    return ms_string ;
}

function timeStamp2String (time){
  var datetime = new Date();
   datetime.setTime(time);
   var year = datetime.getFullYear();
   var month = datetime.getMonth() + 1;
   var date = datetime.getDate();
   var hour = datetime.getHours();
   var minute = datetime.getMinutes();
   var second = datetime.getSeconds();
   var mseconds = datetime.getMilliseconds();
   //return year + "-" + month + "-" + date+" "+hour+":"+minute+":"+second+"."+mseconds;
   return year + "-" + month + "-" + date+" "+hour+":"+minute;
};
