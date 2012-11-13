var express = require("express");
var fs = require("fs");
var app = express();

//app.use(express.errorHandler());
app.use(express.logger('dev'));

app.get("/cache.manifest", function(req, res){
  fs.readFile('cache.manifest', 'utf8', function (err, data) {
    res.set("Content-Type", "text/cache-manifest");
    res.send(data.toString());
  });
});

app.get("/index.html", function(req, res){
  fs.readFile('index.html', 'utf8', function (err, data) {
    res.set('Content-Type', 'text/html');
    res.send(data.toString());
  });
});

app.get("/jquery.min.js", function(req, res){
  fs.readFile('jquery.min.js', 'utf8', function (err, data) {
    res.set("Content-Type", "text/javascript");
    res.send(data.toString());
  });
});


app.listen(8080);
console.log('listening on 8080');