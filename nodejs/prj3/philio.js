
var funcType = {11:"Temperature Sensor", 12:"Illumination Sensor", 13:"Door / Window Sensor",  14:"PIR Sensor"} ;
var eventCode =  {4001:"Tamper trigger", 4002:"Low battery"}; 

var text = {"eventlog":{"Dim_ON_Value":255,"basicValue":0,"battery":255,"channelID":0,"dataUnit":5,"eventCode":4804,"funcName":"Wall Switch","funcType":22,"meter":{"current":0,"kwh":52,"pf":0,"voltage":0,"watt":0},"productCode":16843048,"sensorValue":0,"sequence":1821,"timeStamp":1540643330,"uid":260},"mac":"18CC23004AB4"}
var door = {"eventlog":{"Dim_ON_Value":0,"basicValue":255,"battery":100,"channelID":13,"dataUnit":0,"eventCode":4102,"funcName":"Door / Window Sensor","funcType":13,"productCode":16843276,"sensorValue":0,"sequence":1805,"timeStamp":1540641117,"uid":259},"mac":"18CC23004AB4"} ;

//var j = JSON.parse(text); 
var j = door ;
console.log (j.eventlog.eventCode) ; 
console.log (funcType[12]) ;

