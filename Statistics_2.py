import requests, re

def totalCount(r):
	regex = re.compile(r'("total_count":)(\d+)')
	data = regex.search(r)
	count = data.group(2)
	return count

open_pull = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:pr+state:open')
closed_pull = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:pr+state:closed')
open_issues = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:open')
closed_issues = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:closed')

print("Total open pulls: %s\nTotal closed pulls: %s\nTotal open issues: %s\nTotal closed issues: %s" % (totalCount(open_pull.text), totalCount(closed_pull.text), totalCount(open_issues.text), totalCount(closed_issues.text)))
