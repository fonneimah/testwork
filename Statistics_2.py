import requests, json, re

def totalCount(r):
	header = r.rpartition('&')
	s_regex = re.compile(r'\d+')
	needed_s = s_regex.search(header[2])
	result = needed_s.group()
	return result

open_pulls = requests.get('https://api.github.com/repos/googlechrome/puppeteer/pulls?state=open&per_page=1')
closed_pulls = requests.get('https://api.github.com/repos/googlechrome/puppeteer/pulls?state=closed&per_page=1')
print("Total open pulls: %s" %(totalCount(open_pulls.headers['Link'])))
print("Total closed pulls: %s" %(totalCount(closed_pulls.headers['Link'])))

ans = requests.get('https://api.github.com/repos/googlechrome/puppeteer')
regex = re.compile(r'("open_issues_count":)(\d+)')
data = regex.search(ans.text)
open_issues_count = data.group(2)
print("Open issues count: %s" % (open_issues_count))