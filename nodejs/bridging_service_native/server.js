let discovery_service = require("./discovery.js");
let end_point_service = require("./endpoint.js");
let sync_service  = require ("./sync.js") ;

const DISCOVERY_PORT = 8080;
const ENDPOINT_PORT = 8001;
var enc = 0;
let sleep_time = 3000;



async function start() {
    discovery_service.set_stbs_reference(end_point_service.get_connected_stbs);
    discovery_service.init(enc);
    end_point_service.init(enc);

    discovery_service.start(DISCOVERY_PORT);
    sync_service.start (); 
    await sleep(sleep_time);
    end_point_service.start(ENDPOINT_PORT)
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

try {
    start();

    //setInterval (sync_service.broadcast ("Hi !"), 5000) ;
    setInterval (()=> {sync_service.broadcast ("Hi !");}, 5000) ;

} catch (e) {
    console.log("[Serice] Something didn't catch : " + e);
}

