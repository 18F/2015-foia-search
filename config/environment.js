
// establish an app-wide connection to elasticsearch
var elasticsearch = require("elasticsearch"),
    es = new elasticsearch.Client({log: 'trace'});

module.exports = {es: es}