var routes = require("./routes");

var express = require('express');
var app = express();

// environment and port
var env = process.env.NODE_ENV || 'development';
var port = parseInt(process.argv[2], 10);
if (isNaN(port)) port = 3000;

// app middleware/settings
app.enable('trust proxy')
  .use(express.static(__dirname + '/public'));

// development vs production
if (env == "development")
  app.use(require('errorhandler')({dumpExceptions: true, showStack: true}))
else
  app.use(require('errorhandler')())


// helpers and routes
app.get('/', routes.index);


// boot it up!
app.listen(port, function() {
  console.log("Express server listening on port %s in %s mode", port, env);
});
