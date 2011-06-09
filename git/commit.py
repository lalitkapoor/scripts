from suds.client import Client
from suds import WebFault
import re
import logging
import sys
#app specific
import settings
import config

logging.basicConfig(level=logging.ERROR, filename='jira.log', format='%(asctime)s %(levelname)s\n%(message)s\n\n')
client = Client(config.wsdl)
auth = client.service.login(config.username, config.password)

f = open(sys.argv[1], 'r')
comment = f.read()
f.close()

regex = r"\%s\w*[!-~]*\d*" % (settings.prefix)
matches = re.findall(regex, comment)

commands = set()
issueIDs = set()

for match in matches:
	match = match[1:].upper() #remove the hash and make it all uppercase
	if match in settings.commands:
		print "command found:", match
		commands.add(match)
		#do something here, act on the command
		#do this when the push has completed
	else:
		print "potential JIRA issue:", match
		#this might be an issue so add to list of issues
		issueIDs.add(match)

#check to make sure all issues specified exist:
for issueID in issueIDs:
	issue = None
	
	try:
		issue = client.service.getIssue(auth, issueID)
		print "JIRA issue found:", issueID
	except WebFault as err:
		print "Error finding JIRA issue:", (issueID)
		exit(1) #exit because, if there are errors we don't want to commit

exit(0)

#do this only when the github hook calls us on a successful git push	
for issueID in issueIDs:
	print "adding comment for JIRA issue:", issueID
	client.service.addComment(auth, issueID, {'body': comment})