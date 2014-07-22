#!/usr/bin/env python

# system dependencies
import utils
import glob
import os
import json

# third party dependencies
from elasticsearch import Elasticsearch

# localhost:9200 by default
# uses index 'foia', to load 'documents' mapping run
#   curl -XPUT "http://localhost:9200/foia/_mapping/documents" -d "@config/mappings/documents.json"
es = Elasticsearch()
index = 'foia'
mapping = 'documents'

# options:
#   limit: cut off after X documents

def run(options):
  limit = options.get("limit")
  start = options.get("start")

  i = 0
  missing = 0

  doc_paths = glob.glob("data/state/*/*")
  doc_paths.sort()

  if start:
    doc_paths = doc_paths[(int(start)-1):-1]
  if limit:
    doc_paths = doc_paths[0:(int(limit))]

  # each one is e.g. 'data/state/0139/DOCUMENTS-StateChile3-00008305'
  for doc_path in doc_paths:
    json_path = os.path.join(doc_path, "document.json")
    metadata = json.load(open(json_path))

    # RSS-type fields that might easily be common across agencies
    document_id = metadata["document_id"]
    document = {
      "document_id": document_id,
      "url": metadata['url'],
      "title": metadata['subject'],
      "source": "state"
    }

    # State docs don't always have a postedDate - research should be done
    # to identify the correct posted date for individual tranches, but
    # for now, just fall back to its creation date.
    document["published_on"] = metadata['postedDate'] or metadata['docDate']

    # include anything else as State-specific extra data
    document["state"] = metadata

    # the full text
    text_path = os.path.join(doc_path, "document.txt")
    if os.path.exists(text_path):
      text = open(text_path).read()
      document["text"] = text
    else:
      print("[%s] NO TEXT ON DISK." % document_id)
      missing += 1

    # throw it in elasticsearch
    print("[%i][%s] Loading into elasticsearch." % (i, document_id))
    es.index(index=index, doc_type=mapping, id=document_id, body=document)
    i += 1

    if limit and (i > int(limit)):
      break

  print("Okay, loaded %i documents into Elasticsearch." % i)
  print("Missing text on disk: %i" % missing)

  # reload the index
  es.indices.refresh()

run(utils.options()) if (__name__ == "__main__") else None