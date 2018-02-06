import requests, re, datetime

now = datetime.datetime.now()

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

def getPage(response):
	regexp = re.compile(r'page=(\d+)>;\srel="last"')
	rawexp = regexp.search(response)
	return int(rawexp.group(1))

raw = list(map(lambda x: (x['author']['login'], x['total']), requests.get('https://api.github.com/repos/googlechrome/puppeteer/stats/contributors').json()))
top30 = raw[::-1][:30]
print('+' + ('-'*22) + '+' + ('-'*22) + '+')
print('|' + (' '*9) + 'LOGIN' + (' '*8) + '|' + (' '*7) + 'COMMITS' + (' '*8) + '|')
print('+' + ('-'*22) + '+' + ('-'*22) + '+')
for k in range(len(top30)):
		print('\t' + top30[k][0] + '\t\t\t' + str(top30[k][1])) if len(top30[k][0]) <= 7 else print('\t' + top30[k][0] + '\t\t' + str(top30[k][1]))

print('+' + ('-'*20) + '+' + ('-'*20) + '+'+ ('-'*20) + '+' + ('-'*20) + '+')
print('|' + '  TOTAL OPEN PULLS  ' + '|' + ' TOTAL CLOSED PULLS ' + '|' + ' TOTAL OPEN ISSUES  ' + '|' + ' TOTAL CLOSED ISSUES' + '|')
print('+' + ('-'*20) + '+' + ('-'*20) + '+'+ ('-'*20) + '+' + ('-'*20) + '+')
print('\t' + totalCount(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:pr+state:open').text) + '\t'*3 +
	  totalCount(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:pr+state:closed').text) + '\t'*2 +
	  totalCount(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:open').text) + '\t'*3 +
	  totalCount(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:closed').text))

