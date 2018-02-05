import requests
raw = list(map(lambda x: (x['author']['login'], x['total']), requests.get('https://api.github.com/repos/googlechrome/puppeteer/stats/contributors').json()))
top30 = raw[::-1][:30]
print('+' + ('-'*22) + '+' + ('-'*22) + '+')
print('|' + (' '*9) + 'LOGIN' + (' '*8) + '|' + (' '*7) + 'COMMITS' + (' '*8) + '|')
print('+' + ('-'*22) + '+' + ('-'*22) + '+')
for k in range(len(top30)):
		print('\t' + top30[k][0] + '\t\t\t' + str(top30[k][1])) if len(top30[k][0]) <= 7 else print('\t' + top30[k][0] + '\t\t' + str(top30[k][1]))
