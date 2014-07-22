
var es = require("./config/environment").es;

module.exports = {

  index: function(req, res) {
    res.send("Hello world!");
  },


  /*
    Real basic search API over anything that's been loaded.
    Searches over 'title' and 'text' fields, returns highlighted
    matches. Accepts 'page' and 'per_page' arguments.
  */

  search: function(req, res) {
    var query = req.param("query") || "*";
    var page = parseInt((req.param("page") || 1));
    var per_page = parseInt(req.param("per_page") || 10);

    search(query, page, per_page).then(function(results) {

      res
        .set("Content-Type", "application/json")
        .send(responseFor(results, query, page, per_page));

    }, function(err) {
      console.log("Noooo!");
      res.status(500).send(err.toString());
    })
  }

};

// map ES response format to API response format
function responseFor(results, query, page, per_page) {
  var response = {
    results: [],
    meta: {
      query: query,
      page: {
        page: page,
        per_page: per_page,
        count: results.hits.hits.length
      },
      count: results.hits.total
    }
  };
  results.hits.hits.forEach(function(hit) {
    var result = hit._source;
    result.highlight = hit.highlight;
    response.results.push(result);
  });

  return response;
}


function search(query, page) {
  var per_page = 10;
  var from = (page - 1) * per_page;

  return es.search({
    index: 'foia',
    type: 'documents',
    body: {
      "from": from,
      "size": per_page,
      "query": {
        "filtered": {
          "query": {
            "query_string": {
            "query": query,
            "default_operator": "AND",
            "use_dis_max": true,
            "fields": ["text", "title"]
            }
          }
        }
      },
      "sort": [{
        "published_on": "desc"
      }],
      "highlight": {
        "fields": {
          "*": {}
        }
      },
      "_source": ["document_id", "url", "title", "published_on", "state"]
    }
  });
}
