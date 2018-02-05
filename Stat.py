import requests, re, datetime

now = datetime.datetime.now()
old_issnum = 0

def totalCount(r):
	regex = re.compile(r'("total_count":)(\d+)')
	data = regex.search(r)
	count = data.group(2)
	return count

def deltatime(targettime, duration):
	regexp = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
	rawstr = regexp.search(targettime)
	then = datetime.datetime(int(rawstr.group(1)), int(rawstr.group(2)), int(rawstr.group(3)))
	delta = now - then
	return (True if delta.days >= duration else False)

def getPage(reponse):
	regexp = re.compile(r'page=(\d+)>;\srel="last"')
	rawexp = regexp.search(response)
	return rawexp.group(1)

raw = list(map(lambda x: (x['author']['login'], x['total']), requests.get('https://api.github.com/repos/googlechrome/puppeteer/stats/contributors').json()))
top30 = raw[::-1][:30]
print('+' + ('-'*22) + '+' + ('-'*22) + '+')
print('|' + (' '*9) + 'LOGIN' + (' '*8) + '|' + (' '*7) + 'COMMITS' + (' '*8) + '|')
print('+' + ('-'*22) + '+' + ('-'*22) + '+')
for k in range(len(top30)):
		print('\t' + top30[k][0] + '\t\t\t' + str(top30[k][1])) if len(top30[k][0]) <= 7 else print('\t' + top30[k][0] + '\t\t' + str(top30[k][1]))

open_pull = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:pr+state:open')
closed_pull = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:pr+state:closed')
open_issues = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:open')
closed_issues = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:closed')

print("Total open pulls: %s\nTotal closed pulls: %s\nTotal open issues: %s\nTotal closed issues: %s" % (totalCount(open_pull.text), totalCount(closed_pull.text), totalCount(open_issues.text), totalCount(closed_issues.text)))

old_issues = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:open&sort=created&per_page=100')
lastpage = int(getPage(old_issues.headers['Link']))

for i in range(1, (lastpage + 1)):
	data = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:open&sort=created&per_page=100&page=%d'%(i)).json()['items']
	old_issnum = old_issnum + sum(list(map(lambda x: deltatime(x['created_at'], 14), data)))
print("Old issues count: %d"%(old_issnum))