import requests, re, datetime, sys

repository = 'googlechrome/puppeteer'
branch = 'master'
print("Analyze: %s [%s branch]"%(repository, branch))

def recognize(date):
	regexp = re.compile(r'201[0-9]-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])')
	raw = regexp.search(date)
	if raw != None:
		return raw.group()
	else: return False

since = recognize(input('\nSINCE from which date repository should analyze.\nWARNING! FORMAT: YYYY-MM-DD\nSkip or error date transform to default value which is unlimited.\n'))
until = recognize(input('\nUNTIL till date repository should analyze.\nWARNING! FORMAT: YYYY-MM-DD\nSkip or error date transform to default value which is unlimited.\n'))

raw = list(map(lambda x: (x['author']['login'], x['total']), requests.get('https://api.github.com/repos/%s/stats/contributors'%(repository)).json()))
top30 = raw[::-1][:30]
print('+' + ('-'*22) + '+' + ('-'*22) + '+')
print('|' + (' '*9) + 'LOGIN' + (' '*8) + '|' + (' '*7) + 'COMMITS' + (' '*8) + '|')
print('+' + ('-'*22) + '+' + ('-'*22) + '+')
for k in range(len(top30)):
		print('\t' + top30[k][0] + '\t\t\t' + str(top30[k][1])) if len(top30[k][0]) <= 7 else print('\t' + top30[k][0] + '\t\t' + str(top30[k][1]))

print('+' + ('-'*20) + '+' + ('-'*20) + '+'+ ('-'*20) + '+' + ('-'*20) + '+')
print('|' + '  TOTAL OPEN PULLS  ' + '|' + ' TOTAL CLOSED PULLS ' + '|' + ' TOTAL OPEN ISSUES  ' + '|' + ' TOTAL CLOSED ISSUES' + '|')
print('+' + ('-'*20) + '+' + ('-'*20) + '+'+ ('-'*20) + '+' + ('-'*20) + '+')

if ((since != False and until != False) and ((len(since) != 0) and (len(until) != 0)) and (since < until)):
	print('\t' + str(requests.get('https://api.github.com/search/issues?q=repo:' + repository + '+type:pr+state:open+created%3A' + since + '..' + until).json()['total_count']) + '\t'*3 +
	str(requests.get('https://api.github.com/search/issues?q=repo:' + repository + '+type:pr+state:closed+created%3A' + since + '..' + until).json()['total_count']) + '\t'*2 +
	str(requests.get('https://api.github.com/search/issues?q=repo:' + repository + '+type:issue+state:open+created%3A' + since + '..' + until).json()['total_count']) + '\t'*3 +
	str(requests.get('https://api.github.com/search/issues?q=repo:' + repository + '+type:issue+state:closed+created%3A' + since + '..' + until).json()['total_count']))
else:
	print('\t' + str(requests.get('https://api.github.com/search/issues?q=repo:%s+type:pr+state:open'%repository).json()['total_count']) + '\t'*3 +
	str(requests.get('https://api.github.com/search/issues?q=repo:%s+type:pr+state:closed'%repository).json()['total_count']) + '\t'*2 +
	str(requests.get('https://api.github.com/search/issues?q=repo:%s+type:issue+state:open'%repository).json()['total_count']) + '\t'*3 +
	str(requests.get('https://api.github.com/search/issues?q=repo:%s+type:issue+state:closed'%repository).json()['total_count']))

dateissues = (datetime.datetime.now() - datetime.timedelta(days = 14)).strftime('%Y-%m-%d')
datepulls = (datetime.datetime.now() - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
old_issues = requests.get('https://api.github.com/search/issues?q=repo:%s'%repository + '+created%3A%3C%3D' + dateissues + '+state%3Aopen+is%3Aissue').json()
old_pulls = requests.get('https://api.github.com/search/issues?q=repo:%s'%repository  + '+created%3A%3C%3D' + datepulls + '+state%3Aopen+is%3Apr').json()
print("\nOld issues count: %s"%(old_issues['total_count']) + "\nOld pulls count: %s"%(old_pulls['total_count']))