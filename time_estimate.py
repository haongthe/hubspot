from jira import JIRA
import flask
from flask import Flask, abort, redirect, url_for
app = Flask(__name__)

@app.route('/')
def process():
	jira_options = {'server': 'https://topkidjira.topica.vn'}
	jira = JIRA(options = jira_options, basic_auth = ('thehao5297','thehao5297'))
	while True:    
		issues = jira.search_issues('issue = WOR')
		last_status = None
		for issue in issues:
			status = issue.fields.status
			if status != last_status:
				if str(status) == 'HL01':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 5d 12h'}}]})
				elif str(status) == 'HL02':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 4d 12h'}}]})
				elif str(status) == 'HL02 VER 1.0 IN REVIEW':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 3d 12h'}}]})
				elif str(status) == 'HL02 VER 2.0':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 3d'}}]})
				elif str(status) == 'HL02 VER 3.0':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 2d 12h'}}]})
				elif str(status) == 'HL03 VER 1.0':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 1d 12h'}}]})
				elif str(status) == 'HL03 VER 2.0':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '6d 12h'}}]})
				elif str(status) == 'HL04 IN REVIEW':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '4d 12h'}}]}) 
				elif str(status) == 'HL04':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '3d 12h'}}]})
				elif str(status) == 'HL05 IN REVIEW':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '2d 12h'}}]})
				elif str(status) == 'HL05 DONE':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1d 12h'}}]})
				elif str(status) == 'HL06':
					issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1d'}}]})
				else:
				    print("unknown status, status -> {}".format(status))
			last_status = status
if __name__ == "__main__":
	app.run(port = 9797)
