from flask import Flask
from flask import request
from jira import JIRA
from MasterConfig import *
import http.client
http.client.HTTPConnection.debuglevel = 2

app = Flask(__name__)

@app.route('/jiramicroservice', methods=['POST','GET'])
def main():
	try:
		if request.method == 'GET':
			return 'Jira micro service GET call is successful.'
		else:
			_jsonreq = request.json
			project = _jsonreq['project']
			_summary = _jsonreq['summary']
			_description = _jsonreq['description']
			issuetype = _jsonreq['issuetype']
			_priority = _jsonreq['priority']

		auth_jira = JIRA(server=server, basic_auth=(username, password))
		new_issue = auth_jira.create_issue(project=project,summary=_summary,description=_description,issuetype=issuetype,priority=_priority)
		_issuedict = new_issue.raw
		return _issuedict['key']
	except Exception as e:
		return e.message

if __name__ == "__main__":
	app.run(host='172.31.0.167')