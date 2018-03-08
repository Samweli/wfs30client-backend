import json
import requests
import os
import subprocess

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