import requests, re, datetime

now = datetime.datetime.now()
old_issnum = 0

def deltatime(targettime, duration):
	regexp = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
	rawstr = regexp.search(targettime)
	then = datetime.datetime(int(rawstr.group(1)), int(rawstr.group(2)), int(rawstr.group(3)))
	delta = now - then
	return (True if delta.days >= duration else False)

old_issues = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:open&sort=created&per_page=100')
regexp = re.compile(r'page=(\d+)>;\srel="last"')
rawexp = regexp.search(old_issues.headers['Link'])
lastpage = int(rawexp.group(1))
for i in range(1, (lastpage + 1)):
	data = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:open&sort=created&per_page=100&page=%d'%(i)).json()['items']
	old_issnum = old_issnum + sum(list(map(lambda x: deltatime(x['created_at'], 14), data)))
print("Old issues count: %d"%(old_issnum))