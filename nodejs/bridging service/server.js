let end_point_service = require("./endpoint.js");
let discovery_service = require("./discovery.js");

const DISCOVERY_PORT = 8080;
const ENDPOINT_PORT = 9999;

discovery_service.set_stbs_reference(end_point_service.get_connected_stbs);
discovery_service.init();

discovery_service.start(DISCOVERY_PORT);

setTimeout(function () {
    end_point_service.start(ENDPOINT_PORT)
}, 3000);