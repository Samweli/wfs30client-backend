from flask import Flask, url_for, json, request
app = Flask(__name__)
import requests
import os
import subprocess

from test import *

wfs_server = "http://localhost:9000"
ldproxy = "https://www.ldproxy.nrw.de/kataster/?f=json"


# Routes

# WFS 3.0  Requirement 5
# WFS 3.0  Requirement 6
@app.route("/")
def main():
    server = request.args.get('server')
    endpoint = server
    response = test_conformity('content.json', endpoint)
    return response

# WFS 3.0 Requirement 30
@app.route("/api", endpoint='api')
def api():
	
	server = request.args.get('server')
	endpoint = server + "/api"
	response = generic_api_test('api.json', endpoint)
	return response

# WFS 3.0 Requirement 2
# WFS 3.0 Requirement 3
@app.route("/api/conformance", endpoint='api/conformance')
def api_conformance():
	
	server = request.args.get('server')
	endpoint = server + "/api/conformance"
	response = test_conformity('req_classes.json', endpoint)
	return response


# WFS 3.0 Requirement 7
@app.route("/links")
def links():
	
	server = request.args.get('server')
	endpoint = server
	response = test_conformity_links('link.json', endpoint)
	return response

# WFS 3.0 Requirement 4
@app.route("/http1.1", endpoint='http')
def http():
    
    server = request.args.get('server')
    response = test_http_conformity(server, "HTTP/1.1")
    return response

# WFS 3.0 Recommendation 2
@app.route("/etag", endpoint='etag')
def etag():
    
    server = request.args.get('server')
    response = test_http_conformity(server, 'Etag')
    return response


if __name__ == "__main__":
    app.run()