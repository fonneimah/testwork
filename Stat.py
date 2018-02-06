import requests, re, datetime

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
print('\t' + str(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:pr+state:open').json()['total_count']) + '\t'*3 +
	  str(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:pr+state:closed').json()['total_count']) + '\t'*2 +
	  str(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:open').json()['total_count']) + '\t'*3 +
	  str(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:closed').json()['total_count']))

old_issues = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+created%3A%3C%3D' + (datetime.datetime.now() - datetime.timedelta(days = 14)).strftime('%Y-%m-%d') + '+state%3Aopen+is%3Aissue').json()['total_count']
old_pulls = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+created%3A%3C%3D' + (datetime.datetime.now() - datetime.timedelta(days = 30)).strftime('%Y-%m-%d') + '+state%3Aopen+is%3Apr').json()['total_count']
print("\nOld issues count: %s"%(old_issues) + "\nOld pulls count: %s"%(old_pulls))