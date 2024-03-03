const express = require("express");
const proxy = require("express-http-proxy");
const PORT = 8080;

const app = express();

app.use("/pages", express.static("pages"));
app.use("/", proxy("61.31.169.128"));

app.listen(PORT);

console.log("Server running on " + PORT);