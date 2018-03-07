from flask import Flask, url_for, json, request
app = Flask(__name__)
import requests
import os
import subprocess

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

# WFS 3.0 Requirement 7
@app.route("/links")
def links():
	
	server = request.args.get('server')
	endpoint = server
	response = test_conformity_links('link.json', endpoint)
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
	response = test_conformity('req-classes.json', endpoint)
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



 # Tests
def showjson(file):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "main", file)
    data = json.load(open(json_url))

    return data

def test_conformity(file, endpoint):
	result = requests.get(endpoint)

	root = showjson(file)
	required = root['required']
	required = [str(i) for i in required]
	j_result = json.loads(result.text);

	expected = set(required)
	response = set((j_result.keys()))

	if result.status_code == 200:
		if expected == response:
			out = 'Valid endpoint'
		else:
			difference = expected - response;
			out = "{'text': 'Invalid endpoint', missing_required: '"+ str(list(difference)) +"}'}"
	else:
		out = 'Wrong HTTP status code in the endpoint'

	return out

def test_conformity_links(file, endpoint):
	result = requests.get(endpoint)

	root = showjson(file)
	try:
		ref = root
		j_result = json.loads(result.text)['properties']['links']['items']['$ref'];

		expected = set(ref)
		response = set(j_result)
		print expected

		if result.status_code == 200:
			if expected == response:
				out = 'Valid endpoint'
			else:
				difference = expected - response;
				out = "{'text': 'Invalid endpoint', missing_required: '"+ str(list(difference)) +"}'}"
		else:
			out = 'Wrong HTTP status code in the endpoint'
	except:
		out = "Invalid"
	return out

def generic_api_test(file, endpoint):
	result = requests.get(endpoint)

	root = showjson(file)
	j_result = json.loads(result.text);

	expected = set(root.keys())
	response = set(j_result.keys())

	if result.status_code == 200:
		if expected == response:
			required_path = set(required['paths'])
			j_result_path = set(j_result['paths'])
			if required_path ==  j_result_path:
				out = 'Valid endpoint'
			else:
				path_difference = required_path - j_result_path;
				out = "{'text': 'Invalid endpoint', missing_required: '"+ str(list(path_difference)) +"}'}"

		else:
			difference = expected - response;
			out = "{'text': 'Invalid endpoint', missing_required: '"+ str(list(difference)) +"}'}"
	else:
		out = 'Wrong HTTP status code in the endpoint'

	return out

def test_http_conformity(server, value):
	response = subprocess.check_output(['curl', '--head', server])

	if value in response:
		out = 'Valid'
	else:
		out = 'Invalid'

	return out


if __name__ == "__main__":
    app.run()