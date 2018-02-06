import requests, re, datetime

now = datetime.datetime.now()
old_issnum = 0

def deltatime(targettime, duration):
	regexp = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
	rawstr = regexp.search(targettime)
	then = datetime.datetime(int(rawstr.group(1)), int(rawstr.group(2)), int(rawstr.group(3)))
	delta = now - then
	return delta

old_issues = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+created%3A%3C' + '2018-01-24' + '+state%3Aopen+is%3Aissue').json()['total_count']
print(old_issues)